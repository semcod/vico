# nexu capsule review request

Capsule: `demo`
Created at: 2026-05-30T18:47:55+00:00
Mode: offline

## Task

Review whether this capsule can be promoted back to the source project.
Do not judge by vibes. Use only the evidence below.

Return JSON matching this schema:

```json
type: object
required:
- decision
- summary
- evidence
- risks
- next_action
properties:
  decision:
    type: string
    enum:
    - approve
    - needs_revision
    - reject
  summary:
    type: string
  evidence:
    type: array
    items:
      type: string
  risks:
    type: array
    items:
      type: string
  next_action:
    type: string

```

## Verification

```yaml
capsule: demo
status: partial
score: 0.9
findings:
- code: contracts_found
  status: pass
  message: Found 2 intent contract(s).
  evidence:
  - capsule.demo.main
  - preview:menu_icon_normalization
- code: source_files_found
  status: pass
  message: Capsule contains 1 text source file(s).
  evidence:
  - src/src/menu_icons.py
- code: baseline_lock
  status: pass
  message: Baseline lock tracks 1 file(s).
  evidence:
  - modified=0
  - added=0
  - deleted=0
- code: no_forbidden_write
  status: pass
  message: No obvious forbidden write effect detected.
  evidence: []
- code: secret_leak_check
  status: pass
  message: No obvious secret-like values detected.
  evidence: []
- code: output_presence
  status: warn
  message: Some declared outputs have no text evidence.
  evidence:
  - missing:evidence_map
  - missing:evolved_capsule
  - missing:promotion_plan
- code: required_intents
  status: warn
  message: Some required sub-intents are not explicitly present.
  evidence:
  - missing:validate.contracts
  - missing:verify.capsule
- code: iteration_count
  status: pass
  message: Capsule has 2 planned iteration(s).
  evidence:
  - S1
  - S2
created_at: '2026-05-30T18:47:55+00:00'

```

## Diff

```yaml
capsule: demo
added: []
modified: []
deleted: []
unchanged:
- src/menu_icons.py
created_at: '2026-05-30T18:47:55+00:00'

```

## Source drift

```yaml
capsule: demo
created_at: '2026-05-30T18:47:55+00:00'
status: pass
changed: []
missing: []
recommendation: source baseline still matches

```

## Blueprint

```yaml
version: nexu.blueprint.v1
capsule: demo
created_at: '2026-05-30T18:47:55+00:00'
type: vertical_slice
domain: general
contracts:
- id: capsule.demo.main
  intent: evolve:demo
  input:
  - frozen_slice
  - fixtures
  - user_goal
  output:
  - evolved_capsule
  - promotion_plan
  - evidence_map
  effect:
  - read
  forbid:
  - destructive_write
  - secret_leak
ui:
  screens:
  - route: /demo
    layout: capsule_preview
    sections:
    - id: intent_summary
      type: summary
    - id: input_fixtures
      type: data_panel
    - id: preview
      type: mock_surface
    - id: evidence
      type: verification_panel
api:
  endpoints:
  - method: GET
    path: /api/demo
    kind: mock_endpoint
    response:
      status: ok
      source: capsule_fixture
tests:
  suggested:
  - contract_outputs_are_present
  - forbidden_effects_are_absent
  - capsule_promotion_plan_is_reviewable

```

## Deterministic decision

```yaml
mode: offline_deterministic
decision: needs_revision
summary: Verification status is partial with score 0.900.
evidence:
- Decision derived from deterministic nexu verification gates.
risks:
- At least one gate is not fully passing.
next_action: Create a follow-up capsule iteration for missing evidence before promotion.

```
