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
