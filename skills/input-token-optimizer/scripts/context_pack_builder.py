from __future__ import annotations

import re
from pathlib import Path

CHARS_PER_TOKEN = 4


class ChunkMetadata:
    def __init__(
        self,
        chunk_id: str,
        summary_text: str,
        source_file: str,
        source_line_start: int,
        source_line_end: int,
        confidence: str,
        tags: list[str],
        char_count: int | None = None,
        token_estimate: int | None = None,
    ) -> None:
        self.chunk_id = chunk_id
        self.summary_text = summary_text
        self.source_file = source_file
        self.source_line_start = source_line_start
        self.source_line_end = source_line_end
        self.confidence = confidence
        self.tags = list(tags)
        self.char_count = len(summary_text) if char_count is None else char_count
        self.token_estimate = (
            max(1, self.char_count // CHARS_PER_TOKEN)
            if token_estimate is None
            else token_estimate
        )


class ContextPackStats:
    def __init__(
        self,
        raw_chars: int,
        raw_tokens_estimate: int,
        compressed_chars: int,
        compressed_tokens_estimate: int,
        compression_ratio: float,
        savings_percent: float,
        high_confidence_count: int = 0,
        medium_confidence_count: int = 0,
        low_confidence_count: int = 0,
    ) -> None:
        self.raw_chars = raw_chars
        self.raw_tokens_estimate = raw_tokens_estimate
        self.compressed_chars = compressed_chars
        self.compressed_tokens_estimate = compressed_tokens_estimate
        self.compression_ratio = compression_ratio
        self.savings_percent = savings_percent
        self.high_confidence_count = high_confidence_count
        self.medium_confidence_count = medium_confidence_count
        self.low_confidence_count = low_confidence_count

    @property
    def low_confidence_percent(self) -> float:
        total = (
            self.high_confidence_count
            + self.medium_confidence_count
            + self.low_confidence_count
        )
        if total == 0:
            return 0.0
        return round(self.low_confidence_count / total * 100, 1)


class ArtifactRanker:
    def __init__(self, goal: str) -> None:
        self.goal = goal.lower()
        self.goal_tokens = set(re.findall(r"\b\w+\b", self.goal))

    def score_file(self, path: str | Path, content_snippet: str = "") -> float:
        p = Path(path)
        filename = p.name.lower()
        suffix = p.suffix.lower()
        score = 0.0

        if self.goal and self.goal in filename:
            score += 50.0
        for token in self.goal_tokens:
            if token in filename:
                score += 10.0

        if content_snippet:
            content_lower = content_snippet.lower()
            if self.goal and self.goal in content_lower:
                score += 5.0
            for token in self.goal_tokens:
                if token in content_lower:
                    score += 2.0

        if suffix in (".log", ".txt") and (
            self.goal_tokens & {"error", "debug", "triage"}
        ):
            score += 15.0
        elif suffix == ".sql" and (self.goal_tokens & {"migration", "query"}):
            score += 15.0
        elif suffix in (".py", ".ts", ".js") and (
            self.goal_tokens & {"code", "review"}
        ):
            score += 12.0
        elif suffix in (".md", ".txt") and (self.goal_tokens & {"spec", "doc"}):
            score += 10.0
        elif suffix in (".json", ".yaml", ".yml") and (
            self.goal_tokens & {"config", "schema"}
        ):
            score += 10.0

        return score


class TypeAwareCompressor:
    _CODE_DEF_RE = re.compile(r"^\s*(def|class|async def)\s+\w+")
    _CODE_TODO_RE = re.compile(r"(TODO|FIXME|BUG|HACK):", re.IGNORECASE)
    _CODE_FLOW_RE = re.compile(
        r"^\s*(if|elif|for|while|try|except|finally|raise|return)\b"
    )

    _LOG_LEVEL_RE = re.compile(
        r"(ERROR|WARN|FATAL|Exception|Traceback)", re.IGNORECASE
    )
    _LOG_STACK_RE = re.compile(r'^\s+at |File ".*", line \d+')
    _LOG_META_RE = re.compile(
        r"\d{2}:\d{2}:\d{2}|correlation_id|request_id|session_id"
    )

    _SQL_SELECT_RE = re.compile(r"SELECT\s+(.*?)\s+FROM", re.IGNORECASE | re.DOTALL)
    _SQL_JOIN_RE = re.compile(
        r"(FROM|JOIN|INNER JOIN|LEFT JOIN|RIGHT JOIN)\s+(\w+)", re.IGNORECASE
    )
    _SQL_WHERE_RE = re.compile(
        r"WHERE\s+(.*?)(?:GROUP BY|ORDER BY|$)", re.IGNORECASE | re.DOTALL
    )

    _MD_HEADING_RE = re.compile(r"^#+\s+")
    _MD_KEYWORDS_RE = re.compile(
        r"requirement:|decision:|assumption:|constraint:|question:|note:|risk:"
    )
    _MD_LIST_RE = re.compile(r"^\s*[-*+]\s+.{5,}")

    _JY_KEY_RE = re.compile(r"^\s{0,4}([\w-]+):\s*")
    _JY_LIST_RE = re.compile(r"^\s*-\s+")

    @staticmethod
    def compress_code(
        lines: list[str], goal: str = ""
    ) -> list[tuple[int, int, str]]:
        chunks: list[tuple[int, int, str]] = []
        for i, line in enumerate(lines):
            if (
                TypeAwareCompressor._CODE_DEF_RE.search(line)
                or TypeAwareCompressor._CODE_TODO_RE.search(line)
                or TypeAwareCompressor._CODE_FLOW_RE.search(line)
            ):
                chunks.append((i, i, line.strip()))
        return chunks

    @staticmethod
    def compress_log(
        lines: list[str], goal: str = ""
    ) -> list[tuple[int, int, str]]:
        chunks: list[tuple[int, int, str]] = []
        for i, line in enumerate(lines):
            if (
                TypeAwareCompressor._LOG_LEVEL_RE.search(line)
                or TypeAwareCompressor._LOG_STACK_RE.search(line)
                or TypeAwareCompressor._LOG_META_RE.search(line)
            ):
                chunks.append((i, i, line.strip()))
        return chunks

    @staticmethod
    def compress_sql(
        lines: list[str], goal: str = ""
    ) -> list[tuple[int, int, str]]:
        joined = "\n".join(lines)
        chunks: list[tuple[int, int, str]] = []

        select_match = TypeAwareCompressor._SQL_SELECT_RE.search(joined)
        if select_match:
            chunks.append((0, 0, f"SELECT: {select_match.group(1).strip()[:100]}"))

        for join_match in TypeAwareCompressor._SQL_JOIN_RE.finditer(joined):
            chunks.append(
                (0, 0, f"{join_match.group(1).upper()}: {join_match.group(2)}")
            )

        where_match = TypeAwareCompressor._SQL_WHERE_RE.search(joined)
        if where_match:
            chunks.append((0, 0, f"WHERE: {where_match.group(1).strip()[:100]}"))

        return chunks

    @staticmethod
    def compress_markdown(
        lines: list[str], goal: str = ""
    ) -> list[tuple[int, int, str]]:
        chunks: list[tuple[int, int, str]] = []
        for i, line in enumerate(lines):
            lower = line.lower()
            if (
                TypeAwareCompressor._MD_HEADING_RE.search(line)
                or TypeAwareCompressor._MD_KEYWORDS_RE.search(lower)
                or TypeAwareCompressor._MD_LIST_RE.search(line)
            ):
                chunks.append((i, i, line.strip()))
        return chunks

    @staticmethod
    def compress_json_yaml(
        lines: list[str], goal: str = ""
    ) -> list[tuple[int, int, str]]:
        chunks: list[tuple[int, int, str]] = []
        for i, line in enumerate(lines):
            if TypeAwareCompressor._JY_KEY_RE.search(line):
                chunks.append((i, i, line.strip()))
            if TypeAwareCompressor._JY_LIST_RE.search(line):
                chunks.append((i, i, line.strip()))
        return chunks


def build_manifest(
    chunks: list[tuple[int, int, str]],
    source_file: str,
    file_type: str,
    goal: str,
) -> list[ChunkMetadata]:
    stem = Path(source_file).stem
    goal_lower = goal.lower()
    manifest: list[ChunkMetadata] = []

    for idx, (start, end, summary) in enumerate(chunks):
        chunk_id = f"{stem}_{file_type}_{idx:03d}"
        summary_lower = summary.lower()

        if any(k in summary_lower for k in ("error", "exception", "todo")):
            confidence = "high"
        else:
            confidence = "medium"

        tags: list[str] = []
        if "error" in summary_lower:
            tags.append("error")
        if "todo" in summary_lower or "fixme" in summary_lower:
            tags.append("todo")
        if goal_lower and goal_lower in summary_lower:
            tags.append("goal-relevant")

        char_count = len(summary)
        token_estimate = max(1, char_count // CHARS_PER_TOKEN)

        manifest.append(
            ChunkMetadata(
                chunk_id=chunk_id,
                summary_text=summary,
                source_file=source_file,
                source_line_start=start + 1,
                source_line_end=end + 1,
                confidence=confidence,
                tags=tags,
                char_count=char_count,
                token_estimate=token_estimate,
            )
        )

    return manifest


def compute_stats(
    raw_chars: int,
    compressed_chars: int,
    manifest: list[ChunkMetadata] | None = None,
) -> ContextPackStats:
    raw_tokens = max(1, raw_chars // CHARS_PER_TOKEN)
    compressed_tokens = max(1, compressed_chars // CHARS_PER_TOKEN)
    ratio = compressed_tokens / raw_tokens
    savings_percent = (1 - ratio) * 100

    high_count = 0
    medium_count = 0
    low_count = 0

    if manifest is not None:
        for item in manifest:
            if item.confidence == "high":
                high_count += 1
            elif item.confidence == "low":
                low_count += 1
            else:
                medium_count += 1

    return ContextPackStats(
        raw_chars=raw_chars,
        raw_tokens_estimate=raw_tokens,
        compressed_chars=compressed_chars,
        compressed_tokens_estimate=compressed_tokens,
        compression_ratio=ratio,
        savings_percent=savings_percent,
        high_confidence_count=high_count,
        medium_confidence_count=medium_count,
        low_confidence_count=low_count,
    )
