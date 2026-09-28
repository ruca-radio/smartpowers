"""JSON CLI for local controllers and external harness workers."""

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .contracts import validate_workflow
from .engine import Engine
from .store import Store, StaleAttempt


def main(argv=None):
    parser = argparse.ArgumentParser(prog='smartpowers')
    parser.add_argument('--version', action='version', version=__version__)
    parser.add_argument('--db', default='.smartpowers/state.db')
    commands = parser.add_subparsers(dest='command', required=True)
    for name in ('validate','start'):
        p = commands.add_parser(name)
        p.add_argument('workflow')
        if name == 'start':
            p.add_argument('--workers', type=int, default=4)
            p.add_argument('--no-run', action='store_true')
    for name in ('status','events','resume','cancel','recover','export'):
        p = commands.add_parser(name)
        p.add_argument('run')
        if name == 'resume':
            p.add_argument('--workers', type=int, default=4)
    p = commands.add_parser('claim')
    p.add_argument('run'); p.add_argument('--owner', required=True); p.add_argument('--target', required=True)
    p.add_argument('--task'); p.add_argument('--lease', type=float, default=30)
    p = commands.add_parser('heartbeat')
    p.add_argument('attempt'); p.add_argument('--lease', type=float, default=30)
    p = commands.add_parser('complete')
    p.add_argument('attempt'); p.add_argument('result')
    p = commands.add_parser('approve')
    p.add_argument('run'); p.add_argument('task')
    p = commands.add_parser('reconcile')
    p.add_argument('run'); p.add_argument('task')
    p.add_argument('--status', choices=['pending','completed','failed'], required=True)
    p.add_argument('--evidence', required=True)
    p = commands.add_parser('send')
    p.add_argument('run'); p.add_argument('--sender', required=True); p.add_argument('--recipient', required=True)
    p.add_argument('--correlation', required=True); p.add_argument('--body', required=True)
    p = commands.add_parser('inbox')
    p.add_argument('run'); p.add_argument('recipient')
    p = commands.add_parser('ack')
    p.add_argument('run'); p.add_argument('recipient'); p.add_argument('message')
    args = parser.parse_args(argv)
    try:
        if args.command in ('validate','start'):
            spec = validate_workflow(json.loads(Path(args.workflow).read_text()))
            if args.command == 'validate':
                print(json.dumps({'valid':True,'version':spec['version']}))
                return 0
        store = Store(args.db)
        command = args.command
        if command == 'start':
            run = store.create(spec)
            # Flush the run ID before any long-running work or interruption.
            print(json.dumps({'run_id':run}), flush=True)
            result = store.snapshot(run) if args.no_run else Engine(store).run(run,args.workers)
        elif command == 'resume':
            result = Engine(store).run(args.run,args.workers)
        elif command == 'status':
            result = store.snapshot(args.run)
        elif command == 'events':
            result = store.events(args.run)
        elif command == 'export':
            result = {'version':1,'spec':store.spec(args.run),'state':store.snapshot(args.run),'events':store.events(args.run)}
        elif command == 'claim':
            result = store.claim(args.run,args.owner,args.target,args.task,args.lease)
        elif command == 'heartbeat':
            store.heartbeat(args.attempt,args.lease); result = {'ok':True}
        elif command == 'complete':
            with store.connection() as db:
                row = store._active(db,args.attempt)
                spec = store._spec(db,row['run_id'])
                target = next(t for t in spec['targets'] if t['id']==row['target'])
                if target['adapter'] != 'external':
                    raise ValueError('CLI completion is for external harness targets')
                task = next(t for t in spec['tasks'] if t['id']==row['task_id'])
                request = {'run_id':row['run_id'],'attempt_id':args.attempt,'task':task}
            Engine(store).complete(request,json.loads(Path(args.result).read_text()),lambda:store.heartbeat(args.attempt))
            result = {'ok':True}
        elif command == 'reconcile':
            store.reconcile(args.run,args.task,args.status,args.evidence); result = {'ok':True}
        elif command == 'approve':
            store.approve(args.run,args.task); result = {'ok':True}
        elif command == 'cancel':
            store.cancel(args.run); result = {'ok':True}
        elif command == 'recover':
            store.recover(args.run); result = store.snapshot(args.run)
        elif command == 'send':
            result = {'message_id':store.send(args.run,args.sender,args.recipient,args.body,args.correlation)}
        elif command == 'inbox':
            result = store.inbox(args.run,args.recipient)
        elif command == 'ack':
            store.ack(args.run,args.recipient,args.message); result = {'ok':True}
        print(json.dumps(result,indent=2))
        if command in ('start','resume'):
            return 0 if result['status']=='completed' else 2
        return 0
    except (ValueError, TypeError, KeyError, OSError, StaleAttempt) as exc:
        print(json.dumps({'error':str(exc)}),file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print(json.dumps({'error':'Interrupted; state retained. Resume by run ID.'}),file=sys.stderr)
        return 130


if __name__ == '__main__':
    sys.exit(main())
