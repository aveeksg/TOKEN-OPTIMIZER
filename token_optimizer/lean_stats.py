from __future__ import annotations

import re

CHARS_PER_TOKEN = 4

_FENCED_CODE = re.compile(r"```.*?```", re.DOTALL)
_INLINE_CODE = re.compile(r"`[^`\n]+`")
_URL = re.compile(r"https?://[^\s)]+")
_PATH = re.compile(
    r"""
    (?:
        [A-Za-z]:\\(?:[\w.-]+\\)*[\w.-]+
        | \.\.?[\\/](?:[\w.-]+[\\/])*[\w.-]+
        | (?<![\w:/])/(?:[\w.-]+/)+[\w.-]+
        | \b(?:[\w.-]+[\\/])+[\w.-]+\.[A-Za-z0-9]+\b
    )
    """,
    re.VERBOSE,
)
_VERSION = re.compile(r"\bv?\d+\.\d+(?:\.\d+)?(?:-[\w.]+)?\b")
_ERROR_TOKEN = re.compile(r"\b[A-Z][A-Za-z]*(?:Error|Exception|Warning)\b")

_PATTERNS = [
    _FENCED_CODE,
    _INLINE_CODE,
    _URL,
    _PATH,
    _VERSION,
    _ERROR_TOKEN,
]


def count_chars(text: str) -> int:
    return len(text)


def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    return round(len(text) / CHARS_PER_TOKEN)


def extract_protected_spans(text: str) -> list[str]:
    seen: set[str] = set()
    spans: list[str] = []
    for pattern in _PATTERNS:
        for match in pattern.finditer(text):
            span = match.group(0)
            if span not in seen:
                seen.add(span)
                spans.append(span)
    return spans


def verify_invariants(raw: str, lean: str) -> list[str]:
    missing: list[str] = []
    for span in extract_protected_spans(raw):
        if span not in lean:
            missing.append(span)
    return missing


def savings_report(raw: str, lean: str) -> dict[str, int | float | bool]:
    raw_chars = count_chars(raw)
    lean_chars = count_chars(lean)
    raw_tokens = estimate_tokens(raw)
    lean_tokens = estimate_tokens(lean)
    if raw_tokens == 0:
        reduction_percent = 0.0
    else:
        reduction_percent = round(
            (raw_tokens - lean_tokens) / raw_tokens * 100, 1
        )
    invariants_preserved = not verify_invariants(raw, lean)
    return {
        "raw_chars": raw_chars,
        "lean_chars": lean_chars,
        "raw_tokens": raw_tokens,
        "lean_tokens": lean_tokens,
        "reduction_percent": reduction_percent,
        "invariants_preserved": invariants_preserved,
    }
