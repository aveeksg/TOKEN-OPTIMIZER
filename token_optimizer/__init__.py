from __future__ import annotations

from token_optimizer.context_pack_builder import (
    CHARS_PER_TOKEN,
    ArtifactRanker,
    ChunkMetadata,
    ContextPackStats,
    TypeAwareCompressor,
    build_manifest,
    compute_stats,
)
from token_optimizer.lean_stats import (
    count_chars,
    estimate_tokens,
    extract_protected_spans,
    savings_report,
    verify_invariants,
)

__version__ = "1.0.0"

__all__ = [
    "__version__",
    "CHARS_PER_TOKEN",
    "ChunkMetadata",
    "ContextPackStats",
    "ArtifactRanker",
    "TypeAwareCompressor",
    "build_manifest",
    "compute_stats",
    "count_chars",
    "estimate_tokens",
    "extract_protected_spans",
    "verify_invariants",
    "savings_report",
]
