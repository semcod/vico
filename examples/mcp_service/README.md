# MCP service example

This example demonstrates how an MCP-capable IDE/agent could drive Vico tools.

```bash
vico init .
vico capsule create . --name demo --include "src/**" --domain mcp
vico capsule orchestrate demo --steps 3 --goal "Plan a safe MCP-driven capsule evolution"
vico mcp tools
vico mcp serve --path . --transport stdio
```

Minimal JSON-RPC request for the stdio service:

```json
{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}
```
