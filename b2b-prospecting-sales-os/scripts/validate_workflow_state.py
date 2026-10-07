#!/usr/bin/env python3
import json, sys

BLOCKING = {
    "SOP_BLOCKED_BY_TOOLS", "BLOCKED_BY_PLAN", "BLOCKED_BY_CREDITS",
    "BLOCKED_BY_UNVERIFIED_COST", "BLOCKED_BY_INCOMPLETE_SOURCE_SET",
    "BLOCKED_BY_INCOMPLETE_EXTERNAL_RESEARCH", "AMBIGUOUS_MATCH",
    "CREDIT_LIMIT_REACHED", "ENRICHMENT_FAILED"
}

def fail(msg):
    print(f"FAIL: {msg}")
    raise SystemExit(1)

def main(path):
    data=json.load(open(path, encoding="utf-8"))
    acct=data.get("account") or {}
    if acct:
        if acct.get("account_isolation") is not True:
            fail("account_isolation must be true")
        if not acct.get("active_account"):
            fail("active_account missing")
    auth=data.get("credit_authorization")
    if auth:
        if auth.get("approved_by_human") is not True or auth.get("single_use") is not True:
            fail("credit authorization must be human-approved and single-use")
        if auth.get("max_credits") is None:
            fail("max_credits missing")
    if data.get("status") in BLOCKING:
        print(f"BLOCKED: {data['status']}")
        return
    print("PASS: basic workflow state checks")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: validate_workflow_state.py state.json")
        raise SystemExit(2)
    main(sys.argv[1])
