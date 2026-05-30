# nexu capsule report — demo

Created at: 2026-05-30T18:47:56+00:00

## Decision

- Status: **partial**
- Score: **0.900**
- Latest iteration: **S2**

## Diff from capsule baseline

- Added: 0
- Modified: 0
- Deleted: 0
- Unchanged: 1

## Source drift

- Status: **pass**
- Changed source files: 0
- Missing source files: 0

## Verification gates

| Gate | Status | Message |
|---|---:|---|
| `contracts_found` | **pass** | Found 2 intent contract(s). |
| `source_files_found` | **pass** | Capsule contains 1 text source file(s). |
| `baseline_lock` | **pass** | Baseline lock tracks 1 file(s). |
| `no_forbidden_write` | **pass** | No obvious forbidden write effect detected. |
| `secret_leak_check` | **pass** | No obvious secret-like values detected. |
| `output_presence` | **warn** | Some declared outputs have no text evidence. |
| `required_intents` | **warn** | Some required sub-intents are not explicitly present. |
| `iteration_count` | **pass** | Capsule has 2 planned iteration(s). |

## Journal tail

```yaml
- index: 1
  created_at: '2026-05-30T18:47:56+00:00'
  event: capsule.created
  message: Created capsule from selected project slice.
  data:
    files: 1
    domain: general
- index: 2
  created_at: '2026-05-30T18:47:56+00:00'
  event: plan.created
  message: Created 3-step iteration plan.
  data:
    goal: demo
- index: 3
  created_at: '2026-05-30T18:47:56+00:00'
  event: runtime.built
  message: Built static capsule runtime.
  data:
    path: /home/tom/github/semcod/nexu/examples/vertical_slice/.tmp_nexu_run/.nexu/capsules/demo/runtime/index.html

```
