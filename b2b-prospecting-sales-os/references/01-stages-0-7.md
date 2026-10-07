# Stages 0–7

## Stage 0 — Campaign Brief
Collect: campaign, offering company, solution, geography, ICP, size signal, target roles, exclusions, universe, max Tier A, credit budget. No research yet.
Exit: BRIEF_CONFIRMED.

## Stage 1 — Account Discovery
Search companies, not people. Prefer Apollo organization/account discovery when available.
Exit: ACCOUNTS_DISCOVERED.

## Stage 2 — ICP Qualification
Classify CUMPLE / POSIBLE / NO CUMPLE. Do not turn provider ranges into exact headcount.
Exit: ICP_QUALIFIED.

## Stage 3 — Prioritization
Tier A/B/C is internal research priority only, never purchase intent or probability. Respect max Tier A.
Exit: ACCOUNTS_PRIORITIZED.

## Stage 4A — Public decision-maker discovery
Find relevant HR/People/C&B/GM/operations roles using public research. No paid contact enrichment.

## Stage 4B — Optional Apollo People capability test
Use only if plan/cost permits. A provider plan block = BLOCKED_BY_PLAN, not “not found.”

## Stage 4C — Contact Strategy
Using only discovered people, produce Primary → Backup → Escalation when evidence supports it. Otherwise PENDIENTE_DE_DISCOVERY.
Human selects account/contact(s) that advance.

## Stage 5 — Identity Validation
Read references/07-credit-controls.md first.
Use free preview/search where available. Validate identity/company/title/location/profile. Do not enrich email/phone.
Outcomes: ENCONTRADO + confidence / COINCIDENCIA_AMBIGUA / NO_ENCONTRADO.

## Stage 6 — Work Email Enrichment
Requires explicit human approval under references/07-credit-controls.md.
Request only approved fields for approved contact(s).
For async jobs, store enrichment/job ID and poll the same job only. Never create a second job as an automatic retry.
Validate person + target company + domain.

If credits are insufficient:
1. do not switch paid provider automatically;
2. use already validated work email if available;
3. otherwise use another already validated legitimate no-cost channel only if downstream strategy supports it;
4. otherwise BLOCKED_BY_CREDITS.

## Stage 7 — Coverage benchmark
Benchmark only a small user-approved sample.
Measure separately:
- identity match;
- email result;
- target-account coherence;
- credits consumed.
Do not auto-enrich the entire universe.
