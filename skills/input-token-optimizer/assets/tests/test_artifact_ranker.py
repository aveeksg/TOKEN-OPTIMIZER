from __future__ import annotations

import unittest

from _common import context_pack_builder as b


class TestArtifactRanker(unittest.TestCase):
    def test_filename_goal_match_scores_high(self) -> None:
        ranker = b.ArtifactRanker("error triage")
        score = ranker.score_file("logs/error_triage_report.log")
        self.assertGreaterEqual(score, 20.0)

    def test_content_snippet_raises_score(self) -> None:
        ranker = b.ArtifactRanker("database migration query")
        base_score = ranker.score_file("db/schema.sql")
        snippet_score = ranker.score_file(
            "db/schema.sql",
            content_snippet="-- database migration query for users table",
        )
        self.assertGreater(snippet_score, base_score)


if __name__ == "__main__":
    unittest.main()
