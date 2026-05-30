# Commands

## `vico init`

```bash
vico init .
```

Creates:

```text
vico.yaml
intract.yaml
.vico/
```

## `vico freeze`

```bash
vico freeze . --name baseline
```

Creates `.vico/snapshots/<name>/snapshot.yaml` with text file hashes.

## `vico capsule create`

```bash
vico capsule create . --name users-api --endpoint POST:/api/users --include "backend/users/**"
```

Copies selected files into `.vico/capsules/<name>/src/`, creates `capsule.yaml`, `intract.yaml`, `iterations/S0`, baseline file hashes and supporting folders.

## `vico capsule status`

```bash
vico capsule status users-api
```

Shows capsule metadata, latest iteration, diff counters and the latest verification summary.

## `vico capsule plan`

```bash
vico capsule plan users-api --steps 10 --goal "Improve create user flow" --print
```

Creates `.vico/capsules/<name>/plan/iteration-plan.yaml`. This is a deterministic S1..Sn horizon plan. It does not call an LLM; it gives the LLM/human a small, safe roadmap inside the capsule.

## `vico capsule blueprint`

```bash
vico capsule blueprint users-api --print
```

Generates `.vico/capsules/<name>/blueprints/blueprint.yaml` from routes, endpoints and Intract contracts. This is the lightweight future-preview model for UI/API/tests.

## `vico capsule iterate`

```bash
vico capsule iterate users-api --steps 10 --goal "Improve create user flow"
```

Creates planned iteration folders `S1..S10` and per-step prompts.

## `vico capsule runtime`

```bash
vico capsule runtime users-api
```

Builds a static capsule runtime/mock:

```text
.vico/capsules/<name>/runtime/index.html
.vico/capsules/<name>/runtime/data.json
.vico/capsules/<name>/runtime/runtime.yaml
```

The HTML runtime shows UI screens, API endpoints, intent contracts, fixture data and the iteration timeline. It is intentionally static so it can be opened locally without extra services.

## `vico capsule export-prompt`

```bash
vico capsule export-prompt users-api
vico capsule export-prompt users-api --iteration S3
```

Exports an LLM-ready prompt containing hard rules, Intract contracts, blueprint and current diff from baseline.

## `vico capsule diff`

```bash
vico capsule diff users-api
```

Compares `.vico/capsules/<name>/src/` against the frozen baseline hashes captured at capsule creation.

## `vico capsule drift`

```bash
vico capsule drift users-api
```

Checks whether original source files changed since the capsule was created. If they changed, promotion needs rebase or extra manual review.

## `vico capsule verify`

```bash
vico capsule verify users-api
```

Runs gates:

- contracts exist,
- source files exist,
- baseline lock exists,
- forbidden write-like patterns are absent when write is forbidden,
- secret-like values are absent when `secret_leak` is forbidden,
- declared outputs have text evidence,
- required intents are present or reported as missing,
- iterations are tracked.

Writes `.vico/capsules/<name>/evidence/verification.yaml`.

## `vico capsule report`

```bash
vico capsule report users-api
```

Builds an operator report:

```text
.vico/capsules/<name>/reports/report.yaml
.vico/capsules/<name>/reports/report.md
.vico/capsules/<name>/reports/report.html
```

The report combines verification, diff, source drift and the capsule journal.

## `vico capsule journal`

```bash
vico capsule journal users-api
```

Shows the event history of a capsule: creation, planning, runtime builds, reports and other future automation events.


## `vico capsule orchestrate`

```bash
vico capsule orchestrate users-api --steps 10 --goal "Design safe create-user flow"
vico capsule orchestrate users-api --steps 10 --call-llm
```

Builds an orchestration package:

```text
.vico/capsules/<name>/orchestration/orchestration.yaml
.vico/capsules/<name>/orchestration/orchestration.md
.vico/capsules/<name>/orchestration/orchestration-prompt.md
.vico/capsules/<name>/orchestration/orchestration-context.yaml
```

Offline mode is deterministic. LLM mode requires `llm.allow_network_calls: true`.

## `vico capsule review`

```bash
vico capsule review users-api
vico capsule review users-api --iteration S3
vico capsule review users-api --call-llm --model openrouter/anthropic/claude-3.5-sonnet
```

Builds an evidence-based review packet:

```text
.vico/capsules/<name>/reviews/review.yaml
.vico/capsules/<name>/reviews/review.md
.vico/capsules/<name>/reviews/review-prompt.md
```

By default this is offline and deterministic. It does **not** ask an LLM to judge its own work.
Optional LLM review is available only when `llm.allow_network_calls: true` is set in `vico.yaml` and the API key environment variable is present.

## `vico capsule bundle`

```bash
vico capsule bundle users-api
vico capsule bundle users-api --no-src
```

Creates a portable ZIP for review or handoff:

```text
.vico/capsules/<name>/bundles/<name>-review-bundle.zip
.vico/capsules/<name>/bundles/bundle.yaml
```

## `vico capsule promote`

```bash
vico capsule promote users-api --dry-run
```

Writes `promotion-plan.yaml` for manual review. The plan includes verification prechecks, source drift status, blocking findings and source-to-target file mapping. `--apply` is intentionally not implemented yet.


## `vico mcp tools`

```bash
vico mcp tools
```

Lists tools exposed by the Vico MCP service.

## `vico mcp serve`

```bash
vico mcp serve --path . --transport stdio
```

Runs the MCP-compatible JSON-RPC stdio service. MVP supports stdio only.
