# Architecture

nexu is organized around one main concept: the **capsule**.

```text
large project
  -> freeze baseline
  -> create capsule from selected files/routes/endpoints
  -> plan S1..S10
  -> iterate inside capsule
  -> build runtime/mock
  -> verify contracts and evidence
  -> report
  -> promote after review
```

## Layers

```text
CLI
  -> capsule orchestration
  -> blueprint / runtime / reports
  -> Intract-style contracts
  -> diff / drift / verification
  -> promotion plan
```

## Important modules

```text
src/nexu/freeze.py          baseline hash snapshots
src/nexu/capsule.py         capsule creation/load/save
src/nexu/plan.py            deterministic S1..Sn iteration planning
src/nexu/blueprint.py       UI/API/test blueprint generation
src/nexu/runtime.py         static HTML capsule runtime/mock
src/nexu/export_prompt.py   LLM-ready prompt export
src/nexu/verify.py          verification gates and evidence
src/nexu/report.py          Markdown/HTML/YAML reports
src/nexu/journal.py         capsule event history
src/nexu/promote.py         promotion plan
```

## Why this shape?

nexu should not let an LLM edit the full project blindly. The LLM should work inside a small, versioned, contract-bound capsule. The source project remains frozen until promotion review.

## Relationship with Intract

nexu uses Intract-style contracts as the formal language of intent. In the MVP, nexu includes a lightweight parser for `@intract.v1` lines and `intract.yaml`. In a later version it should call the real Intract engine directly.
