# Architecture

Vico has five layers:

```text
Project root
  ↓ freeze
Snapshot
  ↓ slice
Capsule
  ↓ iterate
Future states S1..Sn
  ↓ verify
Evidence map
  ↓ promote
Promotion plan
```

## Core modules

```text
src/vico/models.py      dataclasses for snapshots, capsules and reports
src/vico/freeze.py      project snapshot generation
src/vico/capsule.py     capsule creation and loading
src/vico/iterate.py     planned iteration state folders
src/vico/verify.py      simple contract/effect verification gates
src/vico/promote.py     promotion plan generation
src/vico/intract.py     lightweight @intract.v1 parser adapter
src/vico/cli.py         Typer CLI
```

## Design rule

Vico does not let an LLM approve its own work. The LLM may suggest or modify a capsule,
but verification is done through files, contracts, diffs, tests and evidence.
