# Examples

## Frontend view capsule

```bash
cd examples/frontend_view
python -m nexu init .
python -m nexu freeze . --name baseline
python -m nexu capsule create . --name menu-icons --domain menu --route /menu-icons --include "src/**"
python -m nexu capsule plan menu-icons --steps 10 --goal "Add icon preview table"
python -m nexu capsule blueprint menu-icons --print
python -m nexu capsule iterate menu-icons --steps 3 --goal "Add icon preview table"
python -m nexu capsule runtime menu-icons
python -m nexu capsule export-prompt menu-icons
python -m nexu capsule verify menu-icons
python -m nexu capsule report menu-icons
python -m nexu capsule status menu-icons
```

## Backend service capsule

```bash
cd examples/backend_service
python -m nexu init .
python -m nexu freeze . --name baseline
python -m nexu capsule create . --name users-api --domain users --endpoint GET:/api/users --include "app/**"
python -m nexu capsule plan users-api --steps 5
python -m nexu capsule blueprint users-api
python -m nexu capsule runtime users-api
python -m nexu capsule verify users-api
python -m nexu capsule report users-api
```

## Vertical slice capsule

```bash
cd examples/vertical_slice
python -m nexu init .
python -m nexu freeze . --name baseline
python -m nexu capsule create . --name flow --domain demo --route /flow --endpoint GET:/api/flow --include "src/**"
python -m nexu capsule plan flow --steps 10 --goal "Evolve a full UI + API flow"
python -m nexu capsule iterate flow --steps 10 --goal "Evolve a full UI + API flow"
python -m nexu capsule runtime flow
python -m nexu capsule export-prompt flow
python -m nexu capsule report flow
```

## Run all examples

```bash
python examples/run_examples.py
```


## MCP service

Folder: `examples/mcp_service/`

Shows how to expose nexu tools to an MCP-capable IDE/agent through `nexu mcp serve --path .`.
