---
name: b2b-prospecting-sales-os
description: Run auditable B2B prospecting from campaign brief through account intelligence, outreach prep, CRM handoff and archive with hard spend gates, multi-account isolation and Gemini fallback.
---

# B2B Prospecting Sales OS

Author: Mitchell Correa/Cyberwolf AI
Version: 0.9.1 RC

Use this skill when the user asks to run, continue, audit, troubleshoot, or scale the validated B2B prospecting workflow.

## Non-negotiable rules

1. SOP State is not Campaign State. A new chat/session starts a NEW CAMPAIGN unless the user supplies an explicit Campaign Handoff, Account Handoff, inherited branch/task, or unambiguous continuation instruction.
2. Execute one stage at a time and respect human gates, tool boundaries, exit states, and stopping rules.
3. Never invent facts. Keep HECHO VERIFICADO / DATO PREVIAMENTE VALIDADO / INFERENCIA COMERCIAL / NO VERIFICADO-NO ENCONTRADO / CONTRADICTORIO separate.
4. SPEND_ALLOWED = FALSE by default. Never authorize, infer, increase, pool, reuse, or auto-approve provider credits.
5. Deep Research is allowed only in Stage 8 native Account Intelligence or the formally activated Stage 8-B external research fallback.
6. Stages 0–7 use shared campaign context. Stages 8–12 are account-specific and require ACCOUNT_ISOLATION=TRUE.
7. For more than one account, fan out into independent account workstreams. Never mix account-specific evidence.
8. Conversation history is not a guaranteed source. Validate explicit artifacts before transformations.
9. GHL remains manual. Prepare payload only.
10. Stage 11 is not a summary. BENCHMARK_PARITY_TEST and VISUAL_SYSTEM_GATE must both PASS.
11. SALES_HANDOFF_COMPLETE closes Stage 11 only. PROSPECTING_WORKFLOW_COMPLETE closes the workflow after Stage 12.

## Load-on-demand files

Always read:
- references/00-operating-contract.md

Then read current-stage instructions:
- Stages 0–7: references/01-stages-0-7.md
- Stage 8: references/02-stage-8-account-intelligence.md
- Stage 8-B: references/03-stage-8b-gemini-fallback.md
- Stages 9–10: references/04-stages-9-10.md
- Stage 11: references/05-stage-11-sales-handoff.md and references/09-visual-system.md
- Stage 12: references/06-stage-12-archive.md

Load when relevant:
- references/07-credit-controls.md
- references/08-multi-agent.md
- references/10-failure-recovery-privacy-platform.md

## First response behavior

For a new campaign:
1. Run PRECHECK 0 without Deep Research or paid operations.
2. Report readiness for account discovery, identity/email enrichment, public web/browser, Stage 8 Deep Research, editable document creation, archive/tracker capability, and GHL manual status.
3. If required capability is missing, return SOP_BLOCKED_BY_TOOLS and ask only for the missing capability.
4. If ready, begin Stage 0 empty and ask only minimum Campaign Brief inputs.

For a continuation:
1. Validate Campaign/Account Handoff and current stage.
2. Validate account isolation and required artifacts.
3. Continue only from the confirmed stage.

## Never do automatically

- Purchase/enrich email or phone data.
- Start a second paid enrichment as a retry.
- Expand a one-contact authorization to a batch.
- Switch paid providers because credits/plan ran out.
- Reuse one account's credit approval on another account.
- Run Deep Research outside Stage 8.
- Contact prospects or execute follow-ups.
- Populate unknown CRM fields to make a record look complete.
- Convert hiring, footprint, title, seniority, reviews, or public silence into unsupported business facts.
