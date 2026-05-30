# Getting started

Install locally:

```bash
pip install -e .[dev]
nexu --help
```

Create nexu metadata in a project:

```bash
nexu init .
```

Freeze a baseline:

```bash
nexu freeze . --name baseline
```

Create a capsule from a small slice:

```bash
nexu capsule create . \
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
nexu capsule plan menu-icons --steps 10 --goal "Evolve menu icon preview and apply flow"
```

Generate a lightweight future-preview blueprint:

```bash
nexu capsule blueprint menu-icons --print
```

Create iteration folders and prompts:

```bash
nexu capsule iterate menu-icons --steps 10 --goal "Evolve menu icon preview and apply flow"
```

Build a static runtime/mock that can be opened in the browser:

```bash
nexu capsule runtime menu-icons
```

Open:

```text
.nexu/capsules/menu-icons/runtime/index.html
```

Export an LLM-ready prompt for the current iteration:

```bash
nexu capsule export-prompt menu-icons
```

Verify:

```bash
nexu capsule verify menu-icons
```

Generate the review report:

```bash
nexu capsule report menu-icons
```

Check local capsule changes and source drift:

```bash
nexu capsule diff menu-icons
nexu capsule drift menu-icons
```

Promote after review:

```bash
nexu capsule promote menu-icons --dry-run
```
