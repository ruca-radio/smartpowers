#!/usr/bin/env python3
"""Install portable skills with ownership tracking and recoverable upgrades."""
import argparse
import fcntl
import json
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BEGIN = '# >>> smartpowers >>>'
END = '# <<< smartpowers <<<'


def strip_block(text):
    if text.count(BEGIN) != text.count(END) or text.count(BEGIN) > 1:
        raise ValueError('Malformed managed preamble; repair markers before installation')
    return re.sub(r'(?m)^# >>> smartpowers >>>\n.*?^# <<< smartpowers <<<\n?', '', text, flags=re.S).rstrip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    profiles = parser.add_mutually_exclusive_group()
    for profile in ('kimi','claude','cursor'):
        profiles.add_argument('--'+profile, dest='profile', action='store_const', const=profile)
    parser.add_argument('--target', type=Path)
    parser.add_argument('--instructions', type=Path, help='Explicit global/project instruction file')
    parser.add_argument('--link', action='store_true')
    parser.add_argument('--uninstall', action='store_true')
    args = parser.parse_args()
    profile = args.profile or 'kimi'
    defaults = {'kimi':('.agents','AGENTS.md'),'claude':('.claude','CLAUDE.md'),'cursor':('.cursor',None)}
    directory, filename = defaults[profile]
    target = (args.target or Path.home()/directory/'skills').expanduser().resolve()
    if target == (ROOT/'skills').resolve() or target.is_relative_to(ROOT/'skills'):
        raise ValueError('Cannot install over the source skill tree')
    instructions = args.instructions
    if instructions is None and args.target is None and filename:
        instructions = Path.home()/directory/filename
    if instructions is not None:
        instructions = instructions.expanduser().resolve()
    target.mkdir(parents=True,exist_ok=True)
    with (target/'.smartpowers-install.lock').open('a+') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        install(target,instructions,args)


def install(target,instructions,args):
    manifest = target/'.smartpowers-manifest'
    old = {'version':2,'skills':[],'instructions':None}
    if manifest.exists():
        text = manifest.read_text()
        if text.lstrip().startswith('{'):
            old = json.loads(text)
            if old.get('version') != 2:
                raise ValueError('Unsupported install manifest version')
        else:
            old['skills'] = text.splitlines()
    if any(not re.fullmatch(r'[a-z0-9-]+', name) for name in old['skills']):
        raise ValueError('Invalid name in install manifest')
    if instructions is None and old.get('instructions'):
        instructions = Path(old['instructions'])
    if old.get('instructions') and instructions and Path(old['instructions']) != instructions:
        raise ValueError('Uninstall the previous instruction-file binding before changing it')
    previous = instructions.read_text() if instructions and instructions.exists() else ''
    existed = bool(instructions and instructions.exists())
    cleaned = strip_block(previous)
    names = sorted(p.name for p in (ROOT/'skills').iterdir() if p.is_dir())
    if not args.uninstall:
        subprocess.run([sys.executable,str(ROOT/'skills/writing-skills/scripts/skill-lint'),str(ROOT/'skills')],check=True)
        for name in names:
            dest = target/name
            if (dest.exists() or dest.is_symlink()) and name not in old['skills']:
                raise ValueError(f'Refusing to overwrite unmanaged skill: {dest}')
    affected = sorted(set(old['skills']) | (set(names) if not args.uninstall else set()))
    backup = target/'.smartpowers-backups'/uuid.uuid4().hex
    backup.mkdir(parents=True)
    if manifest.exists():
        shutil.copy2(manifest,backup/'manifest')
    if existed:
        (backup/'instructions.txt').write_text(previous)
    staged = Path(tempfile.mkdtemp(prefix='.smartpowers-stage-',dir=target))
    moved, installed = [], []
    try:
        if not args.uninstall:
            for name in names:
                src, dst = ROOT/'skills'/name, staged/name
                if args.link:
                    dst.symlink_to(src,target_is_directory=True)
                else:
                    shutil.copytree(src,dst,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
                    for script in (dst/'scripts').glob('*'):
                        if script.is_file():
                            script.chmod(script.stat().st_mode | 0o111)
        for name in affected:
            dest = target/name
            if dest.exists() or dest.is_symlink():
                dest.rename(backup/name); moved.append(name)
        if not args.uninstall:
            for name in names:
                (staged/name).rename(target/name); installed.append(name)
        if instructions:
            instructions.parent.mkdir(parents=True,exist_ok=True)
            updated = cleaned+'\n' if cleaned else ''
            if not args.uninstall:
                snippet=(ROOT/'preamble/AGENTS.snippet.md').read_text().replace('__SKILLS_DIR__',str(target)).strip()
                updated += '\n'+BEGIN+'\n'+snippet+'\n'+END+'\n'
            tmp=instructions.with_name(instructions.name+'.smartpowers-'+uuid.uuid4().hex)
            tmp.write_text(updated)
            if instructions.exists():
                tmp.chmod(instructions.stat().st_mode & 0o777)
            tmp.replace(instructions)
        if args.uninstall:
            manifest.unlink(missing_ok=True)
        else:
            staged_manifest=staged/'manifest'
            staged_manifest.write_text(json.dumps({'version':2,'skills':names,'instructions':str(instructions) if instructions else None},indent=2)+'\n')
            staged_manifest.replace(manifest)
    except BaseException:
        for name in installed:
            dest=target/name
            if dest.is_symlink(): dest.unlink()
            elif dest.exists(): shutil.rmtree(dest)
        for name in moved:
            (backup/name).rename(target/name)
        if instructions:
            if existed: instructions.write_text(previous)
            elif instructions.exists(): instructions.unlink()
        raise
    finally:
        shutil.rmtree(staged)
    print(f'Smartpowers {"uninstalled" if args.uninstall else "installed"}: {target}')
    print(f'Previous files retained: {backup}')
    if not instructions and not args.uninstall:
        print('Add preamble/AGENTS.snippet.md to the harness instructions; replace __SKILLS_DIR__ with the target path.')


if __name__=='__main__':
    try:
        main()
    except (ValueError,OSError,subprocess.CalledProcessError) as exc:
        print(f'install: {exc}',file=sys.stderr)
        raise SystemExit(1)
