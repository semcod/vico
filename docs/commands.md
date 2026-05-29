# Commands

## `nexu init`

```bash
nexu init .
```

Creates:

```text
nexu.yaml
intract.yaml
.vico/
```

## `nexu freeze`

```bash
nexu freeze . --name baseline
```

Creates `.vico/snapshots/<name>/snapshot.yaml` with text file hashes.

## `nexu capsule create`

```bash
nexu capsule create . --name users-api --endpoint POST:/api/users --include "backend/users/**"
```

Copies selected files into `.vico/capsules/<name>/src/`, creates `capsule.yaml`, `intract.yaml`, `iterations/S0`, baseline file hashes and supporting folders.

## `nexu capsule status`

```bash
nexu capsule status users-api
```

Shows capsule metadata, latest iteration, diff counters and the latest verification summary.

## `nexu capsule blueprint`

```bash
nexu capsule blueprint users-api --print
```

Generates `.vico/capsules/<name>/blueprints/blueprint.yaml` from routes, endpoints and Intract contracts. This is the lightweight future-preview model for UI/API/tests.

## `nexu capsule iterate`

```bash
nexu capsule iterate users-api --steps 10 --goal "Improve create user flow"
```

Creates planned iteration folders `S1..S10` and per-step prompts.

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

Compares `.vico/capsules/<name>/src/` against the frozen baseline hashes captured at capsule creation.

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

Writes `.vico/capsules/<name>/evidence/verification.yaml`.

## `nexu capsule promote`

```bash
nexu capsule promote users-api --dry-run
```

Writes `promotion-plan.yaml` for manual review. `--apply` is intentionally not implemented yet.
