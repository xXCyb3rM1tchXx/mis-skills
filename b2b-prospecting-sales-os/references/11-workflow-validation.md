# Workflow validator JSON contract

Run `python scripts/validate_workflow_state.py state.json` before reporting a completed stage and before any potentially paid provider execution. Exit 0 means structural checks passed; exit 1 means invalid or blocked; exit 2 means CLI usage error. This is an offline preflight, not a provider wrapper, state engine, evidence reader or consent verifier. A PASS does not prove artifact contents, consent, actual credit balance or document quality. The controller must independently read evidence and the user's approval and consult the authoritative campaign credit ledger.

Required root fields: nonempty string `campaign` (stable campaign ID), integer `stage` (0–12; Gemini 8-B is 8), and `status` from the Operating Contract, consistent with that stage. All blocking states fail. New campaigns can begin with:

```json
{"campaign":"pilot","stage":0,"status":"PRECHECK"}
```

Stages 8–12 require `account: {"active_account":"account-a","account_isolation":true}`. Artifacts and gates carry the same campaign/account IDs, so references from another workstream fail. Artifact record: `{"reference":"actual-file-or-artifact-id","campaign":"pilot","active_account":"account-a"}`. Gate record: `{"result":"PASS","evidence_reference":"actual-review-record-id","campaign":"pilot","active_account":"account-a"}`. For stages 0–7, account ID is not required on those records. References must identify accessible materials; placeholder references are suitable only for synthetic tests.

For early-stage completion, `artifacts` requires the corresponding entry: `campaign_brief`, `account_universe`, `icp_qualification`, `account_prioritization`, `people_discovery`, `contact_strategy`, `identity_validation`, `enrichment_result`, or `coverage_benchmark`. `CONTACT_ENRICHED` and `TERMINAL` both use `enrichment_result`.

Account requirements accumulate:

| Stage/status | Additional artifacts | Additional gates |
|---|---|---|
| All 8–12 | `source_bundle_0_7` | `SOURCE_SET_VALIDATION` |
| External handoff/research/reconciliation | `gemini_handoff`; reconciliation also requires `external_dossier` | — |
| Intelligence complete and stages 9–12 | `stage_8_dossier`, `intelligence_preservation_ledger` | `STAGE_8_QUALITY_GATE`, `INTELLIGENCE_PRESERVATION_LEDGER` |
| Stage 9+ | `outreach_strategy` | — |
| Stage 10+ | `final_crm_payload` | `FINAL_VALIDATION_GATE` |
| Stage 11+ | `sales_handoff` | All eight handoff gates below |
| Stage 12 | `archive_receipt` | `ARCHIVE_GATE` |
| Tracking updated/workflow complete | `tracking_receipt` | `TRACKER_GATE` |

Completed intelligence also requires `research_mode: "native"` or `"gemini"`. Gemini requires `external_dossier`, `host_reconciliation`, and `RECONCILIATION_GATE` even at later stages. Handoff gates are `ETAPA_8_DOSSIER_ANALYZED`, `STANDALONE_HANDOFF_TEST`, `ACCOUNT_SPECIFICITY_TEST`, `INTELLIGENCE_LOSS_CHECK`, `DETAIL_RETENTION_TEST`, `BENCHMARK_PARITY_TEST`, `VISUAL_SYSTEM_GATE`, and `RENDERING_STYLE_GATE`. Here the dossier-analyzed boolean is represented by its review record with result PASS; this does not replace actual direct analysis. The offline document checker alone cannot supply VISUAL_SYSTEM_GATE.

## Credit preflight

When a `credit_authorization` is present, the validator loads and applies `schemas/credit-authorization.schema.json` using a dependency-free evaluator for the schema's supported keywords. Unsupported keywords fail closed. Credits must be finite, nonnegative numbers; booleans do not count as numbers. A campaign budget is never an authorization.

Example of a structurally valid single-operation authorization and request (synthetic, NOT permission to execute):

```json
{
  "campaign":"pilot", "stage":6, "status":"ENRICHMENT_AWAITING_APPROVAL",
  "credit_authorization": {
    "authorization_id":"approval-1", "approval_reference":"human-message-123",
    "provider":"FullEnrich", "operation":"work_email", "active_account":"account-a",
    "contacts":["person-1"], "fields":["contact.work_emails"], "max_credits":1,
    "single_use":true, "approved_by_human":true, "consumed":false, "consumed_credits":0
  },
  "requested_operation": {
    "authorization_id":"approval-1", "provider":"FullEnrich", "operation":"work_email",
    "active_account":"account-a", "contacts":["person-1"], "fields":["contact.work_emails"],
    "action":"start", "credit_ceiling":1, "cost_verified":true
  }
}
```

Provider, operation, account, contacts and fields must match exactly (array order is immaterial). A `start` request must have an unused approval, no stored job ID, and a verified cost ceiling within the authorized maximum. For uncertain costs, `hard_limit_enforced:true` is acceptable only after the controller verifies an actual enforceable cap; a budget estimate is insufficient. Include the requested operation whenever preparing a paid execution; absence of a request means state validation only, never permission to spend.

Immediately before execution the controller must atomically reserve/mark the approval consumed in the shared authoritative ledger. Record actual consumption and the returned job ID. If submission fails or times out after reservation, do not reset the approval or auto-retry: reconcile with the provider. These JSON checks are stateless and cannot prevent reuse if someone supplies a stale/fabricated ledger snapshot. Never treat repeated PASS results as reusable authorization.

Polling is different: use `action:"poll"`, the same stored `job_id`, `consumed:true`, `credit_ceiling:0` and `cost_verified:true`. A new job, an unknown-cost poll, scope expansion, excess consumption or a consumed start fails. A legitimately chargeable poll requires its own explicit approval; do not disguise it as this no-cost continuation. `ENRICHMENT_RUNNING` requires a consumed approval and stored job ID.

## Executable complete-account example and regression fixtures

`tests/test_workflow_state.py` provides the `complete()` fixture: a structurally valid native account at `PROSPECTING_WORKFLOW_COMPLETE` with every artifact and gate. To print the full JSON example without executing providers:

```sh
python -c 'import json, runpy; print(json.dumps(runpy.run_path("tests/test_workflow_state.py")["complete"](), indent=2))'
```

The `fixture://` references deliberately represent synthetic evidence, not genuine approved materials. Replace every reference and review record before operational use. Tests also exercise empty/invented states, missing completion artifacts/gates, cross-account artifacts, missing Gemini reconciliation, negative/NaN/bool credits, incomplete approvals, changed scope, excess credits, consumed reuse and same-job polling. Run:

```sh
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p test_workflow_state.py -v
```

## Migration

Older ad-hoc JSON snapshots must add mandatory campaign/stage fields, scoped artifact and review references for completed stages, and authorization ID/approval reference/consumption fields where applicable. Do not invent missing evidence to migrate: recover it from authorized artifacts or report the corresponding block. This changes the validation contract only; existing stage names, business-stage sequence, human approvals and MAS reference defaults remain unchanged.
