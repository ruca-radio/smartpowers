import json
import sys
import tempfile
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from smartpowers.contracts import validate_workflow, route
from smartpowers.store import Store, StaleAttempt
from smartpowers.engine import Engine


def workflow(root, tasks=None):
    return {
        "version": 1,
        "root": str(root),
        "authorization": {"mode": "autonomous", "providers": ["local"], "capabilities": ["text"]},
        "targets": [{"id": "worker", "adapter": "command", "provider": "local", "model": "fixture",
                     "capabilities": ["text"], "command": [sys.executable, "-c",
                     "import json,sys; r=json.load(sys.stdin); print(json.dumps({'version':1,'status':'completed','output':r['task']['prompt'],'evidence':['fixture executed']}))"]}],
        "tasks": tasks or [{"id": "a", "prompt": "first", "requires": ["text"], "retry_safe": True}],
    }


class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.store = Store(self.root / "state.db")

    def tearDown(self):
        self.tmp.cleanup()

    def create(self, spec=None):
        return self.store.create(validate_workflow(spec or workflow(self.root)))

    def test_dependency_cycle_is_rejected(self):
        spec = workflow(self.root, [{"id":"a", "prompt":"a", "depends_on":["b"]},
                                    {"id":"b", "prompt":"b", "depends_on":["a"]}])
        with self.assertRaises(ValueError):
            validate_workflow(spec)

    def test_route_enforces_provider_and_capability_requirements(self):
        spec = validate_workflow(workflow(self.root))
        self.assertEqual(route(spec, spec['tasks'][0])[0]['id'], 'worker')
        spec['authorization']['providers'] = []
        self.assertEqual(route(spec, spec['tasks'][0]), [])

    def test_claim_is_exclusive_across_connections(self):
        run = self.create()
        def claim(n):
            return Store(self.root / 'state.db').claim(run, str(n), 'worker', lease_seconds=30)
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(claim, range(8)))
        self.assertEqual(sum(r is not None for r in results), 1)

    def test_expired_unsafe_attempt_requires_reconciliation(self):
        spec = workflow(self.root)
        spec['tasks'][0]['retry_safe'] = False
        run = self.create(spec)
        self.store.claim(run, 'old', 'worker', lease_seconds=0.01)
        time.sleep(0.02)
        self.store.recover(run)
        self.assertEqual(self.store.snapshot(run)['tasks'][0]['status'], 'blocked')

    def test_stale_worker_cannot_complete_after_reassignment(self):
        run = self.create()
        old = self.store.claim(run, 'old', 'worker', lease_seconds=0.01)
        time.sleep(0.02)
        self.store.recover(run)
        new = self.store.claim(run, 'new', 'worker')
        with self.assertRaises(StaleAttempt):
            self.store.finish(old['attempt_id'], 'completed', {'output':'stale'})
        self.store.finish(new['attempt_id'], 'completed', {'output':'fresh'})

    def test_restart_skips_completed_dependencies(self):
        run = self.create(workflow(self.root, [
            {'id':'a','prompt':'first','requires':['text'],'retry_safe':True},
            {'id':'b','prompt':'second','requires':['text'],'depends_on':['a'],'retry_safe':True},
        ]))
        first = self.store.claim(run, 'external', 'worker', task_id='a')
        self.store.finish(first['attempt_id'], 'completed', {'output':'already done'})
        Engine(Store(self.root / 'state.db')).run(run)
        snapshot = self.store.snapshot(run)
        self.assertEqual(snapshot['status'], 'completed')
        self.assertEqual([t['attempts'] for t in snapshot['tasks']], [1,1])

    def test_messages_are_durable_and_acknowledged_by_recipient(self):
        run = self.create()
        message = self.store.send(run, 'a', 'b', {'question':'interface?'}, 'thread-1')
        again = Store(self.root / 'state.db')
        self.assertEqual(again.inbox(run, 'b')[0]['id'], message)
        with self.assertRaises(ValueError):
            again.ack(run, 'a', message)
        again.ack(run, 'b', message)
        self.assertEqual(again.inbox(run, 'b'), [])

    def test_verification_failure_does_not_mark_completed(self):
        spec = workflow(self.root)
        spec['tasks'][0]['verify'] = [[sys.executable, '-c', 'raise SystemExit(1)']]
        spec['authorization']['capabilities'].append('shell')
        run = self.create(spec)
        Engine(self.store).run(run)
        self.assertEqual(self.store.snapshot(run)['tasks'][0]['status'], 'failed')

    def test_cancel_fences_result_and_blocks_dependents(self):
        run = self.create()
        attempt = self.store.claim(run, 'worker', 'worker')
        self.store.cancel(run)
        with self.assertRaises(StaleAttempt):
            self.store.finish(attempt['attempt_id'], 'completed', {})
        self.assertEqual(self.store.snapshot(run)['status'], 'cancelled')

    def test_fallback_requires_retry_safe(self):
        spec = workflow(self.root)
        bad = dict(spec['targets'][0], id='bad', priority=0, command=[sys.executable, '-c', 'raise SystemExit(75)'])
        spec['targets'].insert(0, bad)
        spec['targets'][1]['priority'] = 1
        run = self.create(spec)
        Engine(self.store).run(run)
        self.assertEqual(self.store.snapshot(run)['status'], 'completed')
        self.assertEqual(self.store.snapshot(run)['tasks'][0]['attempts'], 2)

    def test_nonfinite_leases_are_rejected(self):
        run = self.create()
        for value in (float('inf'), float('nan'), -1, 0, True):
            with self.assertRaises(ValueError):
                self.store.claim(run,'owner','worker',lease_seconds=value)
        request = self.store.claim(run,'owner','worker')
        with self.assertRaises(ValueError):
            self.store.heartbeat(request['attempt_id'],float('inf'))

    def test_duplicate_completion_runs_verification_once(self):
        spec=workflow(self.root)
        spec['authorization']['capabilities'].append('shell')
        marker=self.root/'verified'
        spec['tasks'][0]['verify']=[[sys.executable,'-c',
            "from pathlib import Path; import time; p=Path('verified'); p.open('a').write('verified\\n'); time.sleep(0.05)"]]
        run=self.create(spec)
        request=self.store.claim(run,'external','worker')
        def complete(index):
            try:
                Engine(Store(self.root/'state.db')).complete(request,{'version':1,'status':'completed','output':str(index)})
                return 'completed'
            except StaleAttempt:
                return 'stale'
        with ThreadPoolExecutor(max_workers=2) as pool:
            results=list(pool.map(complete,range(2)))
        self.assertCountEqual(results,['completed','stale'])
        self.assertEqual(marker.read_text(),'verified\n')
        result=self.store.snapshot(run)['tasks'][0]['result']
        self.assertEqual(json.loads((self.root/result['artifact']).read_text())['output'],result['output'])

    def test_supervised_approval_resumes_blocked_task(self):
        spec=workflow(self.root)
        spec['authorization']['mode']='supervised'
        run=self.create(spec)
        self.assertEqual(Engine(self.store).run(run)['status'],'blocked')
        self.store.approve(run,'a')
        self.assertEqual(Engine(self.store).run(run)['status'],'completed')

    def test_resources_serialize_shared_writers(self):
        spec=workflow(self.root,[{'id':'a','prompt':'a','resources':['checkout']},
                                  {'id':'b','prompt':'b','resources':['checkout']}])
        run=self.create(spec)
        first=self.store.claim(run,'one','worker',task_id='a')
        self.assertIsNone(self.store.claim(run,'two','worker',task_id='b'))
        self.store.finish(first['attempt_id'],'completed',{'output':'a'})
        self.assertIsNotNone(self.store.claim(run,'two','worker',task_id='b'))

    def test_context_requirement_excludes_unknown_or_small_targets(self):
        spec=validate_workflow(workflow(self.root))
        task=spec['tasks'][0]
        task['min_context_tokens']=32000
        self.assertEqual(route(spec,task),[])
        spec['targets'][0]['context_tokens']=32768
        self.assertEqual(route(spec,task)[0]['id'],'worker')

    def test_unsafe_task_does_not_fallback(self):
        spec=workflow(self.root)
        spec['tasks'][0]['retry_safe']=False
        spec['targets'][0]['command']=[sys.executable,'-c','raise SystemExit(75)']
        run=self.create(spec)
        self.assertEqual(Engine(self.store).run(run)['status'],'failed')
        self.assertEqual(self.store.snapshot(run)['tasks'][0]['attempts'],1)

    def test_reconciled_parent_unblocks_dependents(self):
        spec=workflow(self.root,[{'id':'a','prompt':'a'},
                                {'id':'b','prompt':'b','depends_on':['a']}])
        run=self.create(spec)
        request=self.store.claim(run,'one','worker',task_id='a')
        self.store.finish(request['attempt_id'],'failed',{'output':'failure'})
        self.store.block_unrunnable(run)
        self.store.reconcile(run,'a','completed','Verified prior result')
        self.assertEqual(Engine(self.store).run(run)['status'],'completed')


if __name__ == '__main__':
    unittest.main()
