"""Transactional run state, fenced task leases and durable mailboxes."""

import json
import sqlite3
import time
import uuid
from contextlib import contextmanager
from pathlib import Path

from .contracts import positive, route, validate_workflow


class StaleAttempt(RuntimeError):
    pass


class Store:
    def __init__(self, path):
        self.path = Path(path).resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.execute('PRAGMA journal_mode=WAL')
            version = db.execute('PRAGMA user_version').fetchone()[0]
            if version not in (0, 1):
                raise ValueError('Unsupported state database version')
            db.executescript('''
                CREATE TABLE IF NOT EXISTS runs (
                    id TEXT PRIMARY KEY, spec TEXT NOT NULL, status TEXT NOT NULL, created REAL NOT NULL);
                CREATE TABLE IF NOT EXISTS tasks (
                    run_id TEXT NOT NULL, id TEXT NOT NULL, status TEXT NOT NULL,
                    attempts INTEGER NOT NULL DEFAULT 0, active TEXT, result TEXT,
                    PRIMARY KEY (run_id,id));
                CREATE TABLE IF NOT EXISTS attempts (
                    id TEXT PRIMARY KEY, run_id TEXT NOT NULL, task_id TEXT NOT NULL,
                    owner TEXT NOT NULL, target TEXT NOT NULL, status TEXT NOT NULL,
                    expires REAL NOT NULL, result TEXT);
                CREATE TABLE IF NOT EXISTS events (
                    seq INTEGER PRIMARY KEY AUTOINCREMENT, run_id TEXT NOT NULL,
                    kind TEXT NOT NULL, payload TEXT NOT NULL, created REAL NOT NULL);
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY, run_id TEXT NOT NULL, sender TEXT NOT NULL,
                    recipient TEXT NOT NULL, correlation_id TEXT NOT NULL, payload TEXT NOT NULL,
                    created REAL NOT NULL, acknowledged REAL);
                PRAGMA user_version=1;
            ''')

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=30, isolation_level=None)
        db.row_factory = sqlite3.Row
        try:
            yield db
        finally:
            db.close()

    @contextmanager
    def transaction(self):
        with self.connection() as db:
            db.execute('BEGIN IMMEDIATE')
            try:
                yield db
                db.commit()
            except BaseException:
                db.rollback()
                raise

    def _event(self, db, run, kind, payload):
        db.execute('INSERT INTO events(run_id,kind,payload,created) VALUES(?,?,?,?)',
                   (run, kind, json.dumps(payload), time.time()))

    def _spec(self, db, run):
        row = db.execute('SELECT spec FROM runs WHERE id=?', (run,)).fetchone()
        if row is None:
            raise ValueError(f'Unknown run: {run}')
        return json.loads(row[0])

    def create(self, spec):
        spec = validate_workflow(spec)
        run = uuid.uuid4().hex
        with self.transaction() as db:
            db.execute('INSERT INTO runs VALUES(?,?,?,?)', (run, json.dumps(spec), 'pending', time.time()))
            db.executemany('INSERT INTO tasks(run_id,id,status) VALUES(?,?,?)',
                           [(run, t['id'], 'pending') for t in spec['tasks']])
            self._event(db, run, 'run.created', {'version':1})
        return run

    def spec(self, run):
        with self.connection() as db:
            return self._spec(db, run)

    def _refresh(self, db, run):
        if db.execute('SELECT status FROM runs WHERE id=?', (run,)).fetchone()[0] == 'cancelled':
            return
        spec = self._spec(db, run)
        rows = {r['id']:r for r in db.execute('SELECT * FROM tasks WHERE run_id=?', (run,))}
        for task in spec['tasks']:
            row = rows[task['id']]
            if row['status'] != 'blocked' or not row['result']:
                continue
            result = json.loads(row['result'])
            if result.get('reason') == 'Dependency did not complete' and all(rows[d]['status'] in ('completed','pending','running') for d in task['depends_on']):
                db.execute("UPDATE tasks SET status='pending', result=NULL WHERE run_id=? AND id=?", (run,task['id']))
        states = [r[0] for r in db.execute('SELECT status FROM tasks WHERE run_id=?', (run,))]
        if all(s == 'completed' for s in states):
            status = 'completed'
        elif 'running' in states:
            status = 'running'
        elif 'pending' in states:
            status = 'pending'
        elif 'failed' in states:
            status = 'failed'
        else:
            status = 'blocked'
        db.execute('UPDATE runs SET status=? WHERE id=?', (status, run))

    def claim(self, run, owner, target_id, task_id=None, lease_seconds=30):
        positive(lease_seconds, 'lease_seconds')
        with self.transaction() as db:
            spec = self._spec(db, run)
            if db.execute('SELECT status FROM runs WHERE id=?', (run,)).fetchone()[0] == 'cancelled':
                return None
            rows = {r['id']: dict(r) for r in db.execute('SELECT * FROM tasks WHERE run_id=?', (run,))}
            busy = set()
            for task in spec['tasks']:
                if rows[task['id']]['status'] == 'running':
                    busy.update(task['resources'])
            for task in spec['tasks']:
                tid = task['id']
                state = rows[tid]
                if task_id is not None and task_id != tid:
                    continue
                if state['status'] != 'pending' or state['attempts'] >= task['max_attempts']:
                    continue
                if any(rows[d]['status'] != 'completed' for d in task['depends_on']):
                    continue
                if set(task['resources']) & busy:
                    continue
                if target_id not in {t['id'] for t in route(spec, task)}:
                    continue
                attempt = uuid.uuid4().hex
                db.execute('INSERT INTO attempts VALUES(?,?,?,?,?,?,?,NULL)',
                           (attempt, run, tid, owner, target_id, 'running', time.time()+lease_seconds))
                db.execute("UPDATE tasks SET status='running', active=?, attempts=attempts+1 WHERE run_id=? AND id=?",
                           (attempt, run, tid))
                self._event(db, run, 'task.claimed', {'task_id':tid, 'attempt_id':attempt, 'owner':owner, 'target':target_id})
                self._refresh(db, run)
                dependencies = {d: json.loads(rows[d]['result']) for d in task['depends_on']}
                return {'version':1, 'run_id':run, 'task':task, 'attempt_id':attempt,
                        'idempotency_key':f'{run}:{tid}', 'dependencies':dependencies,
                        'authorization':spec['authorization']}
        return None

    def _active(self, db, attempt):
        row = db.execute('SELECT * FROM attempts WHERE id=?', (attempt,)).fetchone()
        if row is None or row['status'] not in ('running', 'verifying') or row['expires'] <= time.time():
            raise StaleAttempt('Attempt is expired, cancelled, or superseded')
        task = db.execute('SELECT active FROM tasks WHERE run_id=? AND id=?', (row['run_id'], row['task_id'])).fetchone()
        if task['active'] != attempt:
            raise StaleAttempt('Attempt no longer owns task')
        return row

    def heartbeat(self, attempt, lease_seconds=30):
        positive(lease_seconds, 'lease_seconds')
        with self.transaction() as db:
            self._active(db, attempt)
            db.execute('UPDATE attempts SET expires=? WHERE id=?', (time.time()+lease_seconds, attempt))

    def reserve_completion(self, attempt):
        with self.transaction() as db:
            row = self._active(db, attempt)
            if row['status'] != 'running':
                raise StaleAttempt('Completion is already reserved by another submission')
            db.execute("UPDATE attempts SET status='verifying' WHERE id=?", (attempt,))
            self._event(db,row['run_id'],'task.verifying',{'attempt_id':attempt})

    def finish(self, attempt, status, result, retry=False):
        if status not in ('completed', 'failed', 'blocked'):
            raise ValueError('Invalid terminal status')
        with self.transaction() as db:
            row = self._active(db, attempt)
            run, tid = row['run_id'], row['task_id']
            task = next(t for t in self._spec(db, run)['tasks'] if t['id'] == tid)
            tries = db.execute('SELECT attempts FROM tasks WHERE run_id=? AND id=?', (run, tid)).fetchone()[0]
            next_status = status
            if retry and status != 'completed' and task['retry_safe'] and tries < task['max_attempts']:
                next_status = 'pending'
            payload = json.dumps(result)
            db.execute('UPDATE attempts SET status=?, result=? WHERE id=?', (status, payload, attempt))
            db.execute('UPDATE tasks SET status=?, result=?, active=NULL WHERE run_id=? AND id=?',
                       (next_status, payload, run, tid))
            self._event(db, run, 'task.finished', {'task_id':tid, 'attempt_id':attempt, 'status':next_status, 'result':result})
            self._refresh(db, run)

    def recover(self, run):
        with self.transaction() as db:
            spec = self._spec(db, run)
            tasks = {t['id']:t for t in spec['tasks']}
            rows = db.execute("SELECT * FROM attempts WHERE run_id=? AND status IN ('running','verifying') AND expires<=?", (run, time.time())).fetchall()
            for row in rows:
                task = tasks[row['task_id']]
                tries = db.execute('SELECT attempts FROM tasks WHERE run_id=? AND id=?', (run, row['task_id'])).fetchone()[0]
                status = 'pending' if task['retry_safe'] and tries < task['max_attempts'] else 'blocked'
                result = json.dumps({'reason':'Lease expired; reconcile possible side effects before retry'})
                db.execute("UPDATE attempts SET status='expired' WHERE id=?", (row['id'],))
                db.execute('UPDATE tasks SET status=?, active=NULL, result=? WHERE run_id=? AND id=? AND active=?',
                           (status, result, run, row['task_id'], row['id']))
                self._event(db, run, 'task.recovered', {'task_id':row['task_id'], 'status':status})
            self._refresh(db, run)

    def reconcile(self, run, task_id, status, evidence):
        if status not in ('pending', 'completed', 'failed') or not evidence.strip():
            raise ValueError('Reconciliation requires a valid state and evidence')
        with self.transaction() as db:
            self._spec(db, run)
            row = db.execute('SELECT * FROM tasks WHERE run_id=? AND id=?', (run, task_id)).fetchone()
            if row is None or row['status'] not in ('blocked', 'failed'):
                raise ValueError('Only blocked or failed tasks can be reconciled')
            if db.execute('SELECT status FROM runs WHERE id=?', (run,)).fetchone()[0] == 'cancelled':
                raise ValueError('Cancelled runs cannot be reconciled')
            task = next(t for t in self._spec(db, run)['tasks'] if t['id'] == task_id)
            if status == 'pending' and row['attempts'] >= task['max_attempts']:
                raise ValueError('Attempt budget exhausted; create a new scoped run')
            result = {'output':evidence, 'reconciled':True}
            db.execute('UPDATE tasks SET status=?, result=? WHERE run_id=? AND id=?', (status, json.dumps(result), run, task_id))
            self._event(db, run, 'task.reconciled', {'task_id':task_id,'status':status,'evidence':evidence})
            self._refresh(db, run)

    def approve(self, run, task_id):
        with self.transaction() as db:
            spec = self._spec(db, run)
            task = next((t for t in spec['tasks'] if t['id'] == task_id), None)
            if task is None:
                raise ValueError('Unknown task')
            task['approved'] = True
            db.execute('UPDATE runs SET spec=? WHERE id=?', (json.dumps(spec),run))
            db.execute("UPDATE tasks SET status='pending', result=NULL WHERE run_id=? AND id=? AND status='blocked' AND attempts=0",(run,task_id))
            self._event(db, run, 'task.approved', {'task_id':task_id})
            self._refresh(db, run)

    def cancel(self, run):
        with self.transaction() as db:
            self._spec(db, run)
            db.execute("UPDATE runs SET status='cancelled' WHERE id=?", (run,))
            db.execute("UPDATE tasks SET status='cancelled', active=NULL WHERE run_id=? AND status IN ('pending','running','blocked')", (run,))
            db.execute("UPDATE attempts SET status='cancelled' WHERE run_id=? AND status IN ('running','verifying')", (run,))
            self._event(db, run, 'run.cancelled', {})

    def block_unrunnable(self, run):
        with self.transaction() as db:
            spec = self._spec(db, run)
            states = {r['id']:r['status'] for r in db.execute('SELECT * FROM tasks WHERE run_id=?',(run,))}
            for task in spec['tasks']:
                if states[task['id']] != 'pending':
                    continue
                reason = None
                if any(states[d] in ('failed','blocked','cancelled') for d in task['depends_on']):
                    reason = 'Dependency did not complete'
                elif not route(spec, task):
                    reason = 'No authorized, compatible target; approve or correct configuration'
                if reason:
                    db.execute("UPDATE tasks SET status='blocked', result=? WHERE run_id=? AND id=?",
                               (json.dumps({'reason':reason}),run,task['id']))
                    self._event(db,run,'task.blocked',{'task_id':task['id'],'reason':reason})
            self._refresh(db,run)

    def snapshot(self, run):
        with self.connection() as db:
            self._spec(db, run)
            data = dict(db.execute('SELECT id,status,created FROM runs WHERE id=?',(run,)).fetchone())
            data['tasks'] = [dict(r) for r in db.execute('SELECT * FROM tasks WHERE run_id=? ORDER BY rowid',(run,))]
            for task in data['tasks']:
                task['result'] = json.loads(task['result']) if task['result'] else None
            return data

    def events(self, run):
        with self.connection() as db:
            self._spec(db, run)
            rows = [dict(r) for r in db.execute('SELECT * FROM events WHERE run_id=? ORDER BY seq',(run,))]
            for row in rows:
                row['payload'] = json.loads(row['payload'])
            return rows

    def failed_targets(self, run, task):
        with self.connection() as db:
            return [r[0] for r in db.execute("SELECT target FROM attempts WHERE run_id=? AND task_id=? AND status IN ('failed','blocked')",(run,task))]

    def send(self, run, sender, recipient, payload, correlation_id):
        if not sender or not recipient or not correlation_id:
            raise ValueError('Message needs sender, recipient, and correlation_id')
        mid = uuid.uuid4().hex
        with self.transaction() as db:
            self._spec(db,run)
            db.execute('INSERT INTO messages VALUES(?,?,?,?,?,?,?,NULL)',
                       (mid,run,sender,recipient,correlation_id,json.dumps(payload),time.time()))
            self._event(db,run,'message.sent',{'message_id':mid,'sender':sender,'recipient':recipient})
        return mid

    def inbox(self, run, recipient):
        with self.connection() as db:
            self._spec(db,run)
            rows = [dict(r) for r in db.execute('SELECT * FROM messages WHERE run_id=? AND recipient=? AND acknowledged IS NULL ORDER BY created',(run,recipient))]
            for row in rows:
                row['payload'] = json.loads(row['payload'])
            return rows

    def ack(self, run, recipient, message):
        with self.transaction() as db:
            cursor = db.execute('UPDATE messages SET acknowledged=? WHERE run_id=? AND recipient=? AND id=?',
                                (time.time(),run,recipient,message))
            if cursor.rowcount != 1:
                raise ValueError('Message does not belong to this recipient')
            self._event(db,run,'message.acknowledged',{'message_id':message,'recipient':recipient})
