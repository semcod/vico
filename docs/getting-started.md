# Getting started

Install locally:

```bash
pip install -e .[dev]
vico --help
```

Create Vico metadata in a project:

```bash
vico init .
```

Freeze a baseline:

```bash
vico freeze . --name baseline
```

Create a capsule from a small slice:

```bash
vico capsule create . \
  --name menu-icons \
  --domain menu \
  --include "frontend/src/modules/connect-menu-editor/**" \
  --include "backend/app/cqrs/menu/**" \
  --include "contracts/*Menu*"
```

Plan 10 iterations:

```bash
vico capsule iterate menu-icons --steps 10 --goal "Evolve menu icon preview and apply flow"
```

Verify:

```bash
vico capsule verify menu-icons
```

Promote after review:

```bash
vico capsule promote menu-icons --dry-run
```
