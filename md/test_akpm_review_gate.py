#!/usr/bin/env python3
"""Behavioral regressions for the chat-local AKPM review evidence gate v2."""
import hashlib
import json
import importlib.util
from types import SimpleNamespace
import os
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().with_name('akpm-review-gate.py')
WORKFLOW = pathlib.Path(__file__).resolve().with_name('akpm-patch-review-workflow.md')
R034 = pathlib.Path(__file__).resolve() / '..' / 'Pasted text(20261023-231457).txt'
R034 = R034.resolve()
CONFLICT = pathlib.Path(__file__).resolve().with_name('r034-tejun-audit') / 'type-conflict.c'


def invoke(*args, cwd=None):
    if os.environ.get("DEBUG_GATE"):
        print("CALL", str(args[:9])[:220], flush=True)
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], cwd=cwd,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          text=True, check=False, timeout=60)


class GateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.dir = pathlib.Path(self.tmp.name)
        self.wf = self.dir/'workflow.md'
        self.wf.write_bytes(WORKFLOW.read_bytes())
        self.manifest = self.dir/'review.json'

    def new(self, patch=R034, review='R-034-check'):
        r = invoke('new','--patch',patch,'--workflow',self.wf,'--manifest',self.manifest,
                   '--review-id',review,'--source-ref','a'*40)
        self.assertEqual(r.returncode, 0, r.stdout+r.stderr)
        return json.loads(self.manifest.read_text())

    def check(self):
        return invoke('check','--manifest',self.manifest)

    def test_r034_auto_discovery(self):
        m = self.new()
        gates = m['plan']['requirements']
        self.assertIn('shared_header_abi', gates)
        self.assertIn('external_consumer_build', gates)
        self.assertIn('test_matrix', gates)
        self.assertEqual(len(m['hunks']), 74)
        self.assertIn('cg_check_freezetime',m['plan']['classification']['symbols'])
        self.assertIn('cg_read_key_long',m['plan']['classification']['symbols'])
        self.assertNotIn('functions',m['plan']['classification']['symbols'])
        self.assertEqual(self.check().returncode,2)

    def test_no_preflight_overwrite(self):
        self.new()
        again = invoke('new','--patch',R034,'--workflow',self.wf,'--manifest',self.manifest,
                       '--review-id','R-034','--source-ref','a'*40)
        self.assertNotEqual(again.returncode,0)
        self.assertIn('refusing to overwrite',again.stderr)

    def test_plan_tamper_and_workflow_tamper(self):
        obj=self.new()
        obj['plan']['requirements'].pop('external_consumer_build')
        self.manifest.write_text(json.dumps(obj))
        self.assertIn('HOLD',self.check().stdout)
        self.assertIn('digest changed',self.check().stdout)
        self.new_manif = self.dir/'fresh.json'
        c=invoke('new','--patch',R034,'--workflow',self.wf,'--manifest',self.new_manif,
                 '--review-id','fresh','--source-ref','a'*40)
        self.assertEqual(c.returncode,0)
        self.wf.write_text(self.wf.read_text()+'\nNew unrelated text.\n')
        result=invoke('check','--manifest',self.new_manif)
        self.assertEqual(result.returncode,2)
        self.assertIn('workflow changed',result.stdout)

    def test_unrelated_command_rejected(self):
        self.new()
        for purpose, gate in [('whole-tree-search','cross_tree_consumers'),
                              ('consumer-build','external_consumer_build'),
                              ('abi-lp64','shared_header_abi')]:
            result=invoke('run','--manifest',self.manifest,'--gate',gate,'--purpose',purpose,
                          '--scope','whole-tree','--subject','main', '--','true')
            self.assertNotEqual(result.returncode,0)
            self.assertIn('HOLD',result.stderr)
        self.assertEqual(self.check().returncode,2)

    def test_report_without_gate_marker_rejected(self):
        self.new()
        report=self.dir/'generic.md'
        report.write_text('Good review overall. '*35)
        msg='I examined the source and did not find a material issue in these particular call paths.'
        r=invoke('report','--manifest',self.manifest,'--gate','all_callers',
                 '--file',report,'--claim',msg)
        self.assertNotEqual(r.returncode,0)
        self.assertIn('lacks an explicitly identified',r.stderr)

    def test_r034_failed_compiler_is_hold(self):
        self.new()
        output=self.dir/'bad.o'
        r=invoke('run','--manifest',self.manifest,'--gate','shared_header_abi',
                 '--purpose','abi-lp64','--scope','LP64', '--',
                 'gcc','-m64','-c',CONFLICT,'-o',output)
        self.assertEqual(r.returncode,1, r.stdout+r.stderr)
        self.assertIn('FAIL',r.stdout)
        self.assertIn('executed command failed',self.check().stdout)
        receipts=json.loads(self.manifest.read_text())['checks']['shared_header_abi']
        self.assertEqual(receipts[-1]['exit'],1)
        self.assertIn('conflicting types',pathlib.Path(receipts[-1]['file']['path']).read_text())

    def test_adversarial_is_distinct_and_hunk_receipts_required(self):
        self.new()
        report=self.dir/'adversarial.md'
        report.write_text('GATE:adversarial_second_pass\n' +
                          'An ordinary summary with no actual attempt to challenge findings. '*8)
        claim='I performed a distinct attempt to falsify the patch safety argument, using multiple paths.'
        bad=invoke('report','--manifest',self.manifest,'--gate','adversarial_second_pass',
                   '--file',report,'--claim',claim,'--provenance','same-model-adversarial')
        self.assertNotEqual(bad.returncode,0)
        report.write_text(report.read_text()+'\nChallenge: a discarded hypothesis.\nAttempt: test alternate state.\nResult: not reproduced.\n')
        okay=invoke('report','--manifest',self.manifest,'--gate','adversarial_second_pass',
                   '--file',report,'--claim',claim,'--provenance','same-model-adversarial')
        self.assertEqual(okay.returncode,0,okay.stderr)
        self.assertEqual(self.check().returncode,2)


    def test_unrelated_standing_section_citation_rejected(self):
        self.new()
        reason='This stage was examined against the matching source and all known producers and consumers.'
        bad=invoke('section','--manifest',self.manifest,'--id','S03','--status','APPLIED',
                   '--gate','independent_source_pass','--reason',reason)
        self.assertNotEqual(bad.returncode,0)
        self.assertIn('needs gate tejun_method',bad.stderr)
    def test_synthetic_positive_and_late_evidence_mutation(self):
        spec=importlib.util.spec_from_file_location("akpm_gate",SCRIPT)
        gate_module=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gate_module)
        # Demonstrates the *structural* upper outcome, not source correctness.
        repo=self.dir/'tree';repo.mkdir()
        def sh(*cmd):
            return subprocess.run(cmd,cwd=repo,text=True,capture_output=True,check=True)
        sh('git','init','-q')
        sh('git','config','user.email','test@example.com')
        sh('git','config','user.name','Test')
        (repo/'count.c').write_text('int count(void) { return 1; }\n')
        (repo/'Makefile').write_text('test:\n\t$(CC) -Wall -c count.c -o count.o\n# Makefile count\n')
        sh('git','add','.')
        sh('git','commit','-qm','preimage')
        sha=sh('git','rev-parse','HEAD').stdout.strip()
        (repo/'count.c').write_text('int count(void) { return 2; }\n')
        patch=self.dir/'example.patch';patch.write_text(sh('git','diff').stdout)
        sh('git','checkout','--','count.c')
        init=invoke('new','--patch',patch,'--workflow',self.wf,'--manifest',self.manifest,
                    '--review-id','R-999','--source-ref',sha)
        self.assertEqual(init.returncode,0,init.stderr)
        self.assertEqual(self.check().returncode,2)
        data=json.loads(self.manifest.read_text())
        req=data['plan']['requirements']
        report=self.dir/'checks.md'
        report.write_text(('Testing purpose-specific and evidence-anchored review records.\n'*12) +
                          ''.join('GATE:'+gate+'\n' for gate in req) + 'HUNK:H001\n')
        claim='I inspected the exact source and its error, caller, and build context and recorded the applicable reason.'
        for gate,purposes in req.items():
            if gate in ('all_hunks','standing_rule_inventory','adversarial_second_pass'):
                continue
            if 'analysis' in purposes:
                gate_module.report(SimpleNamespace(manifest=self.manifest,gate=gate,file=report,
                                                  claim=claim,provenance='same-model'))
        adv=self.dir/'adversarial.md'
        adv.write_text('GATE:adversarial_second_pass\n'+'Detailed counterfactual source hypothesis. '*10 +
                       '\nChallenge: stale callsites.\nAttempt: inspect alternate callers.\nResult: none found.\n')
        gate_module.report(SimpleNamespace(manifest=self.manifest,gate='adversarial_second_pass',
                                           file=adv,claim=claim,provenance='same-model-adversarial'))
        gate_module.hunk(SimpleNamespace(manifest=self.manifest,id='H001',file='count.c',
                                         report=report,note=claim))
        def run_gate(gate,purpose,scope,subject,argv):
            gate_module.run(SimpleNamespace(manifest=self.manifest,gate=gate,purpose=purpose,
                                            scope=scope,subject=subject,cwd=str(repo),
                                            timeout=20,command=['--']+argv))
        gate_module.inspect(SimpleNamespace(manifest=self.manifest,gate='base_and_preimage',
                                            repo=str(repo),path='count.c',line=1,note=claim))
        run_gate('base_and_preimage','preimage-verify','local','',
                 ['git','apply','--check',str(patch)])
        for gate in ('all_callers','cross_tree_consumers','similar_bug_search'):
            run_gate(gate,'whole-tree-search','whole-tree','count',
                     ['rg','-n','count','.'])
        run_gate('cross_tree_consumers','build-graph','whole-tree','Makefile',
                 ['rg','-n','Makefile','.'])
        run_gate('parallel_tree','integration-search','integration','count.c',
                 ['git','log','--oneline','--all','--','count.c'])
        run_gate('test_and_build_scope','build-or-test','local','count.c',
                 ['make','-C',str(repo),'test'])
        for sid in data['sections']:
            required=gate_module.SECTION_GATES[int(sid[1:])-1]
            gate_module.section(SimpleNamespace(manifest=self.manifest,id=sid,status='APPLIED',
                                                gate=required,reason=claim))
        r=self.check()
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertIn('ELIGIBLE_FOR_HUMAN_DECISION',r.stdout)
        # Alter evidence bytes after checking: the audit must fail again.
        adv.write_text(adv.read_text() + '\nUnauthorized change\n')
        self.assertEqual(self.check().returncode,2)


if __name__=='__main__':
    unittest.main(verbosity=2)
