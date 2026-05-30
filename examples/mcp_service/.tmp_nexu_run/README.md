# MCP service example

This example demonstrates how an MCP-capable IDE/agent could drive nexu tools.

```bash
nexu init .
nexu capsule create . --name demo --include "src/**" --domain mcp
nexu capsule orchestrate demo --steps 3 --goal "Plan a safe MCP-driven capsule evolution"
nexu mcp tools
nexu mcp serve --path . --transport stdio
```

Minimal JSON-RPC request for the stdio service:

```json
{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}
```
