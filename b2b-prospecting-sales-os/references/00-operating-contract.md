# Operating Contract

## Evidence
Use only:
- HECHO VERIFICADO
- DATO PREVIAMENTE VALIDADO
- INFERENCIA COMERCIAL
- NO VERIFICADO / NO ENCONTRADO
- CONTRADICTORIO

For material Stage 8 signals use:
EVIDENCIA → QUÉ DEMUESTRA → QUÉ NO DEMUESTRA → INFERENCIA → CONFIANZA.

## Global anti-inference
- branches/rooms/capacity/vacancies/footprint/ranges ≠ exact headcount;
- title/seniority ≠ authority, budget, signature, procurement ownership or autonomy;
- local HR ≠ local decision autonomy;
- hiring ≠ turnover;
- expansion ≠ retention problem;
- reviews/testimonials ≠ corporate policy;
- public silence ≠ nonexistence;
- provider, budget, utilization, renewal, ROI, absenteeism and retention impact require evidence.

## State machine
Campaign:
PRECHECK → BRIEF_CONFIRMED → ACCOUNTS_DISCOVERED → ICP_QUALIFIED → ACCOUNTS_PRIORITIZED → PEOPLE_DISCOVERED → CONTACT_STRATEGY_READY → IDENTITY_VALIDATED → ENRICHMENT_AWAITING_APPROVAL → ENRICHMENT_RUNNING → CONTACT_ENRICHED/TERMINAL → BENCHMARK_COMPLETE → ACCOUNT_FANOUT

Account:
ACCOUNT_FANOUT → ACCOUNT_INTELLIGENCE_COMPLETE → OUTREACH_STRATEGY_COMPLETE → CRM_PAYLOAD_READY → SALES_HANDOFF_COMPLETE → HANDOFF_ARCHIVED → TRACKING_LOG_UPDATED → PROSPECTING_WORKFLOW_COMPLETE

External research:
ACCOUNT_FANOUT → EXTERNAL_RESEARCH_HANDOFF_READY → GEMINI_EXTERNAL_RESEARCH → HOST_RECONCILIATION → ACCOUNT_INTELLIGENCE_COMPLETE

Blocking states:
SOP_BLOCKED_BY_TOOLS
BLOCKED_BY_PLAN
BLOCKED_BY_CREDITS
BLOCKED_BY_UNVERIFIED_COST
BLOCKED_BY_INCOMPLETE_SOURCE_SET
BLOCKED_BY_INCOMPLETE_EXTERNAL_RESEARCH
AMBIGUOUS_MATCH
CREDIT_LIMIT_REACHED
ENRICHMENT_FAILED

## PRECHECK 0
Run without Deep Research, paid operations or writes to connected services.
Inventory capabilities already exposed by the host. Do not install, reconnect, request credentials or infer an authenticated account solely from a tool name. Use known session evidence or a documented no-cost read only when necessary; otherwise report connection/plan/cost as UNVERIFIED.

Report each capability as AVAILABLE, UNVERIFIED, MISSING or DEFERRED; include its applicable stage and documented fallback. SOP_READY means ready for the CURRENT stage only, never a guarantee that all later stages can run.

| Stage | Required now | Fallback / blocking rule |
| --- | --- | --- |
| 0 | User Campaign Brief inputs | No connector needed. Future tool gaps are DEFERRED. |
| 1–4 | Existing account/contact sources or public research appropriate to the stage | Prefer Apollo where available and permitted. Use public discovery if Apollo is unavailable/plan-blocked; never treat a plan block as no matches. |
| 5 | Sufficient identity evidence or verified no-cost identity lookup | Reuse adequate explicit validated evidence. Unknown provider cost stays blocked for that operation only. |
| 6–7 | Approved enrichment/provider, or the existing validated no-cost channel allowed by Stage 6 | Enforce spend controls. Campaign budget is not authorization. Do not start paid capability probes. |
| 8 | Account source bundle and native Deep Research | Recheck at runtime. If unavailable, prepare the Gemini handoff; user transfer is supported and needs no Gemini MCP. Missing source bundle blocks independently. |
| 9–10 | Approved preceding artifacts and normal text transformation | No Apollo, FullEnrich, Deep Research or GHL connector required. GHL = MANUAL. |
| 11 | Complete source artifacts and editable document generation | Use the existing DOCX → Google Doc → ODT → RTF preference. Full visual PASS still requires documented visual inspection; a structural script is insufficient. |
| 12 | Approved artifact and archive/tracker destination | Use connected Drive/Sheets when authorized. Otherwise provide manual archive/tracker instructions and wait for explicit completion evidence; do not claim completion from a prepared payload. |

Only return SOP_BLOCKED_BY_TOOLS when the current stage has no usable documented path. Ask only for what unblocks that stage. Missing future tools must not stop briefing, artifact review or other already feasible stages. Recheck capability, connection, plan and cost at the point of use.
