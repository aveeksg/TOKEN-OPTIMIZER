# Test Results — `input-token-optimizer`

- **Verdict:** `PASS`
- **Total:** 9 / 9 passed (0 failed, 0 errored, 0 skipped)
- **Duration:** 1.121 ms
- **Python:** 3.11.8

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
