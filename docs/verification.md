# Verification model

Vico verification is intentionally evidence-based.

```text
Expected intent contract
  ↓
Actual capsule files
  ↓
Evidence map
  ↓
PASS / PARTIAL / FAIL
```

Current MVP gates:

| Gate | Meaning |
|---|---|
| `contracts_found` | Capsule has manifest or inline contracts. |
| `source_files_found` | Capsule contains text source files. |
| `no_forbidden_write` | No simple write-like pattern was found when write is forbidden. |
| `iteration_count` | Capsule tracks planned iteration states. |

Future gates:

- AST/tree-sitter effect detection,
- UI blueprint matching,
- OpenAPI contract checks,
- TestQL runtime probes,
- Playwright screenshot comparison,
- real Intract CLI integration.
