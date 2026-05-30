# nexu orchestration — demo

Mode: `offline_deterministic`
Goal: demo

## Steps

### S1 — Stabilize Baseline

Intent: `evolve:demo`

Work only inside this capsule. Step S1: demo. Keep changes small, update fixtures/tests when needed, and leave evidence for every output.

Expected outputs: evidence_map, evolved_capsule, promotion_plan
Verification: run nexu capsule verify, check output evidence, check forbidden effects, prove forbids are not violated: destructive_write, secret_leak, prove outputs: evidence_map, evolved_capsule, promotion_plan

### S2 — Shape Contract

Intent: `evolve:demo`

Work only inside this capsule. Step S2: Make the main intent contract explicit and remove ambiguity.. Keep changes small, update fixtures/tests when needed, and leave evidence for every output.

Expected outputs: evidence_map, evolved_capsule, promotion_plan
Verification: run nexu capsule verify, check output evidence, check forbidden effects, prove forbids are not violated: destructive_write, secret_leak, prove outputs: evidence_map, evolved_capsule, promotion_plan

### S3 — Mock Data

Intent: `evolve:demo`

Work only inside this capsule. Step S3: Prepare focused fixtures and fake runtime data for fast iterations.. Keep changes small, update fixtures/tests when needed, and leave evidence for every output.

Expected outputs: evidence_map, evolved_capsule, promotion_plan
Verification: run nexu capsule verify, check output evidence, check forbidden effects, prove forbids are not violated: destructive_write, secret_leak, prove outputs: evidence_map, evolved_capsule, promotion_plan

## Risks

- Offline orchestration is conservative and does not infer hidden project behavior.
- Use LLM orchestration only as proposal; verify with deterministic gates before promotion.

## Verification strategy

- After every step: nexu capsule verify <name>
- Before promotion: nexu capsule review <name>
- Promotion remains dry-run until a human reviews evidence and drift.
