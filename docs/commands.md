# Commands

## `nexu init`

```bash
nexu init .
```

Creates:

```text
nexu.yaml
intract.yaml
.nexu/
```

## `nexu freeze`

```bash
nexu freeze . --name baseline
```

Creates `.nexu/snapshots/<name>/snapshot.yaml` with text file hashes.

## `nexu capsule create`

```bash
nexu capsule create . --name users-api --endpoint POST:/api/users --include "backend/users/**"
```

Copies selected files into `.nexu/capsules/<name>/src/`, creates `capsule.yaml`, `intract.yaml`, `iterations/S0`, baseline file hashes and supporting folders.

## `nexu capsule status`

```bash
nexu capsule status users-api
```

Shows capsule metadata, latest iteration, diff counters and the latest verification summary.

## `nexu capsule plan`

```bash
nexu capsule plan users-api --steps 10 --goal "Improve create user flow" --print
```

Creates `.nexu/capsules/<name>/plan/iteration-plan.yaml`. This is a deterministic S1..Sn horizon plan. It does not call an LLM; it gives the LLM/human a small, safe roadmap inside the capsule.

## `nexu capsule blueprint`

```bash
nexu capsule blueprint users-api --print
```

Generates `.nexu/capsules/<name>/blueprints/blueprint.yaml` from routes, endpoints and Intract contracts. This is the lightweight future-preview model for UI/API/tests.

## `nexu capsule iterate`

```bash
nexu capsule iterate users-api --steps 10 --goal "Improve create user flow"
```

Creates planned iteration folders `S1..S10` and per-step prompts.

## `nexu capsule runtime`

```bash
nexu capsule runtime users-api
```

Builds a static capsule runtime/mock:

```text
.nexu/capsules/<name>/runtime/index.html
.nexu/capsules/<name>/runtime/data.json
.nexu/capsules/<name>/runtime/runtime.yaml
```

The HTML runtime shows UI screens, API endpoints, intent contracts, fixture data and the iteration timeline. It is intentionally static so it can be opened locally without extra services.

## `nexu capsule export-prompt`

```bash
nexu capsule export-prompt users-api
nexu capsule export-prompt users-api --iteration S3
```

Exports an LLM-ready prompt containing hard rules, Intract contracts, blueprint and current diff from baseline.

## `nexu capsule diff`

```bash
nexu capsule diff users-api
```

Compares `.nexu/capsules/<name>/src/` against the frozen baseline hashes captured at capsule creation.

## `nexu capsule drift`

```bash
nexu capsule drift users-api
```

Checks whether original source files changed since the capsule was created. If they changed, promotion needs rebase or extra manual review.

## `nexu capsule verify`

```bash
nexu capsule verify users-api
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

Writes `.nexu/capsules/<name>/evidence/verification.yaml`.

## `nexu capsule report`

```bash
nexu capsule report users-api
```

Builds an operator report:

```text
.nexu/capsules/<name>/reports/report.yaml
.nexu/capsules/<name>/reports/report.md
.nexu/capsules/<name>/reports/report.html
```

The report combines verification, diff, source drift and the capsule journal.

## `nexu capsule journal`

```bash
nexu capsule journal users-api
```

Shows the event history of a capsule: creation, planning, runtime builds, reports and other future automation events.


## `nexu capsule orchestrate`

```bash
nexu capsule orchestrate users-api --steps 10 --goal "Design safe create-user flow"
nexu capsule orchestrate users-api --steps 10 --call-llm
```

Builds an orchestration package:

```text
.nexu/capsules/<name>/orchestration/orchestration.yaml
.nexu/capsules/<name>/orchestration/orchestration.md
.nexu/capsules/<name>/orchestration/orchestration-prompt.md
.nexu/capsules/<name>/orchestration/orchestration-context.yaml
```

Offline mode is deterministic. LLM mode requires `llm.allow_network_calls: true`.

## `nexu capsule review`

```bash
nexu capsule review users-api
nexu capsule review users-api --iteration S3
nexu capsule review users-api --call-llm --model openrouter/anthropic/claude-3.5-sonnet
```

Builds an evidence-based review packet:

```text
.nexu/capsules/<name>/reviews/review.yaml
.nexu/capsules/<name>/reviews/review.md
.nexu/capsules/<name>/reviews/review-prompt.md
```

By default this is offline and deterministic. It does **not** ask an LLM to judge its own work.
Optional LLM review is available only when `llm.allow_network_calls: true` is set in `nexu.yaml` and the API key environment variable is present.

## `nexu capsule bundle`

```bash
nexu capsule bundle users-api
nexu capsule bundle users-api --no-src
```

Creates a portable ZIP for review or handoff:

```text
.nexu/capsules/<name>/bundles/<name>-review-bundle.zip
.nexu/capsules/<name>/bundles/bundle.yaml
```

## `nexu capsule promote`

```bash
nexu capsule promote users-api --dry-run
```

Writes `promotion-plan.yaml` for manual review. The plan includes verification prechecks, source drift status, blocking findings and source-to-target file mapping. `--apply` is intentionally not implemented yet.


## `nexu mcp tools`

```bash
nexu mcp tools
```

Lists tools exposed by the nexu MCP service.

## `nexu mcp serve`

```bash
nexu mcp serve --path . --transport stdio
```

Runs the MCP-compatible JSON-RPC stdio service. MVP supports stdio only.
