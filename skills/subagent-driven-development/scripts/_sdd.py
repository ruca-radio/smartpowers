"""Shared standalone helpers for installed SDD skills."""
import fcntl
import hashlib
import json
import re
import subprocess
import uuid
from pathlib import Path


def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()


def workspace(plan, new=False):
    plan = Path(plan).resolve(strict=True)
    root = Path(git('rev-parse', '--show-toplevel'))
    identity = hashlib.sha256(str(plan).encode() + b'\0' + plan.read_bytes()).hexdigest()[:24]
    base = root / '.smartpowers' / 'sdd'
    base.mkdir(parents=True, exist_ok=True)
    exclude = Path(git('rev-parse', '--git-path', 'info/exclude')).resolve()
    exclude.parent.mkdir(parents=True, exist_ok=True)
    with exclude.open('a+') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        stream.seek(0)
        if '/.smartpowers/' not in stream.read().splitlines():
            stream.write('\n/.smartpowers/\n')
    with (base / '.lock').open('a+') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        pointer = base / (identity + '.current')
        if pointer.exists() and not new:
            name = pointer.read_text().strip()
            if re.fullmatch(r'[a-f0-9]{32}', name) and (base / name).is_dir():
                return base / name
        name = uuid.uuid4().hex
        out = base / name
        out.mkdir()
        (out / 'run.json').write_text(json.dumps({'version':1,'run_id':name,'plan':str(plan),'identity':identity}, indent=2)+'\n')
        temp = pointer.with_suffix('.tmp')
        temp.write_text(name+'\n')
        temp.replace(pointer)
        return out


def task_text(plan, number):
    lines = Path(plan).read_text().splitlines(keepends=True)
    fence = None
    found = False
    result = []
    for line in lines:
        match = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', line)
        if fence:
            if found:
                result.append(line)
            if match and match[1][0] == fence[0] and len(match[1]) >= fence[1] and not match[2].strip():
                fence = None
            continue
        if match:
            fence = (match[1][0], len(match[1]))
            if found:
                result.append(line)
            continue
        heading = re.match(r'^ {0,3}(#{1,6})\s+(.*)$', line)
        if heading:
            if found and len(heading[1]) <= 3:
                break
            task = re.fullmatch(r'Task ([0-9]+):.*', heading[2])
            if len(heading[1]) == 3 and task and int(task[1]) == number:
                found = True
        if found:
            result.append(line)
    if not found:
        raise ValueError(f'No Task {number} heading in {plan}')
    return ''.join(result)
