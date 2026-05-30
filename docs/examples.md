# Examples

## Frontend view capsule

```bash
cd examples/frontend_view
python -m vico init .
python -m vico freeze . --name baseline
python -m vico capsule create . --name menu-icons --domain menu --route /menu-icons --include "src/**"
python -m vico capsule plan menu-icons --steps 10 --goal "Add icon preview table"
python -m vico capsule blueprint menu-icons --print
python -m vico capsule iterate menu-icons --steps 3 --goal "Add icon preview table"
python -m vico capsule runtime menu-icons
python -m vico capsule export-prompt menu-icons
python -m vico capsule verify menu-icons
python -m vico capsule report menu-icons
python -m vico capsule status menu-icons
```

## Backend service capsule

```bash
cd examples/backend_service
python -m vico init .
python -m vico freeze . --name baseline
python -m vico capsule create . --name users-api --domain users --endpoint GET:/api/users --include "app/**"
python -m vico capsule plan users-api --steps 5
python -m vico capsule blueprint users-api
python -m vico capsule runtime users-api
python -m vico capsule verify users-api
python -m vico capsule report users-api
```

## Vertical slice capsule

```bash
cd examples/vertical_slice
python -m vico init .
python -m vico freeze . --name baseline
python -m vico capsule create . --name flow --domain demo --route /flow --endpoint GET:/api/flow --include "src/**"
python -m vico capsule plan flow --steps 10 --goal "Evolve a full UI + API flow"
python -m vico capsule iterate flow --steps 10 --goal "Evolve a full UI + API flow"
python -m vico capsule runtime flow
python -m vico capsule export-prompt flow
python -m vico capsule report flow
```

## Run all examples

```bash
python examples/run_examples.py
```


## MCP service

Folder: `examples/mcp_service/`

Shows how to expose Vico tools to an MCP-capable IDE/agent through `vico mcp serve --path .`.
