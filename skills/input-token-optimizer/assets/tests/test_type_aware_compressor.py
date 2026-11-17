from __future__ import annotations

import unittest

from _common import context_pack_builder as b


class TestTypeAwareCompressor(unittest.TestCase):
    def test_code_extractor_pulls_def_and_control_flow(self) -> None:
        lines = [
            "import os",
            "def process_items(items):",
            "    x = 1",
            "    if not items:",
            "        return []",
            "    # TODO: optimize batching",
        ]
        chunks = b.TypeAwareCompressor.compress_code(lines, goal="optimize")
        summaries = [c[2] for c in chunks]
        self.assertIn("def process_items(items):", summaries)
        self.assertIn("if not items:", summaries)
        self.assertIn("return []", summaries)
        self.assertIn("# TODO: optimize batching", summaries)

    def test_log_extractor_finds_error_stack_and_id_chunks(self) -> None:
        lines = [
            "INFO Starting worker",
            "2026-11-17 12:00:01 ERROR Connection failed correlation_id=abc-123",
            '  File "app/db.py", line 42, in connect',
            "    raise RuntimeError('db down')",
        ]
        chunks = b.TypeAwareCompressor.compress_log(lines, goal="connection error")
        self.assertGreaterEqual(len(chunks), 2)

    def test_sql_extractor_yields_select_and_where_summaries(self) -> None:
        lines = [
            "SELECT id, email, created_at",
            "FROM users",
            "INNER JOIN accounts ON users.id = accounts.user_id",
            "WHERE users.active = 1",
            "ORDER BY created_at DESC",
        ]
        chunks = b.TypeAwareCompressor.compress_sql(lines, goal="active users")
        summaries = [c[2] for c in chunks]
        self.assertTrue(any(s.startswith("SELECT:") for s in summaries))
        self.assertTrue(any(s.startswith("WHERE:") for s in summaries))


if __name__ == "__main__":
    unittest.main()
