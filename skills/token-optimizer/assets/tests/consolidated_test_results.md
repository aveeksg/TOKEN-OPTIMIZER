# Consolidated Test Results — `token-optimizer-plugin`

- **Aggregate Verdict:** `PASS`
- **Totals:** 33 / 33 passed (0 failed, 0 errored)
- **Timestamp:** 2026-11-17T10:31:23.441158+00:00
- **Python:** 3.11.8

## Suite Summary

| Suite | Verdict | Passed | Total | Duration (ms) |
| :--- | :--- | ---: | ---: | ---: |
| `input-token-optimizer` | **PASS** | 9 | 9 | 1.121 |
| `output-token-optimizer` | **PASS** | 24 | 24 | 2.963 |

## `input-token-optimizer` Details

| Module | Class | Test | Status | Duration (ms) |
| :--- | :--- | :--- | :--- | ---: |
| `test_artifact_ranker` | `TestArtifactRanker` | `test_content_snippet_raises_score` | **PASS** | 0.197 |
| `test_artifact_ranker` | `TestArtifactRanker` | `test_filename_goal_match_scores_high` | **PASS** | 0.052 |
| `test_manifest_and_stats` | `TestManifestAndStats` | `test_compute_stats_basic_ratios` | **PASS** | 0.039 |
| `test_manifest_and_stats` | `TestManifestAndStats` | `test_compute_stats_manifest_derived_confidence_counts` | **PASS** | 0.07 |
| `test_manifest_and_stats` | `TestManifestAndStats` | `test_compute_stats_no_manifest_zero_confidence` | **PASS** | 0.025 |
| `test_manifest_and_stats` | `TestManifestAndStats` | `test_manifest_maps_1_based_lines_and_tags` | **PASS** | 0.047 |
| `test_type_aware_compressor` | `TestTypeAwareCompressor` | `test_code_extractor_pulls_def_and_control_flow` | **PASS** | 0.045 |
| `test_type_aware_compressor` | `TestTypeAwareCompressor` | `test_log_extractor_finds_error_stack_and_id_chunks` | **PASS** | 0.041 |
| `test_type_aware_compressor` | `TestTypeAwareCompressor` | `test_sql_extractor_yields_select_and_where_summaries` | **PASS** | 0.072 |

## `output-token-optimizer` Details

| Module | Class | Test | Status | Duration (ms) |
| :--- | :--- | :--- | :--- | ---: |
| `test_invariant_guard` | `TestInvariantGuard` | `test_extracts_bare_relative_path_with_extension` | **PASS** | 0.105 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_extracts_error_identifiers` | **PASS** | 0.038 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_extracts_fenced_code_block` | **PASS** | 0.036 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_extracts_inline_code` | **PASS** | 0.026 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_extracts_posix_path` | **PASS** | 0.024 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_extracts_url` | **PASS** | 0.028 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_extracts_version_strings` | **PASS** | 0.028 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_extracts_windows_path` | **PASS** | 0.031 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_ignores_unanchored_prose_slashes` | **PASS** | 0.024 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_order_preserving_deduplication` | **PASS** | 0.031 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_verify_invariants_flags_altered_path_and_version` | **PASS** | 0.026 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_verify_invariants_flags_dropped_command` | **PASS** | 0.023 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_verify_invariants_passes_when_preserved` | **PASS** | 0.029 |
| `test_savings_report` | `TestSavingsReport` | `test_empty_raw_is_zero_division_safe` | **PASS** | 1.789 |
| `test_savings_report` | `TestSavingsReport` | `test_invariants_preserved_false_when_code_dropped` | **PASS** | 0.18 |
| `test_savings_report` | `TestSavingsReport` | `test_invariants_preserved_true_when_code_kept` | **PASS** | 0.027 |
| `test_savings_report` | `TestSavingsReport` | `test_positive_reduction_on_verbose_input` | **PASS** | 0.037 |
| `test_savings_report` | `TestSavingsReport` | `test_reduction_rounded_to_one_decimal` | **PASS** | 0.022 |
| `test_savings_report` | `TestSavingsReport` | `test_report_has_all_six_keys` | **PASS** | 0.029 |
| `test_token_estimator` | `TestTokenEstimator` | `test_bankers_rounding_10_and_14` | **PASS** | 0.02 |
| `test_token_estimator` | `TestTokenEstimator` | `test_chars_per_token_constant_is_four` | **PASS** | 0.013 |
| `test_token_estimator` | `TestTokenEstimator` | `test_count_chars_matches_len` | **PASS** | 0.012 |
| `test_token_estimator` | `TestTokenEstimator` | `test_empty_returns_zero` | **PASS** | 0.011 |
| `test_token_estimator` | `TestTokenEstimator` | `test_estimate_tokens_divides_by_four` | **PASS** | 0.011 |
