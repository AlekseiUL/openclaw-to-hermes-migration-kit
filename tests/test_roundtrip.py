import json, os, pathlib, shutil, subprocess, sys, tempfile, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class Migration(unittest.TestCase):
    def test_dry_apply_conflict_rollback_and_secret_reference(self):
        with tempfile.TemporaryDirectory() as td:
            home=pathlib.Path(td).resolve(); src=home/'source'; src.mkdir()
            (src/'.env').write_text('API_TOKEN=synthetic-do-not-copy\n')
            env={**os.environ,'HOME':td}
            p=subprocess.run([sys.executable,str(ROOT/'scripts/openclaw_hermes_audit.py'),'--source',str(src)],env=env,capture_output=True,text=True,check=True)
            self.assertNotIn('synthetic-do-not-copy',p.stdout)
            self.assertEqual(json.loads(p.stdout)['env_keys'][0]['name'],'API_TOKEN')
            target=home/'target'
            command=[sys.executable,str(ROOT/'scripts/generate_profile_skeleton.py'),'--agent','test','--profile','test','--workspace-root',str(target)]
            subprocess.run(command,env=env,check=True,capture_output=True)
            self.assertFalse(target.exists())
            subprocess.run(command+['--apply'],env=env,check=True,capture_output=True)
            role=target/'test/RoleBrief.md'; role.write_text('user customization')
            snapshot=home/'snapshot'; shutil.copytree(target,snapshot)
            subprocess.run(command+['--apply'],env=env,check=True,capture_output=True)
            self.assertEqual(role.read_text(),'user customization')
            self.assertNotIn('synthetic-do-not-copy',''.join(p.read_text() for p in target.rglob('*') if p.is_file()))
            shutil.rmtree(target); shutil.copytree(snapshot,target)
            self.assertEqual(role.read_text(),'user customization')
            self.assertFalse((home/'.hermes').exists())
    def test_reject_escape_and_conflicting_modes(self):
        with tempfile.TemporaryDirectory() as td:
            base=[sys.executable,str(ROOT/'scripts/generate_profile_skeleton.py'),'--profile','test','--workspace-root',td]
            for flags in [['--agent','../escape'],['--agent','test','--apply','--dry-run']]:
                self.assertNotEqual(subprocess.run(base+flags,capture_output=True).returncode,0)
if __name__=='__main__': unittest.main()
