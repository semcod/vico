# Architecture

Vico is a thin orchestration layer around isolated project capsules.

```text
source project
  -> freeze snapshot
  -> capsule selection
  -> baseline lock
  -> capsule src + fixtures + contracts
  -> blueprint / prompt / iteration state
  -> verification evidence
  -> promotion plan
```

## Core modules

- `models.py` — dataclasses for snapshots, capsules, diffs, prompt exports and verification reports.
- `freeze.py` — creates lightweight file-hash snapshots.
- `capsule.py` — creates and loads isolated capsules.
- `blueprint.py` — generates UI/API/test blueprint from capsule metadata and contracts.
- `iterate.py` — creates S1..Sn iteration folders and prompts.
- `export_prompt.py` — exports an LLM-ready prompt constrained by Intract contracts.
- `diff.py` — compares capsule state with baseline lock.
- `drift.py` — checks whether original source files changed after capsule creation.
- `verify.py` — builds evidence-based verification reports.
- `promote.py` — produces a dry-run promotion plan.

## Intract boundary

Vico does not replace Intract. Intract remains the intent-contract layer. Vico uses `@intract.v1` and `intract.yaml` as its formal input and converts them into prompts, blueprints, gates and evidence maps.

## Anti-hallucination principle

LLM output is not trusted directly. It must pass gates based on:

- frozen baseline,
- selected file scope,
- declared intent contracts,
- forbidden effects,
- required outputs,
- source drift,
- verification evidence.
