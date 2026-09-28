"""Restartable bounded-concurrency scheduler."""

import json
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from pathlib import Path

from .adapters import AdapterError, execute, execute_command
from .contracts import route, validate_result
from .store import StaleAttempt


class Engine:
    def __init__(self, store):
        self.store = store
        self.stopping = threading.Event()

    def complete(self, request, result, tick=lambda:None):
        result = dict(validate_result(result))
        self.store.reserve_completion(request['attempt_id'])
        if result['status'] == 'completed':
            evidence = list(result.get('evidence', []))
            for command in request['task']['verify']:
                try:
                    execute_command(command, '', request['task']['workspace'], 300, tick)
                    evidence.append('Verification passed: ' + json.dumps(command))
                except AdapterError as exc:
                    result.update(status='failed', verification_error=str(exc))
                    break
            result['evidence'] = evidence
        artifact_dir = self.store.path.parent / 'artifacts' / request['run_id'] / request['attempt_id']
        artifact_dir.mkdir(parents=True, exist_ok=True)
        artifact = artifact_dir / 'result.json'
        temporary = artifact.with_name(uuid.uuid4().hex + '.tmp')
        temporary.write_text(json.dumps(result, indent=2) + '\n')
        temporary.replace(artifact)
        result['artifact'] = str(artifact.relative_to(self.store.path.parent))
        self.store.finish(request['attempt_id'], result['status'], result)

    def work(self, target, request):
        attempt = request['attempt_id']
        done, lost = threading.Event(), threading.Event()
        def pulse():
            while not done.wait(5):
                try:
                    self.store.heartbeat(attempt)
                except StaleAttempt:
                    lost.set()
                    return
        def tick():
            if self.stopping.is_set():
                raise InterruptedError('Controller interrupted')
            if lost.is_set():
                raise StaleAttempt('Lease lost or run cancelled')
            self.store.heartbeat(attempt)
        thread = threading.Thread(target=pulse, daemon=True)
        thread.start()
        try:
            result = execute(target, request, tick)
            self.complete(request, result, tick)
        except AdapterError as exc:
            try:
                self.store.finish(attempt, 'failed', {'error':str(exc)}, retry=exc.retryable)
            except StaleAttempt:
                pass
        except InterruptedError:
            try:
                self.store.finish(attempt, 'blocked', {'error':'Controller interrupted; inspect effects before resuming'},
                                  retry=request['task']['retry_safe'])
            except StaleAttempt:
                pass
        except StaleAttempt:
            pass
        finally:
            done.set()
            thread.join()

    def run(self, run, workers=4):
        if workers < 1:
            raise ValueError('workers must be positive')
        owner = 'controller-' + uuid.uuid4().hex
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = set()
            try:
                while True:
                    self.store.recover(run)
                    spec = self.store.spec(run)
                    snapshot = self.store.snapshot(run)
                    if snapshot['status'] == 'cancelled':
                        break
                    rows = {t['id']:t for t in snapshot['tasks']}
                    for task in spec['tasks']:
                        if len(futures) >= workers:
                            break
                        if rows[task['id']]['status'] != 'pending':
                            continue
                        candidates = route(spec, task, self.store.failed_targets(run,task['id']))
                        if not candidates:
                            candidates = route(spec, task)
                        if not candidates or candidates[0]['adapter'] == 'external':
                            continue
                        target = candidates[0]
                        request = self.store.claim(run,owner,target['id'],task_id=task['id'])
                        if request:
                            request['target'] = {k:v for k,v in target.items() if k in ('id','model','provider','capabilities')}
                            futures.add(pool.submit(self.work,target,request))
                    if futures:
                        completed, futures = wait(futures, timeout=0.2, return_when=FIRST_COMPLETED)
                        for future in completed:
                            future.result()
                        continue
                    self.store.block_unrunnable(run)
                    # A different controller or external harness owns active work.
                    # Return durable state; a supervisor can invoke resume later.
                    after = self.store.snapshot(run)
                    if after != snapshot and any(t['status']=='pending' for t in after['tasks']):
                        continue
                    return after
            except BaseException:
                self.stopping.set()
                raise
        return self.store.snapshot(run)
