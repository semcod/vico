# Architecture

Vico is organized around one main concept: the **capsule**.

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
src/vico/freeze.py          baseline hash snapshots
src/vico/capsule.py         capsule creation/load/save
src/vico/plan.py            deterministic S1..Sn iteration planning
src/vico/blueprint.py       UI/API/test blueprint generation
src/vico/runtime.py         static HTML capsule runtime/mock
src/vico/export_prompt.py   LLM-ready prompt export
src/vico/verify.py          verification gates and evidence
src/vico/report.py          Markdown/HTML/YAML reports
src/vico/journal.py         capsule event history
src/vico/promote.py         promotion plan
```

## Why this shape?

Vico should not let an LLM edit the full project blindly. The LLM should work inside a small, versioned, contract-bound capsule. The source project remains frozen until promotion review.

## Relationship with Intract

Vico uses Intract-style contracts as the formal language of intent. In the MVP, Vico includes a lightweight parser for `@intract.v1` lines and `intract.yaml`. In a later version it should call the real Intract engine directly.
