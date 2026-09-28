"""Versioned, provider-neutral workflow and worker contracts."""

import copy
import math
import re
from pathlib import Path

PROTOCOL_VERSION = 1
IDENTIFIER = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,127}$')


def identifier(value):
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        raise ValueError(f'Invalid identifier: {value!r}')
    return value


def strings(value, name):
    if not isinstance(value, list) or any(not isinstance(v, str) or not v for v in value):
        raise ValueError(f'{name} must be a list of nonempty strings')
    return value


def positive(value, name):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value) or value <= 0:
        raise ValueError(f'{name} must be positive and finite')
    return value


def validate_workflow(raw):
    if not isinstance(raw, dict):
        raise ValueError('Workflow must be an object')
    spec = copy.deepcopy(raw)
    if type(spec.get('version')) is not int or spec['version'] != PROTOCOL_VERSION:
        raise ValueError('Unsupported workflow version')
    root = Path(spec.get('root', '.')).resolve()
    if not root.is_dir():
        raise ValueError('Workflow root must exist')
    spec['root'] = str(root)
    auth = spec.get('authorization', {})
    if not isinstance(auth, dict):
        raise ValueError('authorization must be an object')
    if auth.get('mode') not in ('autonomous', 'supervised'):
        raise ValueError('Set authorization.mode to autonomous or supervised')
    for field in ('providers', 'capabilities'):
        strings(auth.get(field), f'authorization.{field}')
    targets = spec.get('targets')
    tasks = spec.get('tasks')
    if not isinstance(targets, list) or not targets or not isinstance(tasks, list) or not tasks:
        raise ValueError('Workflow needs targets and tasks')
    ids = set()
    for target in targets:
        if not isinstance(target, dict):
            raise ValueError('Target must be an object')
        tid = identifier(target['id'])
        if tid in ids:
            raise ValueError(f'Duplicate target: {tid}')
        ids.add(tid)
        identifier(target['provider'])
        if not isinstance(target.get('model'), str) or not target['model']:
            raise ValueError('Each target needs a model identifier')
        strings(target.get('capabilities', []), 'target capabilities')
        target.setdefault('priority', 100)
        if isinstance(target['priority'], bool) or not isinstance(target['priority'], int):
            raise ValueError('Target priority must be an integer')
        positive(target.setdefault('timeout', 300), 'target timeout')
        if 'context_tokens' in target:
            positive(target['context_tokens'], 'context_tokens')
        adapter = target.get('adapter')
        if adapter == 'command':
            if not strings(target.get('command'), 'target command'):
                raise ValueError('Command cannot be empty')
            target.setdefault('input', 'json')
            target.setdefault('output', 'json')
            if target['input'] not in ('json', 'prompt') or target['output'] not in ('json', 'text'):
                raise ValueError('Invalid command input/output mode')
        elif adapter == 'openai-compatible':
            from urllib.parse import urlparse
            endpoint = urlparse(target.get('url', ''))
            if endpoint.scheme not in ('http', 'https') or not endpoint.hostname or endpoint.username or endpoint.password:
                raise ValueError('HTTP target requires a URL without embedded credentials')
            if set(target.get('capabilities', [])) - {'text'}:
                raise ValueError('Direct HTTP adapter supports text only; use a tool-capable harness for agents')
            if 'api_key_env' in target:
                identifier(target['api_key_env'])
        elif adapter != 'external':
            raise ValueError(f'Unknown adapter: {adapter}')
    task_ids = set()
    for task in tasks:
        if not isinstance(task, dict):
            raise ValueError('Task must be an object')
        tid = identifier(task['id'])
        if tid in task_ids:
            raise ValueError(f'Duplicate task: {tid}')
        task_ids.add(tid)
        if not isinstance(task.get('prompt'), str) or not task['prompt'].strip():
            raise ValueError('Task prompt cannot be empty')
        strings(task.setdefault('depends_on', []), 'dependencies')
        strings(task.setdefault('requires', []), 'task capabilities')
        strings(task.setdefault('targets', []), 'task targets')
        strings(task.setdefault('resources', []), 'exclusive resources')
        positive(task.setdefault('min_context_tokens', 1), 'min_context_tokens')
        if set(task['targets']) - ids:
            raise ValueError('Task names an unknown target')
        for flag in ('retry_safe', 'approved'):
            if not isinstance(task.setdefault(flag, False), bool):
                raise ValueError(f'{flag} must be boolean')
        maximum = task.setdefault('max_attempts', 3)
        if isinstance(maximum, bool) or not isinstance(maximum, int) or maximum < 1:
            raise ValueError('max_attempts must be a positive integer')
        cwd = (root / task.get('workspace', '.')).resolve()
        if not cwd.is_dir() or not cwd.is_relative_to(root):
            raise ValueError('Task workspace must exist within workflow root')
        task['workspace'] = str(cwd)
        verifies = task.setdefault('verify', [])
        if not isinstance(verifies, list):
            raise ValueError('verify must be an array of argv arrays')
        for argv in verifies:
            if not strings(argv, 'verification command'):
                raise ValueError('Verification command cannot be empty')
        if verifies and 'shell' not in auth['capabilities']:
            raise ValueError('Verification commands require authorized shell capability')
    graph = {t['id']: t['depends_on'] for t in tasks}
    visited, active = set(), set()
    def visit(node):
        if node not in graph:
            raise ValueError(f'Unknown dependency: {node}')
        if node in active:
            raise ValueError('Dependency cycle')
        if node in visited:
            return
        active.add(node)
        for parent in graph[node]:
            visit(parent)
        active.remove(node)
        visited.add(node)
    for tid in graph:
        visit(tid)
    return spec


def route(spec, task, excluded=()):
    auth = spec['authorization']
    needs = set(task['requires'])
    if not needs.issubset(auth['capabilities']):
        return []
    if auth['mode'] == 'supervised' and not task['approved']:
        return []
    return sorted((t for t in spec['targets']
                   if t['id'] not in excluded
                   and t['provider'] in auth['providers']
                   and set(t.get('capabilities', [])).issubset(auth['capabilities'])
                   and needs.issubset(t.get('capabilities', []))
                   and (task['min_context_tokens'] == 1 or t.get('context_tokens', 0) >= task['min_context_tokens'])
                   and (not task['targets'] or t['id'] in task['targets'])),
                  key=lambda t: (t['priority'], t['id']))


def validate_result(value):
    if not isinstance(value, dict) or value.get('version') != PROTOCOL_VERSION:
        raise ValueError('Worker result must be a version 1 object')
    if value.get('status') not in ('completed', 'failed', 'blocked'):
        raise ValueError('Invalid worker result status')
    if not isinstance(value.get('output'), str):
        raise ValueError('Worker output must be a string')
    strings(value.get('evidence', []), 'result evidence')
    return value
