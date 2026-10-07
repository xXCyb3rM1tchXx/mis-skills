#!/usr/bin/env python3
"""Offline structural preflight; does not authenticate evidence or authorize spend."""
import json
import math
from pathlib import Path
import sys

BLOCKING = {
    'SOP_BLOCKED_BY_TOOLS', 'BLOCKED_BY_PLAN', 'BLOCKED_BY_CREDITS',
    'BLOCKED_BY_UNVERIFIED_COST', 'BLOCKED_BY_INCOMPLETE_SOURCE_SET',
    'BLOCKED_BY_INCOMPLETE_EXTERNAL_RESEARCH', 'AMBIGUOUS_MATCH',
    'CREDIT_LIMIT_REACHED', 'ENRICHMENT_FAILED',
}
STATES = {
    0: {'PRECHECK', 'SOP_READY', 'BRIEF_CONFIRMED'},
    1: {'ACCOUNTS_DISCOVERED'}, 2: {'ICP_QUALIFIED'},
    3: {'ACCOUNTS_PRIORITIZED'}, 4: {'PEOPLE_DISCOVERED', 'CONTACT_STRATEGY_READY'},
    5: {'IDENTITY_VALIDATED'},
    6: {'ENRICHMENT_AWAITING_APPROVAL', 'ENRICHMENT_RUNNING', 'CONTACT_ENRICHED', 'TERMINAL'},
    7: {'BENCHMARK_COMPLETE'},
    8: {'ACCOUNT_FANOUT', 'EXTERNAL_RESEARCH_HANDOFF_READY', 'GEMINI_EXTERNAL_RESEARCH',
        'HOST_RECONCILIATION', 'ACCOUNT_INTELLIGENCE_COMPLETE', 'READY_FOR_STAGE_9'},
    9: {'OUTREACH_STRATEGY_COMPLETE'}, 10: {'CRM_PAYLOAD_READY'},
    11: {'SALES_HANDOFF_COMPLETE'},
    12: {'HANDOFF_ARCHIVED', 'TRACKING_LOG_UPDATED', 'PROSPECTING_WORKFLOW_COMPLETE'},
}
EARLY_ARTIFACTS = dict(zip(
    ['BRIEF_CONFIRMED', 'ACCOUNTS_DISCOVERED', 'ICP_QUALIFIED', 'ACCOUNTS_PRIORITIZED',
     'PEOPLE_DISCOVERED', 'CONTACT_STRATEGY_READY', 'IDENTITY_VALIDATED',
     'CONTACT_ENRICHED', 'TERMINAL', 'BENCHMARK_COMPLETE'],
    ['campaign_brief', 'account_universe', 'icp_qualification', 'account_prioritization',
     'people_discovery', 'contact_strategy', 'identity_validation',
     'enrichment_result', 'enrichment_result', 'coverage_benchmark']))
