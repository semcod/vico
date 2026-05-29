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

## `vico capsule promote`

```bash
vico capsule promote users-api --dry-run
```

Writes `promotion-plan.yaml` for manual review. `--apply` is intentionally not implemented yet.
