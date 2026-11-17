from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from token_optimizer import __version__
from token_optimizer.context_pack_builder import (
    ArtifactRanker,
    TypeAwareCompressor,
    build_manifest,
    compute_stats,
)
from token_optimizer.lean_stats import (
    extract_protected_spans,
    savings_report,
    verify_invariants,
)


def _cmd_savings(args: argparse.Namespace) -> int:
    report = savings_report(args.raw, args.lean)
    print(json.dumps(report, indent=2))
    return 0 if report["invariants_preserved"] else 1


def _cmd_verify(args: argparse.Namespace) -> int:
    missing = verify_invariants(args.raw, args.lean)
    spans = extract_protected_spans(args.raw)
    payload = {
        "protected_spans": spans,
        "missing_spans": missing,
        "invariants_preserved": len(missing) == 0,
    }
    print(json.dumps(payload, indent=2))
    return 0 if not missing else 1


def _cmd_stats(args: argparse.Namespace) -> int:
    stats = compute_stats(args.raw_chars, args.compressed_chars)
    payload = {
        "raw_chars": stats.raw_chars,
        "raw_tokens_estimate": stats.raw_tokens_estimate,
        "compressed_chars": stats.compressed_chars,
        "compressed_tokens_estimate": stats.compressed_tokens_estimate,
        "compression_ratio": stats.compression_ratio,
        "savings_percent": stats.savings_percent,
        "low_confidence_percent": stats.low_confidence_percent,
    }
    print(json.dumps(payload, indent=2))
    return 0


def _cmd_rank(args: argparse.Namespace) -> int:
    ranker = ArtifactRanker(args.goal)
    scored: list[dict[str, object]] = []
    for p_str in args.paths:
        p = Path(p_str)
        snippet = ""
        if p.is_file():
            try:
                snippet = p.read_text(encoding="utf-8", errors="ignore")[:2000]
            except OSError:
                snippet = ""
        score = ranker.score_file(p_str, content_snippet=snippet)
        scored.append({"path": p_str, "score": score})
    scored.sort(key=lambda item: float(item["score"]), reverse=True)  # type: ignore[arg-type]
    print(json.dumps(scored, indent=2))
    return 0


def _cmd_compress(args: argparse.Namespace) -> int:
    file_path = Path(args.file)
    if not file_path.is_file():
        print(f"Error: file not found: {file_path}", file=sys.stderr)
        return 1

    text = file_path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    suffix = file_path.suffix.lower()

    if suffix in (".log",):
        file_type = "log"
        chunks = TypeAwareCompressor.compress_log(lines, goal=args.goal)
    elif suffix in (".sql",):
        file_type = "sql"
        chunks = TypeAwareCompressor.compress_sql(lines, goal=args.goal)
    elif suffix in (".md", ".txt"):
        file_type = "doc"
        chunks = TypeAwareCompressor.compress_markdown(lines, goal=args.goal)
    elif suffix in (".json", ".yaml", ".yml"):
        file_type = "config"
        chunks = TypeAwareCompressor.compress_json_yaml(lines, goal=args.goal)
    else:
        file_type = "code"
        chunks = TypeAwareCompressor.compress_code(lines, goal=args.goal)

    manifest = build_manifest(chunks, str(file_path), file_type, args.goal)
    compressed_text = "\n".join(c[2] for c in chunks)
    stats = compute_stats(len(text), len(compressed_text), manifest=manifest)

    payload = {
        "file": str(file_path),
        "file_type": file_type,
        "stats": {
            "raw_chars": stats.raw_chars,
            "raw_tokens_estimate": stats.raw_tokens_estimate,
            "compressed_chars": stats.compressed_chars,
            "compressed_tokens_estimate": stats.compressed_tokens_estimate,
            "compression_ratio": stats.compression_ratio,
            "savings_percent": stats.savings_percent,
            "low_confidence_percent": stats.low_confidence_percent,
        },
        "chunks": [
            {
                "chunk_id": m.chunk_id,
                "summary_text": m.summary_text,
                "source_file": m.source_file,
                "source_line_start": m.source_line_start,
                "source_line_end": m.source_line_end,
                "confidence": m.confidence,
                "tags": m.tags,
            }
            for m in manifest
        ],
    }
    print(json.dumps(payload, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="token-optimizer",
        description="Local-first, end-to-end token optimization toolkit for VS Code Copilot.",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_savings = sub.add_parser(
        "savings", help="Compute output-side token savings and verify invariants"
    )
    p_savings.add_argument("--raw", required=True, help="Raw text")
    p_savings.add_argument("--lean", required=True, help="Lean rewritten text")
    p_savings.set_defaults(func=_cmd_savings)

    p_verify = sub.add_parser(
        "verify", help="Verify byte-for-byte invariant preservation"
    )
    p_verify.add_argument("--raw", required=True, help="Raw text")
    p_verify.add_argument("--lean", required=True, help="Lean rewritten text")
    p_verify.set_defaults(func=_cmd_verify)

    p_stats = sub.add_parser(
        "stats", help="Compute input-side context pack statistics"
    )
    p_stats.add_argument(
        "--raw-chars", type=int, required=True, help="Raw character count"
    )
    p_stats.add_argument(
        "--compressed-chars",
        type=int,
        required=True,
        help="Compressed character count",
    )
    p_stats.set_defaults(func=_cmd_stats)

    p_rank = sub.add_parser(
        "rank", help="Rank candidate files against a task goal"
    )
    p_rank.add_argument("--goal", required=True, help="Task goal string")
    p_rank.add_argument("paths", nargs="+", help="File paths to score")
    p_rank.set_defaults(func=_cmd_rank)

    p_compress = sub.add_parser(
        "compress", help="Run type-aware compression on a single file"
    )
    p_compress.add_argument("--goal", default="", help="Task goal string")
    p_compress.add_argument("file", help="Path to file to compress")
    p_compress.set_defaults(func=_cmd_compress)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
