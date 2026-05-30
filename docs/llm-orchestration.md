# LLM orchestration

Vico 0.5 adds orchestration as a separate stage before review and promotion.

The goal is not to let an LLM freely mutate the project. The goal is to ask the LLM to produce a small, inspectable sequence of capsule steps that can later be verified by deterministic gates.

```text
freeze → capsule create → plan → orchestrate → iterate → verify → review → promote dry-run
```

## Offline by default

`vico capsule orchestrate` is deterministic unless `--call-llm` is passed and `llm.allow_network_calls: true` is set in `vico.yaml`.

```bash
vico capsule orchestrate menu-icons --steps 10 --goal "Add safe preview, apply and undo flow"
```

Generated files:

```text
.vico/capsules/<name>/orchestration/orchestration.yaml
.vico/capsules/<name>/orchestration/orchestration.md
.vico/capsules/<name>/orchestration/orchestration-prompt.md
.vico/capsules/<name>/orchestration/orchestration-context.yaml
```

## Optional LLM mode

```yaml
# vico.yaml
llm:
  provider: openrouter
  model: openrouter/qwen/qwen3-coder-next
  base_url: https://openrouter.ai/api/v1
  api_key_env: OPENROUTER_API_KEY
  temperature: 0.1
  timeout: 60
  allow_network_calls: true
```

```bash
export OPENROUTER_API_KEY="..."
vico capsule orchestrate menu-icons \
  --steps 10 \
  --goal "Generate a safe UI/API evolution plan" \
  --call-llm
```

The LLM is asked for JSON only. Vico still treats this as a proposal. The generated plan must be verified by `vico capsule verify` and reviewed before promotion.

## Why orchestration is separate from review

- `orchestrate` answers: what sequence of capsule steps should be attempted?
- `iterate` creates local S1..Sn step folders and prompts.
- `verify` checks whether current capsule artifacts match contracts.
- `review` builds the final handoff packet.

The LLM may help create the plan, but it does not approve its own result.
