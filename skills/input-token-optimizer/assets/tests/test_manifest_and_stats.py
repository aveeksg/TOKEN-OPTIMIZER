from __future__ import annotations

import unittest

from _common import context_pack_builder as b


class TestManifestAndStats(unittest.TestCase):
    def test_manifest_maps_1_based_lines_and_tags(self) -> None:
        chunks = [
            (0, 0, "ERROR: failed to load auth config"),
            (4, 4, "# TODO: retry auth handshake"),
        ]
        manifest = b.build_manifest(chunks, "src/auth_service.py", "code", "auth")
        self.assertEqual(len(manifest), 2)
        self.assertEqual(manifest[0].chunk_id, "auth_service_code_000")
        self.assertEqual(manifest[0].source_line_start, 1)
        self.assertEqual(manifest[0].source_line_end, 1)
        self.assertEqual(manifest[0].confidence, "high")
        self.assertIn("error", manifest[0].tags)
        self.assertIn("goal-relevant", manifest[0].tags)

        self.assertEqual(manifest[1].source_line_start, 5)
        self.assertEqual(manifest[1].source_line_end, 5)
        self.assertIn("todo", manifest[1].tags)

    def test_compute_stats_basic_ratios(self) -> None:
        stats = b.compute_stats(400, 100)
        self.assertEqual(stats.raw_tokens_estimate, 100)
        self.assertEqual(stats.compressed_tokens_estimate, 25)
        self.assertEqual(stats.compression_ratio, 0.25)
        self.assertEqual(stats.savings_percent, 75.0)

    def test_compute_stats_no_manifest_zero_confidence(self) -> None:
        stats = b.compute_stats(400, 100)
        self.assertEqual(stats.high_confidence_count, 0)
        self.assertEqual(stats.medium_confidence_count, 0)
        self.assertEqual(stats.low_confidence_count, 0)
        self.assertEqual(stats.low_confidence_percent, 0.0)

    def test_compute_stats_manifest_derived_confidence_counts(self) -> None:
        chunks = [
            (0, 0, "ERROR in handler"),
            (1, 1, "TODO: add fallback"),
            (2, 2, "x = 1"),
        ]
        manifest = b.build_manifest(chunks, "app.py", "code", "handler")
        manifest[2].confidence = "low"
        stats = b.compute_stats(800, 200, manifest=manifest)
        self.assertEqual(stats.high_confidence_count, 2)
        self.assertEqual(stats.low_confidence_count, 1)
        self.assertEqual(stats.low_confidence_percent, round(1 / 3 * 100, 1))


if __name__ == "__main__":
    unittest.main()
