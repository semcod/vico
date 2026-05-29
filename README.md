# Nexu


## AI Cost Tracking

![PyPI](https://img.shields.io/badge/pypi-costs-blue) ![Version](https://img.shields.io/badge/version-0.2.6-blue) ![Python](https://img.shields.io/badge/python-3.9+-blue) ![License](https://img.shields.io/badge/license-Apache--2.0-green)
![AI Cost](https://img.shields.io/badge/AI%20Cost-$0.52-orange) ![Human Time](https://img.shields.io/badge/Human%20Time-2.9h-blue) ![Model](https://img.shields.io/badge/Model-openrouter%2Fqwen%2Fqwen3--coder--next-lightgrey)

- 🤖 **LLM usage:** $0.5156 (6 commits)
- 👤 **Human dev:** ~$295 (2.9h @ $100/h, 30min dedup)

Generated on 2026-05-29 using [openrouter/qwen/qwen3-coder-next](https://openrouter.ai/qwen/qwen3-coder-next)

---

**Nexu** — **Visual Intent Contract Orchestrator**.

Nexu is a Python package and CLI for creating small, isolated project capsules from a large codebase.
It helps you freeze a baseline, extract a slice of code/data/contracts, evolve that slice through multiple
LLM or human iterations, and verify the result against formal intent contracts before promoting it back.

The core workflow is:

```text
freeze → capsule create → blueprint → iterate → export-prompt → verify → promote
```

Nexu is designed to work with **Intract**-style intent contracts, but it can run as a standalone prototype.
The goal is not to make an LLM magically correct. The goal is to keep the LLM inside a small, versioned,
contract-bound sandbox and detect when its output diverges from declared intent.

## What changed in 0.2.0

The second iteration adds the missing practical loop around capsules:

- baseline hash lock per capsule,
- capsule diff against the frozen slice,
- source drift check against the original files,
- generated UI/API/test blueprint,
- LLM-ready prompt export,
- capsule status command,
- richer verification with evidence for outputs, forbidden effects, required intents and secret-like values.

## Why Nexu?

Long-running IDE prompting has a common failure mode:

```text
large repo + vague task + many steps = context drift and hallucinated implementation
```

Nexu changes the operating model:

```text
large repo
  ↓ freeze baseline
small capsule
  ↓ evolve only this capsule
verified result
  ↓ promote to the real project
```

## Install locally

```bash
python -m venv .venv
. .venv/bin/activate
pip install -e .[dev]
nexu --help
```

## First run

```bash
nexu init .
nexu freeze . --name baseline
nexu capsule create . --name menu-icons --domain menu --include "examples/frontend_view/src/**" --route /menu-icons
nexu capsule blueprint menu-icons --print
nexu capsule iterate menu-icons --steps 3 --goal "Add preview, confidence and reason fields"
nexu capsule export-prompt menu-icons
nexu capsule verify menu-icons
nexu capsule diff menu-icons
nexu capsule drift menu-icons
nexu capsule promote menu-icons --dry-run
```

## Important folders

```text
src/nexu/       Python package
docs/           documentation
examples/       runnable example projects
tests/          unit tests
```

## Documentation

Start here:

- [Docs index](docs/README.md)
- [Getting started](docs/getting-started.md)
- [Architecture](docs/architecture.md)
- [Commands](docs/commands.md)
- [Capsule format](docs/capsule-format.md)
- [Intent contracts](docs/intent-contracts.md)
- [Verification model](docs/verification.md)
- [Examples](docs/examples.md)
- [Roadmap](docs/roadmap.md)

## Main commands

```bash
nexu init .
nexu freeze . --name baseline
nexu capsule create . --name my-slice --include "src/my_module/**"
nexu capsule list
nexu capsule status my-slice
nexu capsule blueprint my-slice
nexu capsule iterate my-slice --steps 10 --goal "Evolve final screen"
nexu capsule export-prompt my-slice
nexu capsule diff my-slice
nexu capsule drift my-slice
nexu capsule verify my-slice
nexu capsule promote my-slice --dry-run
```

## License

Licensed under Apache-2.0.
