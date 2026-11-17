from __future__ import annotations

import datetime
import json
import platform
import subprocess
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = TESTS_DIR.parents[3]

SUITES = [
    (
        "input-token-optimizer",
        PLUGIN_ROOT / "skills" / "input-token-optimizer" / "assets" / "tests",
    ),
    (
        "output-token-optimizer",
        PLUGIN_ROOT / "skills" / "output-token-optimizer" / "assets" / "tests",
    ),
]


def main() -> int:
    suite_reports: list[dict[str, object]] = []
    overall_ok = True

    for suite_name, suite_dir in SUITES:
        runner_path = suite_dir / "run_all.py"
        proc = subprocess.run(
            [sys.executable, str(runner_path)],
            cwd=str(suite_dir),
            capture_output=True,
            text=True,
        )
        if proc.stdout:
            print(proc.stdout.strip())
        if proc.stderr:
            print(proc.stderr.strip(), file=sys.stderr)
        if proc.returncode != 0:
            overall_ok = False

        results_json = suite_dir / "test_results.json"
        if results_json.exists():
            data = json.loads(results_json.read_text(encoding="utf-8"))
            suite_reports.append(data)
            if data.get("verdict") != "PASS":
                overall_ok = False
        else:
            overall_ok = False

    total_tests = sum(int(r.get("total", 0)) for r in suite_reports)
    total_passed = sum(int(r.get("passed", 0)) for r in suite_reports)
    total_failed = sum(int(r.get("failed", 0)) for r in suite_reports)
    total_errored = sum(int(r.get("errored", 0)) for r in suite_reports)
    verdict = "PASS" if overall_ok else "FAIL"

    md_lines = [
        "# Consolidated Test Results — `token-optimizer-plugin`",
        "",
        f"- **Aggregate Verdict:** `{verdict}`",
        f"- **Totals:** {total_passed} / {total_tests} passed ({total_failed} failed, {total_errored} errored)",
        f"- **Timestamp:** {datetime.datetime.now(datetime.timezone.utc).isoformat()}",
        f"- **Python:** {platform.python_version()}",
        "",
        "## Suite Summary",
        "",
        "| Suite | Verdict | Passed | Total | Duration (ms) |",
        "| :--- | :--- | ---: | ---: | ---: |",
    ]
    for r in suite_reports:
        md_lines.append(
            f"| `{r['suite']}` | **{r['verdict']}** | {r['passed']} | {r['total']} | {r['duration_ms']} |"
        )

    for r in suite_reports:
        md_lines.extend(
            [
                "",
                f"## `{r['suite']}` Details",
                "",
                "| Module | Class | Test | Status | Duration (ms) |",
                "| :--- | :--- | :--- | :--- | ---: |",
            ]
        )
        for t in r.get("tests", []):  # type: ignore[union-attr]
            md_lines.append(
                f"| `{t['module']}` | `{t['class']}` | `{t['test']}` | **{t['status']}** | {t['duration_ms']} |"
            )

    (TESTS_DIR / "consolidated_test_results.md").write_text(
        "\n".join(md_lines) + "\n", encoding="utf-8"
    )

    print(f"AGGREGATE VERDICT: {verdict}, totals {total_passed} / {total_tests} passed.")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    sys.exit(main())
