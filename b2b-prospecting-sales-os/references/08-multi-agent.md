# Multi-account / Multi-agent Orchestration

Use when more than one account proceeds beyond shared campaign stages.

## Campaign Orchestrator owns
- Campaign State
- shared Campaign Brief/evidence
- human selections
- Credit Ledger
- fan-out/fan-in
- blockers
- account completion states

## Account workstream / subagent
One per ACTIVE_ACCOUNT for Stages 8–12.

Each receives:
- shared Campaign Context
- only that account's validated facts
- only that account's contacts/enrichment
- only that account's artifacts
- only that account's explicit spend approvals

Never pass other accounts' dossiers/contact/enrichment results as operational input.

## Fan-out
1. Create one isolated workstream per selected account.
2. Set ACTIVE_ACCOUNT and ACCOUNT_ISOLATION=TRUE.
3. Copy shared Campaign Context + account-specific bundle.
4. Source Set Validation before Stage 8.

Parallelize only independent no-spend work.
Paid actions stay individually gated.

If native subagents are unavailable, emulate with separate chats/tasks/branches and explicit Account Handoffs.

Gemini fallback is per-account.
Never create a combined multi-account Gemini research package unless a later validated SOP revision explicitly allows it.

Each account independently reaches:
PROSPECTING_WORKFLOW_COMPLETE
