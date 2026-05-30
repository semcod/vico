# MCP service

Vico 0.5 exposes a conservative MCP-compatible stdio service so IDE agents can call Vico operations as tools.

The service is intentionally limited:

- no shell execution,
- no direct source-project mutation,
- promotion is dry-run only,
- LLM calls remain disabled unless `vico.yaml` explicitly allows network calls.

## List tools

```bash
vico mcp tools
```

## Run stdio service

```bash
vico mcp serve --path . --transport stdio
```

This command writes only JSON-RPC responses to stdout, so it can be wired into an MCP-capable IDE/client.

## Exposed tools

Important tools:

```text
vico_init
vico_freeze
vico_capsule_create
vico_capsule_list
vico_capsule_status
vico_capsule_plan
vico_capsule_blueprint
vico_capsule_iterate
vico_capsule_orchestrate
vico_capsule_export_prompt
vico_capsule_runtime
vico_capsule_verify
vico_capsule_review
vico_capsule_report
vico_capsule_promote_plan
```

## Resources and prompts

The service also exposes lightweight resources:

```text
vico://config
vico://capsules
vico://capsules/<name>/status
```

And a prompt template:

```text
vico_capsule_iteration
```

## Minimal JSON-RPC example

Send one line to the process stdin:

```json
{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}
```

Call a tool:

```json
{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"vico_capsule_list","arguments":{}}}
```

## Security model

MCP tools are powerful because an external agent can trigger local operations. Vico therefore keeps the first implementation conservative:

- `vico_capsule_promote_plan` creates a review plan only.
- `vico_capsule_orchestrate` uses offline mode unless the project config enables LLM network calls.
- all operations are rooted under the configured project path.
