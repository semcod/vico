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
  --route /connect-menu-editor/icon-normalization \
  --endpoint POST:/api/v3/menu/icons/normalize/preview \
  --include "frontend/src/modules/connect-menu-editor/**" \
  --include "backend/app/cqrs/menu/**" \
  --include "contracts/*Menu*"
```

Generate a deterministic 10-step plan:

```bash
vico capsule plan menu-icons --steps 10 --goal "Evolve menu icon preview and apply flow"
```

Generate a lightweight future-preview blueprint:

```bash
vico capsule blueprint menu-icons --print
```

Create iteration folders and prompts:

```bash
vico capsule iterate menu-icons --steps 10 --goal "Evolve menu icon preview and apply flow"
```

Build a static runtime/mock that can be opened in the browser:

```bash
vico capsule runtime menu-icons
```

Open:

```text
.vico/capsules/menu-icons/runtime/index.html
```

Export an LLM-ready prompt for the current iteration:

```bash
vico capsule export-prompt menu-icons
```

Verify:

```bash
vico capsule verify menu-icons
```

Generate the review report:

```bash
vico capsule report menu-icons
```

Check local capsule changes and source drift:

```bash
vico capsule diff menu-icons
vico capsule drift menu-icons
```

Promote after review:

```bash
vico capsule promote menu-icons --dry-run
```
