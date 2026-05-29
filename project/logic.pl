% ── Project Metadata ─────────────────────────────────────
project_metadata('nexu', '0.2.5', 'python').

% ── Project Files ────────────────────────────────────────
project_file('app.doql.less', 39, 'less').
project_file('examples/backend_service/app/users.py', 9, 'python').
project_file('examples/frontend_view/src/menu_icons.py', 25, 'python').
project_file('examples/run_examples.py', 65, 'python').
project_file('examples/vertical_slice/src/flow.py', 10, 'python').
project_file('project.sh', 50, 'shell').
project_file('src/vico/__init__.py', 6, 'python').
project_file('src/vico/__main__.py', 5, 'python').
project_file('src/vico/blueprint.py', 74, 'python').
project_file('src/vico/capsule.py', 123, 'python').
project_file('src/vico/cli.py', 220, 'python').
project_file('src/vico/diff.py', 36, 'python').
project_file('src/vico/drift.py', 37, 'python').
project_file('src/vico/export_prompt.py', 101, 'python').
project_file('src/vico/files.py', 52, 'python').
project_file('src/vico/freeze.py', 27, 'python').
project_file('src/vico/git.py', 23, 'python').
project_file('src/vico/hashing.py', 17, 'python').
project_file('src/vico/init_project.py', 63, 'python').
project_file('src/vico/intract.py', 126, 'python').
project_file('src/vico/iterate.py', 45, 'python').
project_file('src/vico/models.py', 155, 'python').
project_file('src/vico/paths.py', 36, 'python').
project_file('src/vico/promote.py', 32, 'python').
project_file('src/vico/status.py', 36, 'python').
project_file('src/vico/verify.py', 237, 'python').
project_file('tests/test_capsule_flow.py', 26, 'python').
project_file('tests/test_capsule_next_stage.py', 59, 'python').
project_file('tests/test_intract.py', 12, 'python').
project_file('tests/test_models.py', 15, 'python').
project_file('tests/test_vico.py', 12, 'python').
project_file('tree.sh', 2, 'shell').

% ── Python Functions ─────────────────────────────────────
python_function('examples/backend_service/app/users.py', 'list_users', 2, 4, 1).
python_function('examples/frontend_view/src/menu_icons.py', 'preview_menu_icons', 1, 3, 2).
python_function('examples/run_examples.py', 'run_example', 1, 2, 17).
python_function('examples/run_examples.py', 'main', 0, 2, 1).
python_function('examples/vertical_slice/src/flow.py', 'run_flow', 1, 1, 0).
python_function('src/vico/blueprint.py', 'build_blueprint', 2, 7, 7).
python_function('src/vico/capsule.py', 'default_contract_manifest', 1, 1, 1).
python_function('src/vico/capsule.py', 'create_capsule', 2, 8, 19).
python_function('src/vico/capsule.py', 'list_capsules', 1, 4, 5).
python_function('src/vico/capsule.py', 'load_capsule', 2, 1, 3).
python_function('src/vico/capsule.py', 'save_capsule', 2, 1, 3).
python_function('src/vico/cli.py', 'init', 1, 3, 6).
python_function('src/vico/cli.py', 'freeze', 3, 2, 7).
python_function('src/vico/cli.py', 'capsule_create', 7, 1, 8).
python_function('src/vico/cli.py', 'capsule_list', 1, 3, 7).
python_function('src/vico/cli.py', 'capsule_status_command', 2, 3, 11).
python_function('src/vico/cli.py', 'capsule_iterate', 4, 1, 7).
python_function('src/vico/cli.py', 'capsule_blueprint', 3, 2, 8).
python_function('src/vico/cli.py', 'capsule_export_prompt', 3, 1, 8).
python_function('src/vico/cli.py', 'capsule_diff', 2, 1, 10).
python_function('src/vico/cli.py', 'capsule_drift', 2, 2, 7).
python_function('src/vico/cli.py', 'capsule_verify', 2, 4, 8).
python_function('src/vico/cli.py', 'capsule_promote', 3, 2, 7).
python_function('src/vico/diff.py', 'diff_capsule', 2, 12, 10).
python_function('src/vico/drift.py', 'check_source_drift', 2, 7, 9).
python_function('src/vico/export_prompt.py', '_latest_iteration', 1, 2, 0).
python_function('src/vico/export_prompt.py', 'export_iteration_prompt', 2, 3, 14).
python_function('src/vico/files.py', 'rel', 2, 1, 2).
python_function('src/vico/files.py', 'matches_any', 2, 3, 3).
python_function('src/vico/files.py', 'is_text_file', 1, 2, 1).
python_function('src/vico/files.py', 'collect_files', 3, 8, 7).
python_function('src/vico/freeze.py', 'freeze_project', 3, 2, 12).
python_function('src/vico/git.py', 'current_git_sha', 1, 4, 3).
python_function('src/vico/hashing.py', 'sha256_file', 1, 2, 6).
python_function('src/vico/hashing.py', 'sha256_text', 1, 1, 3).
python_function('src/vico/init_project.py', 'init_project', 1, 3, 4).
python_function('src/vico/intract.py', '_split_csv', 1, 4, 3).
python_function('src/vico/intract.py', '_tokenize_contract', 1, 5, 6).
python_function('src/vico/intract.py', 'parse_intract_line', 1, 3, 6).
python_function('src/vico/intract.py', 'scan_contracts_in_text', 1, 3, 4).
python_function('src/vico/intract.py', 'scan_contracts_in_file', 2, 3, 4).
python_function('src/vico/intract.py', 'read_manifest_contracts', 1, 12, 9).
python_function('src/vico/iterate.py', 'iterate_capsule', 2, 7, 13).
python_function('src/vico/models.py', 'utc_now', 0, 1, 2).
python_function('src/vico/models.py', 'write_yaml', 2, 1, 3).
python_function('src/vico/models.py', 'read_yaml', 1, 3, 4).
python_function('src/vico/paths.py', 'project_root', 1, 1, 3).
python_function('src/vico/paths.py', 'vico_dir', 1, 1, 0).
python_function('src/vico/paths.py', 'snapshots_dir', 1, 1, 1).
python_function('src/vico/paths.py', 'capsules_dir', 1, 1, 1).
python_function('src/vico/paths.py', 'capsule_dir', 2, 1, 1).
python_function('src/vico/paths.py', 'ensure_project_dirs', 1, 2, 4).
python_function('src/vico/promote.py', 'build_promotion_plan', 2, 2, 6).
python_function('src/vico/status.py', 'capsule_status', 2, 3, 6).
python_function('src/vico/verify.py', '_scan_capsule_contracts', 2, 2, 4).
python_function('src/vico/verify.py', '_text', 1, 2, 1).
python_function('src/vico/verify.py', '_contains_patterns', 2, 3, 2).
python_function('src/vico/verify.py', '_find_term_evidence', 3, 6, 8).
python_function('src/vico/verify.py', 'verify_capsule', 2, 45, 23).
python_function('tests/test_capsule_flow.py', 'test_capsule_flow', 1, 5, 7).
python_function('tests/test_capsule_next_stage.py', 'test_capsule_blueprint_prompt_diff_status_and_drift', 1, 11, 14).
python_function('tests/test_intract.py', 'test_parse_intract_line', 0, 5, 1).
python_function('tests/test_models.py', 'test_capsule_roundtrip', 0, 3, 4).
python_function('tests/test_models.py', 'test_snapshot_roundtrip', 0, 2, 3).
python_function('tests/test_vico.py', 'test_placeholder', 0, 2, 0).
python_function('tests/test_vico.py', 'test_import', 0, 1, 0).

