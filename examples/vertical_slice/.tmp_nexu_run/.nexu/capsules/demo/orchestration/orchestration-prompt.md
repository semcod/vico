# nexu orchestration request

You are planning controlled capsule evolution, not editing the source project directly.
Create a step-by-step orchestration that keeps the LLM inside the capsule and preserves Intract contracts.

Return JSON only, matching this schema:

```yaml
type: object
required:
- mode
- goal
- steps
- risk_notes
- verification_strategy
properties:
  mode:
    type: string
  goal:
    type: string
  steps:
    type: array
    items:
      type: object
      required:
      - id
      - title
      - intent
      - prompt
      - expected_outputs
      - verification
      properties:
        id:
          type: string
        title:
          type: string
        intent:
          type: string
        prompt:
          type: string
        expected_outputs:
          type: array
          items:
            type: string
        verification:
          type: array
          items:
            type: string
  risk_notes:
    type: array
    items:
      type: string
  verification_strategy:
    type: array
    items:
      type: string
```

Rules:

- Every step must be small enough for one IDE-agent iteration.
- Every step must mention which intent contract it protects or extends.
- Never ask the agent to mutate the source project directly.
- If write effects are needed, split read-only preview and write/apply into separate steps.
- Include verification instructions for each step.
- Prefer evidence: output fields, fixtures, tests, UI/API blueprint, runtime mock and promotion plan.

Context:

```yaml
version: nexu.orchestration_context.v1
capsule:
  name: demo
  type: vertical_slice
  source_project_root: /home/tom/github/semcod/nexu/examples/vertical_slice/.tmp_nexu_run
  source_snapshot_id: baseline
  source_git_sha: 6bcda3ecc28021848890005e0cc1f35097fa1717
  selection:
    domain: general
    routes:
    - /demo
    endpoints:
    - GET:/api/demo
    include:
    - '**/*.py'
    exclude: []
  runtime:
    frontend: null
    backend: null
    data: []
  contracts_manifest: intract.yaml
  created_at: '2026-05-30T18:47:56+00:00'
  iterations:
  - S1
  - S2
  baseline_files:
    src/flow.py: ee90046f4810072ba5bac5277265e237ff8175ea8068c7a41a729f355f10497d
goal: demo
steps: 3
contracts:
- id: capsule.demo.main
  scope: module
  intent: evolve:demo
  priority: 2
  domain: general
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
  require:
  - validate.contracts
  - verify.capsule
  validate:
  - input_presence
  - output_presence
  - no_forbidden_effect
  meaning: evolve this isolated project slice without mutating the source project
blueprint:
  version: nexu.blueprint.v1
  capsule: demo
  created_at: '2026-05-30T18:47:56+00:00'
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
iteration_plan:
  version: nexu.iteration_plan.v1
  capsule: demo
  created_at: '2026-05-30T18:47:56+00:00'
  horizon: 3
  goal: demo
  contract_summary:
    intents:
    - evolve:demo
    outputs:
    - evidence_map
    - evolved_capsule
    - promotion_plan
    forbid:
    - destructive_write
    - secret_leak
    require:
    - validate.contracts
    - verify.capsule
  steps:
  - state: S1
    theme: stabilize_baseline
    title: Stabilize Baseline
    goal: demo
    expected_delta:
      ui: update capsule blueprint or mock surface
      api: update mock endpoint or response
      data: update fixtures only when needed
      tests: add or update evidence for this step
    verification_focus:
    - no forbidden effects
    - outputs have evidence
    - capsule diff is reviewable
    outputs_to_prove:
    - evidence_map
    - evolved_capsule
    - promotion_plan
  - state: S2
    theme: shape_contract
    title: Shape Contract
    goal: Make the main intent contract explicit and remove ambiguity.
    expected_delta:
      ui: update capsule blueprint or mock surface
      api: update mock endpoint or response
      data: update fixtures only when needed
      tests: add or update evidence for this step
    verification_focus:
    - no forbidden effects
    - outputs have evidence
    - capsule diff is reviewable
    outputs_to_prove:
    - evidence_map
    - evolved_capsule
    - promotion_plan
  - state: S3
    theme: mock_data
    title: Mock Data
    goal: Prepare focused fixtures and fake runtime data for fast iterations.
    expected_delta:
      ui: update capsule blueprint or mock surface
      api: update mock endpoint or response
      data: update fixtures only when needed
      tests: add or update evidence for this step
    verification_focus:
    - no forbidden effects
    - outputs have evidence
    - capsule diff is reviewable
    outputs_to_prove:
    - evidence_map
    - evolved_capsule
    - promotion_plan
verification:
  capsule: demo
  status: partial
  score: 0.9
  findings:
  - code: contracts_found
    status: pass
    message: Found 2 intent contract(s).
    evidence:
    - capsule.demo.main
    - evolve:menu_icon_flow
  - code: source_files_found
    status: pass
    message: Capsule contains 1 text source file(s).
    evidence:
    - src/src/flow.py
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
    - missing:evolved_capsule
    - missing:promotion_plan
  - code: required_intents
    status: warn
    message: Some required sub-intents are not explicitly present.
    evidence:
    - missing:preview.menu_icons
    - missing:validate.contracts
    - missing:verify.capsule
  - code: iteration_count
    status: pass
    message: Capsule has 2 planned iteration(s).
    evidence:
    - S1
    - S2
  created_at: '2026-05-30T18:47:56+00:00'
diff:
  capsule: demo
  added: []
  modified: []
  deleted: []
  unchanged:
  - src/flow.py
  created_at: '2026-05-30T18:47:56+00:00'
```
