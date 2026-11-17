# Test Results — `output-token-optimizer`

- **Verdict:** `PASS`
- **Total:** 24 / 24 passed (0 failed, 0 errored, 0 skipped)
- **Duration:** 1.444 ms
- **Python:** 3.11.8

| Module | Class | Test | Status | Duration (ms) |
| :--- | :--- | :--- | :--- | ---: |
| `test_invariant_guard` | `TestInvariantGuard` | `test_extracts_bare_relative_path_with_extension` | **PASS** | 0.094 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_extracts_error_identifiers` | **PASS** | 0.039 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_extracts_fenced_code_block` | **PASS** | 0.032 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_extracts_inline_code` | **PASS** | 0.025 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_extracts_posix_path` | **PASS** | 0.025 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_extracts_url` | **PASS** | 0.028 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_extracts_version_strings` | **PASS** | 0.027 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_extracts_windows_path` | **PASS** | 0.031 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_ignores_unanchored_prose_slashes` | **PASS** | 0.024 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_order_preserving_deduplication` | **PASS** | 0.029 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_verify_invariants_flags_altered_path_and_version` | **PASS** | 0.025 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_verify_invariants_flags_dropped_command` | **PASS** | 0.022 |
| `test_invariant_guard` | `TestInvariantGuard` | `test_verify_invariants_passes_when_preserved` | **PASS** | 0.028 |
| `test_savings_report` | `TestSavingsReport` | `test_empty_raw_is_zero_division_safe` | **PASS** | 0.355 |
| `test_savings_report` | `TestSavingsReport` | `test_invariants_preserved_false_when_code_dropped` | **PASS** | 0.155 |
| `test_savings_report` | `TestSavingsReport` | `test_invariants_preserved_true_when_code_kept` | **PASS** | 0.027 |
| `test_savings_report` | `TestSavingsReport` | `test_positive_reduction_on_verbose_input` | **PASS** | 0.037 |
| `test_savings_report` | `TestSavingsReport` | `test_reduction_rounded_to_one_decimal` | **PASS** | 0.022 |
| `test_savings_report` | `TestSavingsReport` | `test_report_has_all_six_keys` | **PASS** | 0.025 |
| `test_token_estimator` | `TestTokenEstimator` | `test_bankers_rounding_10_and_14` | **PASS** | 0.018 |
| `test_token_estimator` | `TestTokenEstimator` | `test_chars_per_token_constant_is_four` | **PASS** | 0.012 |
| `test_token_estimator` | `TestTokenEstimator` | `test_count_chars_matches_len` | **PASS** | 0.012 |
| `test_token_estimator` | `TestTokenEstimator` | `test_empty_returns_zero` | **PASS** | 0.011 |
| `test_token_estimator` | `TestTokenEstimator` | `test_estimate_tokens_divides_by_four` | **PASS** | 0.012 |
