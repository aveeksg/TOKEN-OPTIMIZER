from __future__ import annotations

import unittest

from _common import lean_stats as ts


class TestSavingsReport(unittest.TestCase):
    def test_report_has_all_six_keys(self) -> None:
        report = ts.savings_report("Hello world", "Hello")
        expected_keys = {
            "raw_chars",
            "lean_chars",
            "raw_tokens",
            "lean_tokens",
            "reduction_percent",
            "invariants_preserved",
        }
        self.assertEqual(set(report.keys()), expected_keys)

    def test_positive_reduction_on_verbose_input(self) -> None:
        raw = (
            "Great question! Basically, as you can see in src/app/main.ts, "
            "you should wrap the callback in `useCallback` to prevent extra renders."
        )
        lean = "In src/app/main.ts, wrap callback in `useCallback`."
        report = ts.savings_report(raw, lean)
        self.assertGreater(report["reduction_percent"], 0.0)
        self.assertTrue(report["invariants_preserved"])

    def test_invariants_preserved_true_when_code_kept(self) -> None:
        raw = "Run `npm run build` on v1.0.0."
        lean = "Run `npm run build` (v1.0.0)."
        report = ts.savings_report(raw, lean)
        self.assertTrue(report["invariants_preserved"])

    def test_invariants_preserved_false_when_code_dropped(self) -> None:
        raw = "Run `npm run build` on v1.0.0."
        lean = "Run the build script on v1.0.0."
        report = ts.savings_report(raw, lean)
        self.assertFalse(report["invariants_preserved"])

    def test_empty_raw_is_zero_division_safe(self) -> None:
        report = ts.savings_report("", "")
        self.assertEqual(report["raw_tokens"], 0)
        self.assertEqual(report["lean_tokens"], 0)
        self.assertEqual(report["reduction_percent"], 0.0)
        self.assertTrue(report["invariants_preserved"])

    def test_reduction_rounded_to_one_decimal(self) -> None:
        report = ts.savings_report("x" * 40, "x" * 12)
        self.assertEqual(report["reduction_percent"], 70.0)
        self.assertTrue(report["invariants_preserved"])


if __name__ == "__main__":
    unittest.main()
