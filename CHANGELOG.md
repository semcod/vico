# Changelog

## [Unreleased]

## [0.5.3] - 2026-05-30

### Docs
- Update README.md
- Update SUMD.md
- Update SUMR.md
- Update project/README.md
- Update project/context.md

### Other
- Update .gitignore
- Update app.doql.less
- Update project/analysis.toon.yaml
- Update project/calls.mmd
- Update project/calls.png
- Update project/calls.toon.yaml
- Update project/calls.yaml
- Update project/compact_flow.mmd
- Update project/compact_flow.png
- Update project/duplication.toon.yaml
- ... and 10 more files

## [0.5.2] - 2026-05-30

### Docs
- Update README.md
- Update docs/README.md
- Update docs/architecture.md
- Update docs/capsule-format.md
- Update docs/commands.md
- Update docs/examples.md
- Update docs/getting-started.md
- Update docs/intent-contracts.md
- Update docs/llm-orchestration.md
- Update docs/llm-review.md
- ... and 42 more files

### Test
- Update tests/test_capsule_next_stage.py
- Update tests/test_capsule_runtime_report.py
- Update tests/test_orchestration_mcp.py

### Other
- Update examples/backend_service/.tmp_nexu_run/.nexu/capsules/demo/blueprints/blueprint.yaml
- Update examples/backend_service/.tmp_nexu_run/.nexu/capsules/demo/bundles/bundle.yaml
- Update examples/backend_service/.tmp_nexu_run/.nexu/capsules/demo/bundles/demo-review-bundle.zip
- Update examples/backend_service/.tmp_nexu_run/.nexu/capsules/demo/capsule.yaml
- Update examples/backend_service/.tmp_nexu_run/.nexu/capsules/demo/evidence/diff.yaml
- Update examples/backend_service/.tmp_nexu_run/.nexu/capsules/demo/evidence/source-drift.yaml
- Update examples/backend_service/.tmp_nexu_run/.nexu/capsules/demo/evidence/verification.yaml
- Update examples/backend_service/.tmp_nexu_run/.nexu/capsules/demo/intract.yaml
- Update examples/backend_service/.tmp_nexu_run/.nexu/capsules/demo/iterations/S0/state.yaml
- Update examples/backend_service/.tmp_nexu_run/.nexu/capsules/demo/iterations/S1/state.yaml
- ... and 101 more files

## [0.5.1] - 2026-05-30

### Docs
- Update CHANGELOG.md
- Update README.md
- Update docs/README.md
- Update docs/architecture.md
- Update docs/capsule-format.md
- Update docs/commands.md
- Update docs/examples.md
- Update docs/getting-started.md
- Update docs/llm-orchestration.md
- Update docs/llm-review.md
- ... and 4 more files

### Test
- Update tests/test_capsule_runtime_report.py
- Update tests/test_orchestration_mcp.py
- Update tests/test_review_bundle.py

### Other
- Update VERSION
- Update examples/mcp_service/src/demo.py
- Update examples/run_examples.py
- Update uv.lock


## 0.5.0

- Added `vico capsule orchestrate` for offline or optional LLM-assisted capsule orchestration.
- Added `src/vico/orchestrate.py` with orchestration context, prompt, deterministic plan and markdown output.
- Added generic LiteLLM JSON helper for orchestration/review while keeping network calls disabled by default.
- Added conservative MCP-compatible stdio service with tools, resources and prompt templates.
- Added `vico mcp tools` and `vico mcp serve`.
- Added MCP service example and documentation.

## 0.4.0

- Added offline/optional LLM review packets with strict JSON review schema.
- Added `vico capsule review` to generate evidence-based review prompts and review YAML/Markdown.
- Added `vico capsule bundle` for portable ZIP bundles of capsule context, prompts and evidence.
- Added `vico.config` and LLM/review settings in `vico.yaml`.
- Strengthened promotion plans with prechecks, drift status, blocking findings and file mapping.

## 0.3.0

- Added `vico capsule plan` for deterministic S1..Sn iteration planning.
- Added `vico capsule runtime` to build a static HTML mock/runtime from capsule blueprint, contracts and fixtures.
- Added `vico capsule report` with Markdown, HTML and YAML verification evidence.
- Added `vico capsule journal` for capsule event history.
- Added journal hooks for capsule creation, planning, runtime and reports.
- Updated examples and docs for the runtime/report workflow.

## 0.2.0

- Added capsule status, blueprint, prompt export, diff and source drift checks.
- Added richer verification for baseline lock, forbidden writes, secret-like values, outputs and required intents.

## 0.1.0

- Initial freeze → capsule → iterate → verify → promote MVP.
