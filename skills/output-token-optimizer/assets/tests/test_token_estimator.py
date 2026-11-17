from __future__ import annotations

import unittest

from _common import lean_stats as ts


class TestTokenEstimator(unittest.TestCase):
    def test_empty_returns_zero(self) -> None:
        self.assertEqual(ts.estimate_tokens(""), 0)

    def test_count_chars_matches_len(self) -> None:
        sample = "Hello, world! 12345"
        self.assertEqual(ts.count_chars(sample), len(sample))

    def test_estimate_tokens_divides_by_four(self) -> None:
        self.assertEqual(ts.estimate_tokens("abcd" * 10), 10)

    def test_bankers_rounding_10_and_14(self) -> None:
        self.assertEqual(ts.estimate_tokens("x" * 10), 2)
        self.assertEqual(ts.estimate_tokens("x" * 14), 4)

    def test_chars_per_token_constant_is_four(self) -> None:
        self.assertEqual(ts.CHARS_PER_TOKEN, 4)


if __name__ == "__main__":
    unittest.main()
