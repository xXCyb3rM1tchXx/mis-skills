import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('workflow', ROOT / 'scripts/validate_workflow_state.py')
workflow = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workflow)


def complete():
    state = {'campaign': 'pilot', 'stage': 12, 'status': 'PROSPECTING_WORKFLOW_COMPLETE',
             'account': {'active_account': 'account-a', 'account_isolation': True},
             'research_mode': 'native', 'artifacts': {}, 'gates': {}}
    for name in ('source_bundle_0_7', 'stage_8_dossier', 'intelligence_preservation_ledger',
                 'outreach_strategy', 'final_crm_payload', 'sales_handoff', 'archive_receipt', 'tracking_receipt'):
        state['artifacts'][name] = {'reference': f'fixture://{name}', 'campaign': 'pilot', 'active_account': 'account-a'}
    for name in ['SOURCE_SET_VALIDATION', 'STAGE_8_QUALITY_GATE', 'INTELLIGENCE_PRESERVATION_LEDGER',
                 'FINAL_VALIDATION_GATE', 'ARCHIVE_GATE', 'TRACKER_GATE'] + workflow.HANDOFF_GATES:
        state['gates'][name] = {'result': 'PASS', 'evidence_reference': f'fixture://{name}',
                              'campaign': 'pilot', 'active_account': 'account-a'}
    return state


def paid():
    auth = {'authorization_id': 'approval-1', 'approval_reference': 'message-1', 'provider': 'FullEnrich',
            'operation': 'work_email', 'active_account': 'account-a', 'contacts': ['person-1'],
            'fields': ['contact.work_emails'], 'max_credits': 1, 'single_use': True,
            'approved_by_human': True, 'consumed': False, 'consumed_credits': 0}
    request = {k: copy.deepcopy(auth[k]) for k in ('authorization_id', 'provider', 'operation', 'active_account', 'contacts', 'fields')}
    request.update(action='start', credit_ceiling=1, cost_verified=True)
    return {'campaign': 'pilot', 'stage': 6, 'status': 'ENRICHMENT_AWAITING_APPROVAL',
            'credit_authorization': auth, 'requested_operation': request}


class WorkflowTests(unittest.TestCase):
    def rejects(self, value):
        with self.assertRaises(ValueError):
            workflow.validate(value)

    def test_valid_precheck(self):
        workflow.validate({'campaign': 'pilot', 'stage': 0, 'status': 'PRECHECK'})

    def test_bad_audit_cases(self):
        for state in ({}, {'campaign': 'pilot', 'stage': 0, 'status': 'INVENTED'},
                      {'campaign': 'pilot', 'stage': 12, 'status': 'PROSPECTING_WORKFLOW_COMPLETE'},
                      {'campaign': 'pilot', 'stage': 6, 'status': 'BLOCKED_BY_CREDITS'}):
            with self.subTest(state=state): self.rejects(state)

    def test_valid_complete(self):
        workflow.validate(complete())

    def test_each_completion_requirement(self):
        for group in ('artifacts', 'gates'):
            for name in complete()[group]:
                state = complete(); del state[group][name]
                with self.subTest(missing=name): self.rejects(state)

    def test_cross_account(self):
        state = complete(); state['artifacts']['sales_handoff']['active_account'] = 'account-b'
        self.rejects(state)

    def test_gemini_needs_reconciliation(self):
        state = complete(); state['research_mode'] = 'gemini'; self.rejects(state)

    def test_valid_authorization(self):
        workflow.validate(paid())

    def test_auth_schema_and_limits(self):
        for key, value in [('max_credits', -1), ('max_credits', float('nan')), ('max_credits', True),
                           ('provider', ' '), ('consumed_credits', 2), ('consumed', True),
                           ('contacts', ['person-1', 'person-1'])]:
            state = paid(); state['credit_authorization'][key] = value
            with self.subTest(key=key, value=value): self.rejects(state)
        state = paid(); del state['credit_authorization']['approval_reference']; self.rejects(state)

    def test_request_mismatch(self):
        for key, value in [('provider', 'Other'), ('active_account', 'account-b'), ('contacts', ['person-2']),
                           ('fields', ['phone']), ('credit_ceiling', 2), ('cost_verified', False)]:
            state = paid(); state['requested_operation'][key] = value
            with self.subTest(key=key): self.rejects(state)

    def test_poll_and_reuse(self):
        state = paid(); state['credit_authorization'].update(consumed=True, consumed_credits=1, job_id='job-1')
        state['requested_operation'].update(action='poll', credit_ceiling=0, job_id='job-1')
        state['status'] = 'ENRICHMENT_RUNNING'
        workflow.validate(state)
        state['requested_operation']['job_id'] = 'job-2'; self.rejects(state)
        state['requested_operation'].update(action='start', job_id=None); self.rejects(state)


if __name__ == '__main__':
    unittest.main()
