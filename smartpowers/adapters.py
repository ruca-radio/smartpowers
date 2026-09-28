"""Execution adapters. Commands use argv arrays, never a shell string."""

import json
import os
import signal
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

from .contracts import validate_result

MAX_OUTPUT = 2 * 1024 * 1024


class AdapterError(RuntimeError):
    def __init__(self, message, retryable=False):
        super().__init__(message)
        self.retryable = retryable


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def stop_process(process):
    if process.poll() is None:
        if os.name == 'posix':
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        else:
            process.kill()
        process.wait()


def execute_command(argv, payload, cwd, timeout, tick):
    with tempfile.TemporaryFile() as stdin, tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        stdin.write(payload.encode())
        stdin.seek(0)
        try:
            process = subprocess.Popen(argv, cwd=cwd, stdin=stdin, stdout=stdout, stderr=stderr,
                                       start_new_session=os.name == 'posix')
        except OSError as exc:
            raise AdapterError(f'Cannot start executable: {exc.strerror}', retryable=True) from exc
        started = time.monotonic()
        try:
            while process.poll() is None:
                tick()
                if time.monotonic() - started > timeout:
                    raise AdapterError('Command timed out', retryable=True)
                if os.fstat(stdout.fileno()).st_size + os.fstat(stderr.fileno()).st_size > MAX_OUTPUT:
                    raise AdapterError('Command output exceeded 2 MiB limit')
                time.sleep(0.05)
            tick()
            if os.fstat(stdout.fileno()).st_size + os.fstat(stderr.fileno()).st_size > MAX_OUTPUT:
                raise AdapterError('Command output exceeded 2 MiB limit')
            stdout.seek(0)
            stderr.seek(0)
            output = stdout.read(MAX_OUTPUT).decode('utf-8', errors='replace')
            error = stderr.read(MAX_OUTPUT).decode('utf-8', errors='replace')
            if process.returncode:
                # Do not persist raw stderr: CLIs may echo credentials in errors.
                raise AdapterError(f'Command exited with status {process.returncode}',
                                   retryable=process.returncode == 75)
            return output, error
        finally:
            stop_process(process)


def execute(target, request, tick):
    if target['adapter'] == 'command':
        payload = json.dumps(request) if target['input'] == 'json' else (
            request['task']['prompt'] + '\n\nSmartpowers context:\n' + json.dumps(request))
        output, _ = execute_command(target['command'], payload, request['task']['workspace'], target['timeout'], tick)
        if target['output'] == 'text':
            return {'version':1, 'status':'completed', 'output':output,
                    'evidence':['Command exited successfully; task verification is separate']}
        try:
            return validate_result(json.loads(output))
        except (ValueError, TypeError) as exc:
            raise AdapterError(f'Invalid worker result: {exc}') from exc
    if target['adapter'] == 'openai-compatible':
        key = os.environ.get(target.get('api_key_env',''), '')
        if target.get('api_key_env') and not key:
            raise AdapterError('API key environment variable is not set', retryable=True)
        body = {'model':target['model'], 'messages':[
            {'role':'user','content':request['task']['prompt'] + '\n\nTask context:\n' + json.dumps(request)}]}
        headers = {'Content-Type':'application/json'}
        if key:
            headers['Authorization'] = f'Bearer {key}'
        req = urllib.request.Request(target['url'], json.dumps(body).encode(), headers)
        tick()
        try:
            with urllib.request.build_opener(NoRedirect).open(req, timeout=target['timeout']) as response:
                data = response.read(MAX_OUTPUT+1)
                if len(data) > MAX_OUTPUT:
                    raise AdapterError('HTTP response exceeded 2 MiB limit')
            parsed = json.loads(data)
            output = parsed['choices'][0]['message']['content']
            if not isinstance(output, str):
                raise ValueError('Text response missing')
        except urllib.error.HTTPError as exc:
            raise AdapterError(f'Provider HTTP status {exc.code}', retryable=exc.code in (401,403,408,429) or exc.code >= 500) from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise AdapterError('Provider transport failed', retryable=True) from exc
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise AdapterError('Malformed provider response') from exc
        tick()
        return {'version':1,'status':'completed','output':output,'evidence':['Provider returned text']}
    raise AdapterError('External targets must be claimed by their harness worker')