% ── Python Classes ───────────────────────────────────────
python_class('src/vico/intract.py', 'IntentContract').
python_method('IntentContract', 'key', 0, 3, 0).
python_class('src/vico/models.py', 'FrozenFile').
python_class('src/vico/models.py', 'FrozenSnapshot').
python_method('FrozenSnapshot', 'to_dict', 0, 1, 1).
python_method('FrozenSnapshot', 'from_dict', 2, 2, 4).
python_class('src/vico/models.py', 'CapsuleSelection').
python_class('src/vico/models.py', 'CapsuleRuntime').
python_class('src/vico/models.py', 'Capsule').
python_method('Capsule', 'to_dict', 0, 1, 1).
python_method('Capsule', 'from_dict', 2, 2, 7).
python_class('src/vico/models.py', 'VerificationFinding').
python_class('src/vico/models.py', 'VerificationReport').
python_method('VerificationReport', 'to_dict', 0, 1, 1).
python_class('src/vico/models.py', 'CapsuleDiff').
python_method('CapsuleDiff', 'to_dict', 0, 1, 1).
python_class('src/vico/models.py', 'PromptExport').
python_method('PromptExport', 'to_dict', 0, 1, 1).

% ── Dependencies ─────────────────────────────────────────

% ── Makefile Targets ─────────────────────────────────────
makefile_target('test', '').
makefile_target('examples', '').

% ── Taskfile Tasks ───────────────────────────────────────

% ── Environment Variables ────────────────────────────────
env_variable('OPENROUTER_API_KEY', '*(not set)*', 'Required: OpenRouter API key (https://openrouter.ai/keys)').
env_variable('LLM_MODEL', 'openrouter/qwen/qwen3-coder-next', 'Model (default: openrouter/qwen/qwen3-coder-next)').
env_variable('PFIX_AUTO_APPLY', 'true', 'true = apply fixes without asking').
env_variable('PFIX_AUTO_INSTALL_DEPS', 'true', 'true = auto pip/uv install').
env_variable('PFIX_AUTO_RESTART', 'false', 'true = os.execv restart after fix').
env_variable('PFIX_MAX_RETRIES', '3', '').
env_variable('PFIX_DRY_RUN', 'false', '').
env_variable('PFIX_ENABLED', 'true', '').
env_variable('PFIX_GIT_COMMIT', 'false', 'true = auto-commit fixes').
env_variable('PFIX_GIT_PREFIX', 'pfix:', 'commit message prefix').
env_variable('PFIX_CREATE_BACKUPS', 'false', 'false = disable .pfix_backups/ directory').

% ── TestQL Scenarios ─────────────────────────────────────
testql_scenario('generated-cli-tests.testql.toon.yaml', 'cli').

% ── Semantic Facts from SUMD.md ──────────────────────────
sumd_declared_file('app.doql.less', 'doql').
sumd_declared_file('testql-scenarios/generated-cli-tests.testql.toon.yaml', 'testql').
sumd_declared_file('project/map.toon.yaml', 'analysis').
sumd_declared_file('project/logic.pl', 'analysis').
sumd_declared_file('project/calls.toon.yaml', 'analysis').
sumd_interface('cli', 'argparse').
sumd_interface('cli', '').
sumd_workflow('test', 'manual').
sumd_workflow_step('test', 1, 'pytest -q').
sumd_workflow('examples', 'manual').
sumd_workflow_step('examples', 1, 'python examples/run_examples.py').

