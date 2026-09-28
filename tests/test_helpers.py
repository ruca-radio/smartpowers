import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HELPERS = REPO / 'skills/subagent-driven-development/scripts'


class HelperTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.run_git('init','-q')
        self.run_git('config','user.name','Test')
        self.run_git('config','user.email','test@example.invalid')
        (self.root/'seed').write_text('seed')
        self.run_git('add','seed'); self.run_git('commit','-qm','seed')

    def tearDown(self):
        self.tmp.cleanup()

    def run_git(self,*args):
        return subprocess.check_output(['git',*args],cwd=self.root,text=True).strip()

    def helper(self,name,*args):
        return subprocess.check_output(['python3',str(HELPERS/name),*args],cwd=self.root,text=True).strip()

    def test_workspace_does_not_commit_or_modify_index(self):
        (self.root/'plan.md').write_text('plan')
        (self.root/'unrelated').write_text('unrelated')
        self.run_git('add','unrelated')
        head = self.run_git('rev-parse','HEAD')
        index = self.run_git('diff','--cached')
        self.helper('sdd-workspace','plan.md')
        self.assertEqual(head,self.run_git('rev-parse','HEAD'))
        self.assertEqual(index,self.run_git('diff','--cached'))

    def test_identity_and_explicit_new_run(self):
        for parent in ('a','b'):
            (self.root/parent).mkdir(); (self.root/parent/'plan.md').write_text('plan')
        first = self.helper('sdd-workspace','a/plan.md')
        self.assertEqual(first,self.helper('sdd-workspace','a/plan.md'))
        self.assertNotEqual(first,self.helper('sdd-workspace','b/plan.md'))
        self.assertNotEqual(first,self.helper('sdd-workspace','a/plan.md','--new'))

    def test_task_parser_retains_nested_headings_and_fenced_text(self):
        (self.root/'plan.md').write_text('### Task 1: First\n#### Steps\n~~~~md\n### Task 2: fake\n~~~~\nkeep\n### Task 2: Actual\nexclude\n')
        result = Path(self.helper('task-brief','plan.md','1')).read_text()
        self.assertIn('#### Steps',result)
        self.assertIn('keep',result)
        self.assertNotIn('exclude',result)

    def test_changed_plan_gets_new_workspace(self):
        plan = self.root/'plan.md'; plan.write_text('v1')
        first = self.helper('sdd-workspace','plan.md')
        plan.write_text('v2')
        self.assertNotEqual(first,self.helper('sdd-workspace','plan.md'))


class InstallerTests(unittest.TestCase):
    def test_custom_target_link_upgrade_and_uninstall_preserve_unmanaged_files(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t); target = root/'skills'; instructions=root/'INSTRUCTIONS.md'
            instructions.write_text('User rules\n')
            base = ['bash',str(REPO/'install.sh'),'--target',str(target),'--instructions',str(instructions)]
            subprocess.run(base,check=True,capture_output=True)
            self.assertTrue((target/'using-smartpowers/SKILL.md').is_file())
            subprocess.run(base+['--link'],check=True,capture_output=True)
            self.assertTrue((target/'using-smartpowers').is_symlink())
            self.assertEqual(instructions.read_text().count('# >>> smartpowers >>>'),1)
            (target/'unmanaged').mkdir()
            subprocess.run(base+['--uninstall'],check=True,capture_output=True)
            self.assertTrue((target/'unmanaged').is_dir())
            self.assertEqual(instructions.read_text(),'User rules\n')

    def test_unmanaged_name_collision_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as t:
            target=Path(t)/'skills'; existing=target/'brainstorming'
            existing.mkdir(parents=True); (existing/'mine').write_text('mine')
            result=subprocess.run(['bash',str(REPO/'install.sh'),'--target',str(target)],capture_output=True)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual((existing/'mine').read_text(),'mine')


if __name__=='__main__':
    unittest.main()
