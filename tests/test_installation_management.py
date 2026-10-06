"""Exercise actual installation, local edits, recovery and scoped destinations."""
import importlib.util
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('nps_install', ROOT / 'scripts/manage_install.py')
manager = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(manager)


class InstallationManagementTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='nps test ')
        self.base = Path(self.temp.name)
        self.dest = self.base / 'skills'
        self.source = self.base / 'source'
        self.skill = self.source / 'skills/core/demo'
        self.skill.mkdir(parents=True)
        (self.skill / 'SKILL.md').write_text('---\nname: demo\ndescription: A demo.\n---\nOriginal.\n')
        (self.source / 'VERSION').write_text('0.2.0\n')
        (self.source / 'LICENSE-APACHE').write_text('Apache license fixture\n')
        (self.source / 'NOTICE').write_text('Notice fixture\n')

    def tearDown(self):
        self.temp.cleanup()

    def args(self, *extra):
        return [sys.executable, str(ROOT/'scripts/manage_install.py'), '--source', str(self.source),
                '--dest', str(self.dest), '--skill', 'core/demo', '--apache', 'core/demo',
                '--source-ref', 'test', '--commit', 'a'*40, *extra]

    def run_manager(self, *extra, code=0):
        r = subprocess.run(self.args(*extra), text=True, capture_output=True)
        self.assertEqual(r.returncode, code, r.stdout+r.stderr)
        return r

    def manifest(self):
        return json.loads((self.dest/manager.STATE/'installed.json').read_text())

    def backups(self):
        root = self.dest/manager.STATE/'backups'
        return [p for p in sorted(root.glob('*')) if (p/'demo').exists()]

    def test_install_doctor_and_licenses(self):
        self.run_manager()
        self.assertEqual((self.dest/'demo/LICENSE-APACHE').read_text(), 'Apache license fixture\n')
        self.assertEqual((self.dest/'demo/NOTICE').read_text(), 'Notice fixture\n')
        self.assertEqual(self.manifest()['skills']['demo']['commit'], 'a'*40)
        self.run_manager('--doctor')

    def test_unchanged_install_is_idempotent(self):
        self.run_manager()
        before = self.manifest()
        self.run_manager()
        self.assertEqual(self.manifest(), before)
        self.assertEqual(self.backups(), [])

    def test_local_edit_is_backed_up_and_restored(self):
        self.run_manager()
        target = self.dest/'demo/SKILL.md'
        target.write_text(target.read_text()+'Local note.\n')
        self.run_manager('--doctor', code=1)
        self.run_manager()
        backup = self.backups()[-1]
        self.assertIn('Local note.', (backup/'demo/SKILL.md').read_text())
        self.assertNotIn('Local note.', target.read_text())
        self.run_manager('--restore', backup.name)
        self.assertIn('Local note.', target.read_text())
        self.assertGreaterEqual(len(self.backups()), 2)

    def make_restore_backup(self):
        self.run_manager()
        target = self.dest/'demo/SKILL.md'
        target.write_text(target.read_text()+'Local note.\n')
        self.run_manager()
        return self.backups()[-1]

    def link_current_skill(self, dest, relative=True):
        canonical = self.base/(dest.name+'-canonical')/'demo'
        canonical.parent.mkdir()
        (dest/'demo').rename(canonical)
        value = os.path.relpath(canonical, dest) if relative else str(canonical)
        (dest/'demo').symlink_to(value, target_is_directory=True)
        return canonical

    def test_restore_refuses_relative_and_absolute_current_links(self):
        backup = self.make_restore_backup()
        canonical = self.link_current_skill(self.dest)
        before = self.manifest()
        count = len(self.backups())
        for value in (os.readlink(self.dest/'demo'), str(canonical)):
            # Alter only our scratch symlink, preserving its canonical directory.
            if os.readlink(self.dest/'demo') != value:
                alternate = self.dest/'alternate'
                alternate.symlink_to(value, target_is_directory=True)
                os.replace(alternate, self.dest/'demo')
            result = self.run_manager('--restore', backup.name, code=2)
            self.assertIn('Refusing to replace linked skill', result.stderr)
            self.assertEqual(os.readlink(self.dest/'demo'), value)
            self.assertTrue((self.dest/'demo/SKILL.md').is_file())
            self.assertTrue((canonical/'SKILL.md').is_file())
            self.assertEqual(self.manifest(), before)
            self.assertEqual(len(self.backups()), count)

    def test_restore_preflights_all_destinations_before_replacing_any(self):
        backup = self.make_restore_backup()
        second = self.base/'second'
        shutil.copytree(self.dest, second)
        self.link_current_skill(second)
        before = (self.dest/'demo/SKILL.md').read_bytes()
        manifest = self.manifest()
        result = self.run_manager('--dest', str(second), '--restore', backup.name, code=2)
        self.assertIn('Refusing to replace linked skill', result.stderr)
        self.assertEqual((self.dest/'demo/SKILL.md').read_bytes(), before)
        self.assertEqual(self.manifest(), manifest)
        self.assertTrue((second/'demo').is_symlink())

    def test_restore_refuses_linked_backup(self):
        backup = self.make_restore_backup()
        canonical = self.base/'backup-canonical'
        (backup/'demo').rename(canonical)
        (backup/'demo').symlink_to(os.path.relpath(canonical, backup), target_is_directory=True)
        result = self.run_manager('--restore', backup.name, code=2)
        self.assertIn('linked backup', result.stderr)
        self.assertTrue((backup/'demo/SKILL.md').is_file())

    def test_keep_and_error_preserve_local_edits(self):
        self.run_manager()
        target = self.dest/'demo/SKILL.md'
        target.write_text(target.read_text()+'Custom.\n')
        self.run_manager('--on-conflict', 'keep')
        self.assertIn('Custom.', target.read_text())
        self.run_manager('--on-conflict', 'error', code=2)
        self.assertIn('Custom.', target.read_text())

    def test_dry_run_writes_nothing(self):
        self.run_manager('--dry-run')
        self.assertFalse(self.dest.exists())

    def test_unmanaged_copy_is_preserved(self):
        target = self.dest/'demo'
        target.mkdir(parents=True)
        (target/'SKILL.md').write_text('My unrelated skill')
        self.run_manager()
        self.assertEqual((self.backups()[-1]/'demo/SKILL.md').read_text(), 'My unrelated skill')

    def test_non_skill_directory_blocks_all_destinations(self):
        blocked = self.base/'blocked'
        (blocked/'demo').mkdir(parents=True)
        self.run_manager('--dest', str(blocked), code=2)
        self.assertFalse((self.dest/'demo').exists())

    def test_deleted_upstream_file_does_not_linger(self):
        (self.skill/'obsolete.txt').write_text('old')
        self.run_manager()
        (self.skill/'obsolete.txt').unlink()
        self.run_manager()
        self.assertFalse((self.dest/'demo/obsolete.txt').exists())
        self.assertTrue((self.backups()[-1]/'demo/obsolete.txt').exists())

    def test_bytecode_is_not_shipped(self):
        (self.skill/'__pycache__').mkdir()
        (self.skill/'__pycache__/x.pyc').write_bytes(b'junk')
        self.run_manager()
        self.assertFalse((self.dest/'demo/__pycache__').exists())

    def test_missing_license_does_not_replace_install(self):
        self.run_manager()
        before = (self.dest/'demo/SKILL.md').read_text()
        (self.source/'NOTICE').unlink()
        self.run_manager(code=2)
        self.assertEqual((self.dest/'demo/SKILL.md').read_text(), before)

    def test_missing_file_is_reported(self):
        self.run_manager()
        (self.dest/'demo/SKILL.md').unlink()
        self.run_manager('--doctor', code=1)

    def test_failed_swap_rolls_back_previous_copy(self):
        self.run_manager()
        before = (self.dest/'demo/SKILL.md').read_text()
        (self.skill/'SKILL.md').write_text('New version')
        real_replace = manager.os.replace
        def fail_new_payload(src, dst):
            if Path(src).parent.name.startswith('stage-') and Path(dst).resolve() == (self.dest/'demo').resolve():
                raise OSError('simulated disk failure')
            return real_replace(src,dst)
        with patch.object(sys, 'argv', self.args()[1:]), patch.object(manager.os, 'replace', side_effect=fail_new_payload):
            self.assertEqual(manager.main(), 2)
        self.assertEqual((self.dest/'demo/SKILL.md').read_text(), before)
        self.run_manager('--doctor')

    def test_invalid_backup_id_cannot_escape_backup_root(self):
        self.run_manager()
        self.run_manager('--restore', '../../elsewhere', code=2)

    def test_symlinked_management_area_is_rejected(self):
        self.dest.mkdir()
        elsewhere = self.base/'elsewhere'
        elsewhere.mkdir()
        (self.dest/manager.STATE).symlink_to(elsewhere, target_is_directory=True)
        self.run_manager(code=2)
        self.assertEqual(list(elsewhere.iterdir()), [])

    def test_linked_skill_is_rejected_by_default_before_any_destination_changes(self):
        self.run_manager()
        before = (self.dest/'demo/SKILL.md').read_text()
        manifest_before = (self.dest/manager.STATE/'installed.json').read_bytes()
        (self.skill/'SKILL.md').write_text('New upstream version')
        blocked = self.base/'linked-agent'
        blocked.mkdir()
        link = blocked/'demo'
        link.symlink_to(self.skill, target_is_directory=True)

        result = self.run_manager('--dest', str(blocked), code=2)

        self.assertIn('Refusing to replace linked skill', result.stderr)
        self.assertIn(str(self.skill.resolve()), result.stderr)
        self.assertIn('canonical installation', result.stderr)
        self.assertEqual((self.dest/'demo/SKILL.md').read_text(), before)
        self.assertEqual((self.dest/manager.STATE/'installed.json').read_bytes(), manifest_before)
        self.assertTrue(link.is_symlink())
        self.assertEqual(os.readlink(link), str(self.skill))
        self.assertEqual((self.skill/'SKILL.md').read_text(), 'New upstream version')
        self.assertFalse((blocked/manager.STATE).exists())
        self.assertEqual(self.backups(), [])

    def test_backup_and_error_policies_do_not_replace_relative_links(self):
        self.dest.mkdir()
        link = self.dest/'demo'
        referent = '../source/skills/core/demo'
        link.symlink_to(referent, target_is_directory=True)

        for policy in ('backup', 'error'):
            for dry_run in (False, True):
                with self.subTest(policy=policy, dry_run=dry_run):
                    flags = ('--dry-run',) if dry_run else ()
                    result = self.run_manager('--on-conflict', policy, *flags, code=2)
                    self.assertIn('Refusing to replace linked skill', result.stderr)
                    self.assertTrue(link.is_symlink())
                    self.assertEqual(os.readlink(link), referent)
                    self.assertTrue((link/'SKILL.md').is_file())
                    self.assertFalse((self.dest/manager.STATE).exists())

    def test_keep_preserves_valid_link_without_adopting_it(self):
        self.dest.mkdir()
        link = self.dest/'demo'
        link.symlink_to(self.skill, target_is_directory=True)
        before = (self.skill/'SKILL.md').read_bytes()

        result = self.run_manager('--on-conflict', 'keep')

        self.assertIn('Kept linked skill', result.stdout)
        self.assertIn('not verified', result.stdout)
        self.assertTrue(link.is_symlink())
        self.assertEqual((self.skill/'SKILL.md').read_bytes(), before)
        self.assertFalse((self.dest/manager.STATE).exists())

    def test_broken_link_is_protected_and_can_be_kept(self):
        self.dest.mkdir()
        link = self.dest/'demo'
        missing = self.base/'missing-canonical/demo'
        link.symlink_to(missing, target_is_directory=True)

        rejected = self.run_manager(code=2)
        self.assertIn('Refusing to replace linked skill', rejected.stderr)
        kept = self.run_manager('--on-conflict', 'keep')
        self.assertIn('Kept linked skill', kept.stdout)
        self.assertTrue(link.is_symlink())
        self.assertEqual(os.readlink(link), str(missing))
        self.assertFalse(missing.exists())
        self.assertFalse((self.dest/manager.STATE).exists())

    def test_dry_run_keep_preserves_link_and_writes_nothing(self):
        self.dest.mkdir()
        link = self.dest/'demo'
        link.symlink_to('../missing/demo', target_is_directory=True)

        result = self.run_manager('--on-conflict', 'keep', '--dry-run')

        self.assertIn('Would keep', result.stdout)
        self.assertTrue(link.is_symlink())
        self.assertEqual(os.readlink(link), '../missing/demo')
        self.assertFalse((self.dest/manager.STATE).exists())

    def test_kept_link_with_previous_copy_record_is_not_verified_as_managed_copy(self):
        self.run_manager()
        previous = self.base/'previous-copy'
        (self.dest/'demo').rename(previous)
        link = self.dest/'demo'
        link.symlink_to(previous, target_is_directory=True)
        manifest_before = (self.dest/manager.STATE/'installed.json').read_bytes()

        self.run_manager('--on-conflict', 'keep')
        result = self.run_manager('--doctor', code=1)

        self.assertIn('LINKED (not verified here)', result.stdout)
        self.assertNotIn('OK demo', result.stdout)
        self.assertTrue(link.is_symlink())
        self.assertEqual((self.dest/manager.STATE/'installed.json').read_bytes(), manifest_before)

    def test_symlink_loop_has_a_safe_diagnostic(self):
        self.dest.mkdir()
        link = self.dest/'demo'
        link.symlink_to('demo', target_is_directory=True)

        rejected = self.run_manager(code=2)
        self.assertIn('Refusing to replace linked skill', rejected.stderr)
        self.run_manager('--on-conflict', 'keep')
        doctor = self.run_manager('--doctor', code=1)
        self.assertIn('INVALID_LINK', doctor.stdout)
        self.assertTrue(link.is_symlink())
        self.assertEqual(os.readlink(link), 'demo')
        self.assertFalse((self.dest/manager.STATE).exists())

    def test_doctor_labels_valid_link_without_verifying_it(self):
        self.dest.mkdir()
        link = self.dest/'demo'
        link.symlink_to(self.skill, target_is_directory=True)

        result = self.run_manager('--doctor', code=1)

        self.assertIn('LINKED (not verified here)', result.stdout)
        self.assertIn(str(self.skill.resolve()), result.stdout)
        self.assertIn('canonical installation directory', result.stdout)
        self.assertNotIn('OK demo', result.stdout)
        self.assertFalse((self.dest/manager.STATE).exists())

    def test_doctor_labels_broken_link_without_changing_it(self):
        self.dest.mkdir()
        link = self.dest/'demo'
        link.symlink_to('../missing/demo', target_is_directory=True)

        result = self.run_manager('--doctor', code=1)

        self.assertIn('INVALID_LINK (not verified here)', result.stdout)
        self.assertNotIn('OK demo', result.stdout)
        self.assertTrue(link.is_symlink())
        self.assertEqual(os.readlink(link), '../missing/demo')
        self.assertFalse((self.dest/manager.STATE).exists())

    def test_keep_link_still_installs_other_skills_without_recording_link_ownership(self):
        other = self.source/'skills/core/other'
        other.mkdir()
        (other/'SKILL.md').write_text('---\nname: other\ndescription: Other.\n---\n')
        self.dest.mkdir()
        link = self.dest/'demo'
        link.symlink_to(self.skill, target_is_directory=True)

        self.run_manager('--on-conflict', 'keep', '--skill', 'core/other')

        self.assertTrue(link.is_symlink())
        self.assertTrue((self.dest/'other/SKILL.md').is_file())
        self.assertEqual(set(self.manifest()['skills']), {'other'})

    def test_linked_destination_root_is_still_supported(self):
        self.dest.mkdir()
        alias = self.base/'linked-root'
        alias.symlink_to(self.dest, target_is_directory=True)

        self.run_manager('--dest', str(alias))

        self.assertTrue(alias.is_symlink())
        self.assertFalse((self.dest/'demo').is_symlink())
        self.assertTrue((alias/'demo/SKILL.md').is_file())
        self.run_manager('--dest', str(alias), '--doctor')

    def test_canonical_updates_remain_visible_through_agent_link(self):
        self.run_manager()
        agent = self.base/'agent'
        agent.mkdir()
        link = agent/'demo'
        link.symlink_to(self.dest/'demo', target_is_directory=True)
        (self.skill/'SKILL.md').write_text('Updated canonical version')

        self.run_manager()

        self.assertTrue(link.is_symlink())
        self.assertEqual((link/'SKILL.md').read_text(), 'Updated canonical version')
        self.run_manager('--doctor')

    def test_codex_and_claude_project_local_install(self):
        result = subprocess.run(['bash', str(ROOT/'install.sh'), '--agent', 'both', '--local'],
                                cwd=self.base, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        for target in (self.base/'.agents/skills', self.base/'.claude/skills'):
            self.assertEqual(len(list(target.glob('*/SKILL.md'))),19)
            self.assertTrue((target/'paper-reviewer/SKILL.md').exists())

    def test_existing_temporary_symlink_never_overwrites_its_target(self):
        state = self.dest/manager.STATE
        state.mkdir(parents=True)
        external = self.base/'external.txt'
        external.write_text('Preserve this file')
        link = state/'installed.json.tmp'
        link.symlink_to(external)
        self.run_manager()
        self.assertEqual(external.read_text(), 'Preserve this file')
        self.assertTrue(link.is_symlink())
        self.assertFalse((state/'installed.json').is_symlink())
        self.run_manager('--doctor')

    def test_dangling_temporary_symlink_does_not_create_external_file(self):
        state = self.dest/manager.STATE
        state.mkdir(parents=True)
        external = self.base/'missing.txt'
        (state/'installed.json.tmp').symlink_to(external)
        self.run_manager()
        self.assertFalse(external.exists())
        self.run_manager('--doctor')

    def test_failed_metadata_replace_preserves_record_and_cleans_temporary_file(self):
        path = self.base/'record.json'
        path.write_text('{"original": true}\n')
        with patch.object(manager.os, 'replace', side_effect=OSError('disk failure')):
            with self.assertRaises(OSError):
                manager.write_json(path, {'new': True})
        self.assertEqual(json.loads(path.read_text()), {'original': True})
        self.assertEqual(list(self.base.glob('.record.json-*.tmp')), [])

class RemoteInstallerTests(unittest.TestCase):
    """Exercise curl|bash and pinned-download plumbing with a local HTTP fixture substitute."""
    def setUp(self):
        import tarfile
        self.temp = tempfile.TemporaryDirectory(prefix='nps-remote-')
        self.base = Path(self.temp.name)
        self.archive = self.base/'source.tar.gz'
        with tarfile.open(self.archive,'w:gz') as archive:
            for name in ('skills','scripts','VERSION','LICENSE-APACHE','NOTICE'):
                archive.add(ROOT/name, arcname='snapshot/'+name, filter=lambda item: None if '__pycache__' in item.name else item)
        self.bin = self.base/'bin'
        self.bin.mkdir()
        curl = self.bin/'curl'
        curl.write_text('#!'+sys.executable+'\n'+
            'import sys,shutil,os,json\n'+
            "args=sys.argv[1:]; url=args[-1]\n"+
            "if '/commits/' in url:\n"+
            " if os.environ.get('NPS_TEST_LOOKUP_FAIL'): sys.exit(22)\n"+
            " print(json.dumps({'sha':'a'*40}))\n"+
            "else:\n"+
            ' shutil.copyfile('+repr(str(self.archive))+",args[args.index('-o')+1])\n")
        curl.chmod(0o755)
        self.env = dict(os.environ)
        self.env['PATH'] = str(self.bin)+os.pathsep+self.env['PATH']
        self.dest = self.base/'installed'

    def tearDown(self):
        self.temp.cleanup()

    def run_pipe(self, ref):
        result = subprocess.run(['bash','-s','--','--dest',str(self.dest),'--ref',ref],
            input=(ROOT/'install.sh').read_text(), text=True, capture_output=True,
            env=self.env,cwd=self.base)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        return result

    def test_pipe_records_resolved_commit_and_installs_reviewer(self):
        self.run_pipe('main')
        record=json.loads((self.dest/manager.STATE/'installed.json').read_text())
        self.assertEqual(record['skills']['paper-workflow']['commit'],'a'*40)
        self.assertTrue((self.dest/'paper-reviewer/SKILL.md').is_file())

    def test_unresolved_branch_is_not_mislabeled_as_commit(self):
        self.env['NPS_TEST_LOOKUP_FAIL']='1'
        result=self.run_pipe('main')
        record=json.loads((self.dest/manager.STATE/'installed.json').read_text())
        self.assertIsNone(record['skills']['paper-workflow']['commit'])
        self.assertIn('lookup unavailable',result.stderr)


if __name__ == '__main__':
    unittest.main()