HANDOFF_GATES = ['ETAPA_8_DOSSIER_ANALYZED', 'STANDALONE_HANDOFF_TEST',
    'ACCOUNT_SPECIFICITY_TEST', 'INTELLIGENCE_LOSS_CHECK', 'DETAIL_RETENTION_TEST',
    'BENCHMARK_PARITY_TEST', 'VISUAL_SYSTEM_GATE', 'RENDERING_STYLE_GATE']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def number(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def schema_check(value, schema, path='credit_authorization'):
    """Evaluate the keywords used by the bundled schema, with no third-party dependency."""
    allowed = {'$schema', 'title', 'type', 'required', 'properties', 'additionalProperties',
               'minLength', 'minimum', 'minItems', 'uniqueItems', 'items', 'const'}
    require(not set(schema) - allowed, f'{path}: unsupported schema keyword')
    checks = {'object': lambda v: isinstance(v, dict), 'string': lambda v: isinstance(v, str),
              'array': lambda v: isinstance(v, list), 'number': lambda v: type(v) in (int, float) and math.isfinite(v),
              'boolean': lambda v: type(v) is bool, 'null': lambda v: v is None}
    types = schema.get('type')
    if types:
        types = types if isinstance(types, list) else [types]
        require(all(t in checks for t in types), f'{path}: unsupported schema type')
        require(any(checks[t](value) for t in types), f'{path}: invalid type')
    if 'const' in schema:
        require(type(value) is type(schema['const']) and value == schema['const'], f'{path}: invalid constant')
    if isinstance(value, str) and 'minLength' in schema:
        require(len(value.strip()) >= schema['minLength'], f'{path}: empty string')
    if 'minimum' in schema:
        require(value >= schema['minimum'], f'{path}: below minimum')
    if isinstance(value, dict):
        for key in schema.get('required', []):
            require(key in value, f'{path}.{key}: required')
        props = schema.get('properties', {})
        if schema.get('additionalProperties') is False:
            require(not set(value) - set(props), f'{path}: unknown fields')
        for key, item in value.items():
            if key in props:
                schema_check(item, props[key], f'{path}.{key}')
    if isinstance(value, list):
        require(len(value) >= schema.get('minItems', 0), f'{path}: too few items')
        if schema.get('uniqueItems'):
            require(len({json.dumps(v, sort_keys=True) for v in value}) == len(value), f'{path}: duplicate items')
        for i, item in enumerate(value):
            if 'items' in schema:
                schema_check(item, schema['items'], f'{path}[{i}]')


def validate(data):
    require(isinstance(data, dict), 'state must be an object')
    require(nonempty(data.get('campaign')), 'campaign must be a nonempty identifier')
    stage, status = data.get('stage'), data.get('status')
    require(type(stage) is int and stage in STATES, 'stage must be an integer 0–12 (8-B uses 8)')
    require(nonempty(status) and status in STATES[stage] | BLOCKING, 'unknown status or wrong stage')
    if status in BLOCKING:
        raise ValueError(f'BLOCKED: {status}')
    acct = data.get('account', {})
    require(isinstance(acct, dict), 'account must be an object')
    if stage >= 8 or acct:
        require(acct.get('account_isolation') is True, 'account_isolation must be true')
        require(nonempty(acct.get('active_account')), 'active_account missing')
    artifacts, gates = data.get('artifacts', {}), data.get('gates', {})
    require(isinstance(artifacts, dict) and isinstance(gates, dict), 'artifacts/gates must be objects')

    def artifact(name):
        item = artifacts.get(name)
        require(isinstance(item, dict) and nonempty(item.get('reference')), f'artifact {name}: reference required')
        require(item.get('campaign') == data['campaign'], f'artifact {name}: wrong campaign')
        if stage >= 8:
            require(item.get('active_account') == acct['active_account'], f'artifact {name}: wrong account')

    def gate(name):
        item = gates.get(name)
        require(isinstance(item, dict) and item.get('result') == 'PASS' and nonempty(item.get('evidence_reference')),
                f'gate {name}: PASS and evidence_reference required')
        require(item.get('campaign') == data['campaign'], f'gate {name}: wrong campaign')
        if stage >= 8:
            require(item.get('active_account') == acct['active_account'], f'gate {name}: wrong account')

    if status in EARLY_ARTIFACTS:
        artifact(EARLY_ARTIFACTS[status])
    if stage >= 8:
        artifact('source_bundle_0_7')
        gate('SOURCE_SET_VALIDATION')
    external = status in {'EXTERNAL_RESEARCH_HANDOFF_READY', 'GEMINI_EXTERNAL_RESEARCH', 'HOST_RECONCILIATION'}
    if external:
        artifact('gemini_handoff')
    if status == 'HOST_RECONCILIATION':
        artifact('external_dossier')
    intelligence_complete = stage >= 9 or status in {'ACCOUNT_INTELLIGENCE_COMPLETE', 'READY_FOR_STAGE_9'}
    if intelligence_complete:
        artifact('stage_8_dossier')
        artifact('intelligence_preservation_ledger')
        gate('STAGE_8_QUALITY_GATE')
        gate('INTELLIGENCE_PRESERVATION_LEDGER')
        require(data.get('research_mode') in {'native', 'gemini'}, 'research_mode must be native or gemini')
        if data['research_mode'] == 'gemini':
            artifact('external_dossier')
            artifact('host_reconciliation')
            gate('RECONCILIATION_GATE')
    if stage >= 9:
        artifact('outreach_strategy')
    if stage >= 10:
        artifact('final_crm_payload')
        gate('FINAL_VALIDATION_GATE')
    if stage >= 11:
        artifact('sales_handoff')
        for name in HANDOFF_GATES:
            gate(name)
    if stage == 12:
        artifact('archive_receipt')
        gate('ARCHIVE_GATE')
        if status in {'TRACKING_LOG_UPDATED', 'PROSPECTING_WORKFLOW_COMPLETE'}:
            artifact('tracking_receipt')
            gate('TRACKER_GATE')
    auth = data.get('credit_authorization')
    request = data.get('requested_operation')
    if auth is not None:
        schema = json.loads((Path(__file__).resolve().parents[1] / 'schemas/credit-authorization.schema.json').read_text())
        schema_check(auth, schema)
        require(auth['consumed_credits'] <= auth['max_credits'], 'authorization credits exceeded')
        require(auth['consumed'] or auth['consumed_credits'] == 0, 'unused authorization has consumed credits')
        if acct:
            require(auth['active_account'] == acct['active_account'], 'authorization belongs to another account')
    if request is not None:
        require(stage in {5, 6, 7}, 'credit operation outside permitted enrichment stages')
        require(isinstance(request, dict) and auth is not None, 'requested operation requires authorization')
        require(request.get('authorization_id') == auth['authorization_id'], 'authorization ID mismatch')
        for name in ('provider', 'operation', 'active_account'):
            require(request.get(name) == auth[name], f'request {name}: outside authorization')
        for name in ('contacts', 'fields'):
            values = request.get(name)
            require(isinstance(values, list) and all(nonempty(v) for v in values), f'request {name}: invalid')
            require(len(values) == len(set(values)) and set(values) == set(auth[name]), f'request {name}: scope mismatch')
        action = request.get('action')
        require(action in {'start', 'poll'}, 'action must be start or poll')
        if action == 'start':
            require(auth['consumed'] is False and auth.get('job_id') is None, 'single-use approval already consumed')
            require(request.get('job_id') is None, 'start cannot carry existing job ID')
            ceiling = request.get('credit_ceiling')
            require(number(ceiling) and ceiling <= auth['max_credits'], 'invalid or excessive credit ceiling')
            require(request.get('cost_verified') is True or request.get('hard_limit_enforced') is True,
                    'unverified cost requires an enforceable hard maximum')
        else:
            require(auth['consumed'] is True and nonempty(auth.get('job_id')), 'poll requires a consumed approval and stored job ID')
            require(request.get('job_id') == auth['job_id'], 'poll must use the same job ID')
            require(type(request.get('credit_ceiling')) in (int, float) and request['credit_ceiling'] == 0
                    and request.get('cost_verified') is True, 'poll must be verified no-cost')
    if status == 'ENRICHMENT_RUNNING':
        require(auth is not None and auth['consumed'] is True and nonempty(auth.get('job_id')),
                'running enrichment requires consumed approval and job ID')


def main(path):
    try:
        with open(path, encoding='utf-8') as stream:
            data = json.load(stream, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f'non-finite number: {value}')))
        validate(data)
    except (ValueError, TypeError, KeyError, OSError) as error:
        print(f'FAIL: {error}')
        return 1
    print('PASS: structural state checks only; evidence, human consent and live credit ledger require independent verification')
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage: validate_workflow_state.py state.json')
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
