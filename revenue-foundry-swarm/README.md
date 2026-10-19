# Revenue Foundry Swarm v0.2

Bounded parallel workers (parent -> hunters -> assessors), GitHub API opportunity discovery, automated six-hour scheduling, read-only reporting. No third-party Python dependencies.

**Not yet LLM-driven or autonomously money-making.** Workers are processes, not independently reasoning AI agents. Child spawning is bounded by RF_MAX_WORKERS, maximum 12; the current workflow uses 4. Never assume advertised bounties are funded. All candidates require manual verification before coding or submission.

## Run
python revenue-foundry-swarm/swarm.py

GitHub: Actions -> Revenue Foundry Swarm -> Run workflow. Reports appear in workflow artifacts. Scheduled runs are best-effort and may be delayed.

## Safety and cost
No financial commitments, spending, outreach, bids, PRs, credential sharing, crypto transactions or self-replication across external hosts. GitHub Actions public repository standard runners have usage conditions; verify account-specific billing and policy. No model API calls are configured, and no credentials are stored in code.

## Next phases
Persist state, verify payout and SA eligibility, integrate an approved LLM runtime, add independent QA, approval-gated work submission, payment reconciliation. A real income-generating swarm needs actual paid tasks and a verified payment route.
