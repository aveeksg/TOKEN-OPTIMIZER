from __future__ import annotations

import unittest

from _common import lean_stats as ts


class TestInvariantGuard(unittest.TestCase):
    def test_extracts_fenced_code_block(self) -> None:
        text = "Run:\n```bash\nnpm test --watch\n```\nthen check."
        spans = ts.extract_protected_spans(text)
        self.assertIn("```bash\nnpm test --watch\n```", spans)

    def test_extracts_inline_code(self) -> None:
        text = "Wrap the value in `useMemo` before passing."
        spans = ts.extract_protected_spans(text)
        self.assertIn("`useMemo`", spans)

    def test_extracts_url(self) -> None:
        text = "See https://api.example.com/v1/users for details."
        spans = ts.extract_protected_spans(text)
        self.assertIn("https://api.example.com/v1/users", spans)

    def test_extracts_windows_path(self) -> None:
        text = r"Update C:\Users\me\config.json and restart."
        spans = ts.extract_protected_spans(text)
        self.assertIn(r"C:\Users\me\config.json", spans)

    def test_extracts_posix_path(self) -> None:
        text = "Check /etc/nginx/nginx.conf for worker settings."
        spans = ts.extract_protected_spans(text)
        self.assertIn("/etc/nginx/nginx.conf", spans)

    def test_extracts_version_strings(self) -> None:
        text = "Upgraded from v1.2.3 to 2.0.0-rc.1 in prod."
        spans = ts.extract_protected_spans(text)
        self.assertIn("v1.2.3", spans)
        self.assertIn("2.0.0-rc.1", spans)

    def test_extracts_error_identifiers(self) -> None:
        text = "Caught ValueError and TimeoutException after DeprecationWarning."
        spans = ts.extract_protected_spans(text)
        self.assertIn("ValueError", spans)
        self.assertIn("TimeoutException", spans)
        self.assertIn("DeprecationWarning", spans)

    def test_order_preserving_deduplication(self) -> None:
        text = "Use `foo`, then `bar`, then `foo` again."
        spans = ts.extract_protected_spans(text)
        self.assertEqual(spans, ["`foo`", "`bar`"])

    def test_ignores_unanchored_prose_slashes(self) -> None:
        text = "Check input/output and/or flags."
        spans = ts.extract_protected_spans(text)
        self.assertNotIn("input/output", spans)
        self.assertNotIn("and/or", spans)

    def test_extracts_bare_relative_path_with_extension(self) -> None:
        text = "Edit src/app/main.ts to register the route."
        spans = ts.extract_protected_spans(text)
        self.assertIn("src/app/main.ts", spans)

    def test_verify_invariants_passes_when_preserved(self) -> None:
        raw = "In src/app/main.ts on v1.2.0, `init()` raises ValueError."
        lean = "src/app/main.ts (v1.2.0): `init()` raises ValueError."
        self.assertEqual(ts.verify_invariants(raw, lean), [])

    def test_verify_invariants_flags_dropped_command(self) -> None:
        raw = "Please run `pytest -q tests/` to verify."
        lean = "Please run the test suite to verify."
        missing = ts.verify_invariants(raw, lean)
        self.assertIn("`pytest -q tests/`", missing)

    def test_verify_invariants_flags_altered_path_and_version(self) -> None:
        raw = "Update src/app/main.ts for v2.4.1 compatibility."
        lean = "Update src/app/index.ts for v2.4 compatibility."
        missing = ts.verify_invariants(raw, lean)
        self.assertIn("src/app/main.ts", missing)
        self.assertIn("v2.4.1", missing)


if __name__ == "__main__":
    unittest.main()
