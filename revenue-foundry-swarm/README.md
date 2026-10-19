# Revenue Foundry Swarm v0.3

A bounded scheduled multi-worker research pipeline, with durable-ish memory and optional AI analysis. **Not an independently earning swarm.**

## Live workflow
GitHub Actions runs every six hours and on manual dispatch. Hunters search public GitHub bounty issues; verifiers reject unsuitable items; an SQLite ledger tracks repeat discoveries. State is restored and saved via GitHub Actions cache (which may be evicted). Artifacts contain the report.

## AI integration — currently OFF
Optional OpenAI-compatible chat-completions API is supported. Repository secret: `RF_AI_KEY`. Repository variables: `RF_AI_URL` (full HTTPS endpoint), `RF_AI_MODEL`. The workflow deliberately sets `RF_MAX_AI_CALLS: '0'`. Enable only after the user explicitly approves the selected provider, its terms, potential charges and data sharing; set a small nonzero cap (maximum 8). Do not store API keys in public code.

## Limits
No unrestricted replication, external hosting, external outreach, PRs, proposals, purchases, payments or unapproved code execution. No claim of payment without evidence. Dollar amounts are unverified advertisements; South African eligibility, sponsor funding, and availability require independent confirmation. GitHub Actions cache is not a production database.

## Revenue path
Verify a genuinely payable issue, confirm sponsor and payment terms, build and test a deliverable, obtain user approval for any external submission, and verify cleared receipt. Until then: **R0 earned**.
