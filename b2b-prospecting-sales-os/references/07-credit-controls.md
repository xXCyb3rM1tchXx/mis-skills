# Hard Credit and Spend Controls

Default:
SPEND_ALLOWED = FALSE

Any operation with positive, unknown, plan-dependent, or potentially credit-consuming cost is BLOCKED until explicit human authorization.

Authorization must identify:
- provider;
- exact operation;
- ACTIVE_ACCOUNT;
- exact contact(s);
- exact fields;
- current known balance when observable;
- verified cost rule OR explicit uncertain-cost hard maximum;
- maximum credits authorized;
- single-use scope.

Never:
- infer approval from campaign budget;
- exceed max credits;
- expand contact count or requested fields;
- reuse authorization across accounts;
- use one approval for a second enrichment retry;
- switch paid provider automatically;
- top up/buy credits;
- hide unknown cost behind “best effort.”

Unknown cost with no approved hard maximum:
BLOCKED_BY_UNVERIFIED_COST

Polling the SAME async job ID is continuation.
Starting a NEW paid job requires new approval.

Insufficient balance:
use only an already validated no-cost fallback defined by the current stage; otherwise BLOCKED_BY_CREDITS.

For multi-account work, the Campaign Orchestrator owns the Credit Ledger.
Batch approval is valid only when the user explicitly names accounts/contacts/fields and maximum total credits.

Silence, “continue”, or general campaign approval is never spend approval.
