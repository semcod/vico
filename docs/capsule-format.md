# Capsule format

A Vico capsule is stored in:

```text
.vico/capsules/<name>/
  capsule.yaml
  intract.yaml
  src/
  fixtures/
  iterations/
  evidence/
  prompts/
```

Example `capsule.yaml`:

```yaml
name: menu-icons
type: vertical_slice
source_project_root: /repo/c2004
source_snapshot_id: baseline
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
```

A capsule should be small enough for a human or LLM to understand fully.
