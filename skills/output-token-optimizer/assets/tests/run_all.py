from __future__ import annotations

import datetime
import io
import json
import platform
import sys
import time
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))


class _Recorder(unittest.TextTestResult):
    def __init__(self, stream, descriptions, verbosity) -> None:
        super().__init__(stream, descriptions, verbosity)
        self.records: list[dict[str, object]] = []
        self._start_time: float = 0.0

    def startTest(self, test: unittest.TestCase) -> None:
        self._start_time = time.perf_counter()
        super().startTest(test)

    def _record(self, test: unittest.TestCase, status: str, detail: str = "") -> None:
        duration_ms = round((time.perf_counter() - self._start_time) * 1000, 3)
        self.records.append(
            {
                "module": test.__class__.__module__,
                "class": test.__class__.__name__,
                "test": test._testMethodName,
                "status": status,
                "duration_ms": duration_ms,
                "detail": detail,
            }
        )

    def addSuccess(self, test: unittest.TestCase) -> None:
        super().addSuccess(test)
        self._record(test, "PASS")

    def addFailure(self, test: unittest.TestCase, err) -> None:
        super().addFailure(test, err)
        self._record(test, "FAIL", self._exc_info_to_string(err, test))

    def addError(self, test: unittest.TestCase, err) -> None:
        super().addError(test, err)
        self._record(test, "ERROR", self._exc_info_to_string(err, test))

    def addSkip(self, test: unittest.TestCase, reason: str) -> None:
        super().addSkip(test, reason)
        self._record(test, "SKIP", reason)


def main() -> int:
    suite_name = "output-token-optimizer"
    loader = unittest.TestLoader()
    suite = loader.discover(str(TESTS_DIR), pattern="test_*.py")

    log_buffer = io.StringIO()
    runner = unittest.TextTestRunner(
        stream=log_buffer, verbosity=2, resultclass=_Recorder
    )
    started_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    t0 = time.perf_counter()
    result: _Recorder = runner.run(suite)  # type: ignore[assignment]
    total_duration_ms = round((time.perf_counter() - t0) * 1000, 3)

    passed = sum(1 for r in result.records if r["status"] == "PASS")
    failed = len(result.failures)
    errored = len(result.errors)
    skipped = len(result.skipped)
    total = result.testsRun
    verdict = "PASS" if (failed == 0 and errored == 0) else "FAIL"

    log_text = log_buffer.getvalue()
    (TESTS_DIR / "test_run.log").write_text(log_text, encoding="utf-8")

    payload = {
        "suite": suite_name,
        "verdict": verdict,
        "timestamp": started_at,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "total": total,
        "passed": passed,
        "failed": failed,
        "errored": errored,
        "skipped": skipped,
        "duration_ms": total_duration_ms,
        "tests": result.records,
    }
    (TESTS_DIR / "test_results.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )

    md_lines = [
        f"# Test Results — `{suite_name}`",
        "",
        f"- **Verdict:** `{verdict}`",
        f"- **Total:** {passed} / {total} passed ({failed} failed, {errored} errored, {skipped} skipped)",
        f"- **Duration:** {total_duration_ms} ms",
        f"- **Python:** {platform.python_version()}",
        "",
        "| Module | Class | Test | Status | Duration (ms) |",
        "| :--- | :--- | :--- | :--- | ---: |",
    ]
    for r in result.records:
        md_lines.append(
            f"| `{r['module']}` | `{r['class']}` | `{r['test']}` | **{r['status']}** | {r['duration_ms']} |"
        )
    (TESTS_DIR / "test_results.md").write_text(
        "\n".join(md_lines) + "\n", encoding="utf-8"
    )

    print(f"[{suite_name}] VERDICT: {verdict} ({passed}/{total} passed)")
    return 0 if (failed == 0 and errored == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
