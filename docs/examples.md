# Examples

## Frontend view capsule

```bash
cd examples/frontend_view
python -m vico init .
python -m vico freeze . --name baseline
python -m vico capsule create . --name menu-icons --domain menu --include "src/**"
python -m vico capsule iterate menu-icons --steps 3 --goal "Add icon preview table"
python -m vico capsule verify menu-icons
```

## Backend service capsule

```bash
cd examples/backend_service
python -m vico init .
python -m vico freeze . --name baseline
python -m vico capsule create . --name users-api --domain users --include "app/**"
python -m vico capsule verify users-api
```

## Run all examples

```bash
python examples/run_examples.py
```
