# Core regression cases

1. Fresh chat with no handoff → new campaign, PRECHECK, empty Stage 0.
2. Contact provided but no spend approval → no enrichment.
3. One-email/one-credit approval → no phone, batch, second contact or retry job.
4. Async enrichment in progress → poll same job ID only.
5. Apollo People blocked by plan → public discovery fallback, not “not found.”
6. Zero FullEnrich credits and no validated channel → BLOCKED_BY_CREDITS.
7. Deep Research exhausted at Stage 8 → Gemini handoff → user transfer → external dossier → host reconciliation.
8. Deep Research requested at Stage 10 → reject/reroute to normal transformation.
9. Two accounts → isolated workstreams; separate spend gates; no cross-account data leakage.
10. Stage 11 has all headings but shallow recap → BENCHMARK_PARITY_TEST FAIL.
11. Very long generic Stage 11 document → FAIL if intelligence density is weak.
12. Stage 11 content is correct but visual style differs from standard → VISUAL_SYSTEM_GATE FAIL.
13. Stage 11 DOCX matches the Xcaret-derived visual system and content gates → delivery allowed.
14. Stage 12 has tracker but ambiguous Drive → ask only for DRIVE DESTINO.


15. Empty JSON, unknown status, wrong-stage status or completion without artifact/gate references → state validator FAIL.
16. Incomplete/negative/non-finite credit approval, consumed approval reused, scope mismatch or ceiling above approval → FAIL. Same-job verified free polling remains valid.
17. Missing required DOCX style properties or table header fill, including invalid later-section geometry → structural visual FAIL. Structural PASS never grants VISUAL_SYSTEM_GATE.
18. New campaign with web but missing future connectors → Stage 0 SOP_READY, later gaps DEFERRED. Missing native Deep Research routes Stage 8 to Gemini handoff.
