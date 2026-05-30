# Capsule format

A nexu capsule is stored in:

```text
.nexu/capsules/<name>/
  capsule.yaml
  intract.yaml
  src/
  fixtures/
  iterations/
  evidence/
  prompts/
  blueprints/
```

## Example `capsule.yaml`

```yaml
name: menu-icons
type: vertical_slice
source_project_root: /repo/c2004
source_snapshot_id: baseline
source_git_sha: a13f92c
selection:
  domain: menu
  routes:
    - /connect-menu-editor
  endpoints:
    - POST:/api/v3/menu/icons/normalize/preview
  include:
    - frontend/src/modules/connect-menu-editor/**
    - backend/app/cqrs/menu/**
contracts_manifest: intract.yaml
iterations:
  - S1
  - S2
baseline_files:
  frontend/src/modules/connect-menu-editor/MenuEditorPage.tsx: 2f3c...
  backend/app/cqrs/menu/preview.py: 8d1a...
```

## Baseline lock

`baseline_files` stores hashes of source files at the moment of capsule creation. nexu uses it for:

- `nexu capsule diff` — compare capsule contents with the frozen slice,
- `nexu capsule drift` — check whether original source files changed after capsule creation,
- safer `promote` review.

## Blueprint

`nexu capsule blueprint <name>` writes:

```text
.nexu/capsules/<name>/blueprints/blueprint.yaml
```

The blueprint is not a full app. It is a small future-preview model containing UI screens, API mock endpoints and suggested tests.

## Rule of thumb

A capsule should be small enough for a human or LLM to understand fully. Prefer a route, endpoint, service, module or vertical slice instead of the whole project.
