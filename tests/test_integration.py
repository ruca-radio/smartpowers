import json
import os
import signal
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from smartpowers.adapters import AdapterError, execute
from smartpowers.contracts import validate_workflow
from smartpowers.engine import Engine
from smartpowers.store import Store
from test_runtime import workflow

REPO=Path(__file__).resolve().parents[1]


class HTTPFixture(BaseHTTPRequestHandler):
    def do_POST(self):
        self.server.paths.append(self.path)
        self.rfile.read(int(self.headers.get('Content-Length',0)))
        if self.path=='/quota':
            self.send_response(429); self.end_headers(); return
        if self.path=='/redirect':
            self.send_response(302); self.send_header('Location','/ok'); self.end_headers(); return
        self.send_response(200); self.send_header('Content-Type','application/json'); self.end_headers()
        self.wfile.write(json.dumps({'choices':[{'message':{'content':'HTTP fixture result'}}]}).encode())

    def log_message(self,*args):
        pass


class IntegrationTests(unittest.TestCase):
    @unittest.skipUnless(os.name == 'posix', 'POSIX signal integration')
    def test_controller_interrupt_preserves_resumable_state(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t); database=root/'state.db'; spec=workflow(root)
            spec['targets'][0]['command']=[sys.executable,'-c',"from pathlib import Path; import time; Path('started').write_text('yes'); time.sleep(30)"]
            config=root/'workflow.json'; config.write_text(json.dumps(spec))
            process=subprocess.Popen([sys.executable,'-m','smartpowers','--db',str(database),'start',str(config)],cwd=REPO,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
            try:
                run=json.loads(process.stdout.readline())['run_id']
                deadline=time.monotonic()+5
                while not (root/'started').exists() and time.monotonic()<deadline:
                    time.sleep(0.01)
                self.assertTrue((root/'started').exists())
                process.send_signal(signal.SIGINT)
                process.communicate(timeout=5)
                self.assertEqual(process.returncode,130)
                snapshot=Store(database).snapshot(run)
                self.assertEqual(snapshot['tasks'][0]['status'],'pending')
                self.assertEqual(snapshot['tasks'][0]['attempts'],1)
            finally:
                if process.poll() is None:
                    process.kill(); process.communicate()

    def test_http_provider_fallback_and_redirect_rejection(self):
        server=ThreadingHTTPServer(('127.0.0.1',0),HTTPFixture)
        server.paths=[]
        thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
        try:
            with tempfile.TemporaryDirectory() as t:
                root=Path(t); store=Store(root/'state.db')
                spec=workflow(root)
                base=f'http://127.0.0.1:{server.server_port}'
                spec['authorization']['providers']=['provider-a','provider-b']
                spec['targets']=[
                    {'id':'quota','adapter':'openai-compatible','provider':'provider-a','model':'fixture-a',
                     'capabilities':['text'],'priority':0,'url':base+'/quota'},
                    {'id':'available','adapter':'openai-compatible','provider':'provider-b','model':'fixture-b',
                     'capabilities':['text'],'priority':1,'url':base+'/ok'},
                ]
                run=store.create(spec)
                result=Engine(store).run(run)
                self.assertEqual(result['status'],'completed')
                self.assertEqual(result['tasks'][0]['attempts'],2)
                self.assertEqual(result['tasks'][0]['result']['output'],'HTTP fixture result')
                target=validate_workflow(spec)['targets'][0]
                target['url']=base+'/redirect'
                request={'task':{'prompt':'hello'},'dependencies':{}}
                with self.assertRaises(AdapterError):
                    execute(target,request,lambda:None)
                self.assertEqual(server.paths,['/quota','/ok','/redirect'])
        finally:
            server.shutdown(); server.server_close(); thread.join()

    def test_cross_process_external_handoff_and_restart(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t); database=root/'state.db'
            spec=workflow(root,[{'id':'a','prompt':'external task','targets':['external'],'requires':['text']},
                                {'id':'b','prompt':'consume external artifact','depends_on':['a'],'targets':['worker'],'requires':['text']}])
            spec['targets'].append({'id':'external','adapter':'external','provider':'second-provider','model':'external-fixture','capabilities':['text']})
            spec['authorization']['providers'].append('second-provider')
            config=root/'workflow.json'; config.write_text(json.dumps(spec))
            def cli(*args,expected=0):
                result=subprocess.run([sys.executable,'-m','smartpowers','--db',str(database),*args],cwd=REPO,capture_output=True,text=True)
                self.assertEqual(result.returncode,expected,result.stderr+result.stdout)
                return result.stdout
            output=cli('start',str(config),'--no-run',expected=2)
            run=json.loads(output.splitlines()[0])['run_id']
            claimed=json.loads(cli('claim',run,'--owner','harness-one','--target','external'))
            cli('heartbeat',claimed['attempt_id'])
            result=root/'result.json'; result.write_text(json.dumps({'version':1,'status':'completed','output':'external artifact','evidence':['external process']}))
            cli('complete',claimed['attempt_id'],str(result))
            resumed=json.loads(cli('resume',run))
            self.assertEqual(resumed['status'],'completed')
            self.assertEqual([x['attempts'] for x in resumed['tasks']],[1,1])
            self.assertEqual(json.loads(cli('resume',run))['status'],'completed')
            self.assertEqual([x['attempts'] for x in Store(database).snapshot(run)['tasks']],[1,1])

    def test_cancel_stops_running_command(self):
        with tempfile.TemporaryDirectory() as t:
            root=Path(t); store=Store(root/'state.db'); spec=workflow(root)
            spec['targets'][0]['command']=[sys.executable,'-c',"from pathlib import Path; import time; Path('started').write_text('yes'); time.sleep(30); Path('late').write_text('bad')"]
            run=store.create(spec); errors=[]
            def runner():
                try: Engine(store).run(run)
                except Exception as exc: errors.append(exc)
            thread=threading.Thread(target=runner); thread.start()
            deadline=time.monotonic()+5
            while not (root/'started').exists() and time.monotonic()<deadline:
                time.sleep(0.01)
            self.assertTrue((root/'started').exists())
            store.cancel(run); thread.join(timeout=5)
            self.assertFalse(thread.is_alive())
            self.assertEqual(errors,[])
            self.assertFalse((root/'late').exists())
            self.assertEqual(store.snapshot(run)['status'],'cancelled')


if __name__=='__main__': unittest.main()
