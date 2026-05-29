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

Copies selected files into `.vico/capsules/<name>/src/` and creates `capsule.yaml` plus `intract.yaml`.

## `vico capsule iterate`

```bash
vico capsule iterate users-api --steps 10 --goal "Improve create user flow"
```

Creates planned iteration folders `S1..S10`.

## `vico capsule verify`

```bash
vico capsule verify users-api
```

Runs basic gates:

- contracts exist,
- source files exist,
- forbidden write-like patterns are not present when write is forbidden,
- iterations are tracked.

## `vico capsule promote`

```bash
vico capsule promote users-api --dry-run
```

Writes `promotion-plan.yaml` for manual review.
