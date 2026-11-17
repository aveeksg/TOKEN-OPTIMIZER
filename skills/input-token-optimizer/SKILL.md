---
name: input-token-optimizer
description: Local-first context compression and retrieval workflow that turns large workspace scope into a reversible, traceable context pack under temp/context_pack_vN/.
argument-hint: "goal=<text> scope_paths=<paths> [mode=quick|balanced|lossless] [max_files=200] [max_chars=800000] [include_patterns=...] [exclude_patterns=...]"
---

# input-token-optimizer

> **You (Copilot) are the LLM for this skill. Do not call external LLM APIs, make network requests, or upload workspace content.**

## 1. Inputs (and `references/contract.yaml` bounds)

| Input | Required | Default | Contract constraints |
| :--- | :--- | :--- | :--- |
| `goal` | yes | — | `string`, `minLength: 5`, `maxLength: 200` |
| `scope_paths` | yes | — | `array[string]`, `minItems: 1` |
| `mode` | no | `balanced` | `enum`: `quick`, `balanced`, `lossless` |
| `max_files` | no | `200` | `integer`, `min: 1`, `max: 5000` |
| `max_chars` | no | `800000` | `integer`, `min: 10000`, `max: 10000000` |
| `include_patterns` | no | `[]` | `array[string]` glob includes |
| `exclude_patterns` | no | `[]` | `array[string]` glob excludes |

## 2. Required Output Artifacts (under `temp/context_pack_vN/`)

Exactly five artifacts, all `required: true` in `references/contract.yaml`:

1. `context_pack.md` — task-focused compressed context (human-readable), `100`–`500000` bytes.
2. `context_manifest.json` — reversible chunk → source mapping, `50`–`5000000` bytes.
3. `context_retrieval_index.json` — tag/symbol/file/time lookup, `50`–`2000000` bytes.
4. `context_stats.md` — compression statistics + confidence, `100`–`100000` bytes.
5. `context_pack_reasoning_log.md` — audit trail of decisions, `50`–`500000` bytes.

## 3. Six-Step Procedure (Prompt Contract)

1. **Scope & inventory** — resolve `scope_paths`; discover candidate files with `include_patterns`/`exclude_patterns` filters; rank by relevance to `goal` using lexical filename + content hints (`ArtifactRanker`); build an inventory (`path`, `type`, `size`, `relevance_score`); stop ingestion at `max_files` or `max_chars`.
2. **Type-aware compression** — deterministic extraction by file type (`TypeAwareCompressor`):
   - **Code:** signatures (`def`, `class`, `async def`), control-flow pivots (`if`, `elif`, `for`, `while`, `try`, `except`, `finally`, `raise`, `return`), `TODO`/`FIXME`/`BUG`/`HACK`, error paths, interfaces.
   - **Logs:** `ERROR`, `WARN`, `FATAL`, `Exception`, `Traceback`, stack frames (`at `, `File "...", line N`), timestamps (`HH:MM:SS`), correlation/request/session IDs; collapse repetition.
   - **SQL:** `SELECT` columns, `FROM`/`JOIN` tables, `WHERE` filters, grouping, ordering.
   - **Docs:** headings (`#`), requirements, decisions, assumptions, constraints, questions, notes, risks, and substantive list items.
   - **JSON/YAML:** top-level key structure + goal-relevant list items; collapse long arrays.
   Assign a unique `chunk_id` to every retained statement.
3. **Reversible mapping** — write `context_manifest.json` (`build_manifest`), one entry per chunk: `chunk_id`, `summary_text`, `source_file`, `source_line_start` (1-based), `source_line_end` (1-based), `confidence` (`high` | `medium` | `low`), `tags`, `char_count`, `token_estimate`. **No chunk may appear in `context_pack.md` without a matching manifest record (`100%` manifest coverage).**
4. **Retrieval index** — write `context_retrieval_index.json` with `by_tag`, `by_file`, `by_symbol`, `by_time`.
5. **Savings & quality report** — write `context_stats.md` (`compute_stats`): raw vs compressed char count; token estimates via `tokens ≈ chars / 4` (`CHARS_PER_TOKEN = 4`); compression ratio (`compressed_tokens / raw_tokens`); estimated savings %; low-confidence risk notes; recommended next action.
6. **Final context pack** — write `context_pack.md` with sections in exact order:
   1. `Task Goal`
   2. `High-Signal Summary`
   3. `Critical Findings`
   4. `Known Unknowns`
   5. `Suggested Investigation Order`
   6. `Retrieval Instructions`
   Use terse, actionable language.

## 4. Modes & Stated Savings Bands

| Mode | Behaviour | Savings Band |
| :--- | :--- | :--- |
| `quick` | Aggressive compression, precision over coverage | 60–80% |
| `balanced` (default) | Blend of coverage and compression | 40–60% |
| `lossless` | Broader detail retention, lower savings | 20–40% |

## 5. Guardrails & Validation Thresholds

- **Local-first only:** Never upload content or call external APIs.
- **No invented facts:** Every claim in `context_pack.md` maps to a source file and 1-based line range in `context_manifest.json`.
- **Uncertainty & confidence gating:** Flag low-confidence chunks; warn when `low_confidence_percent > 20%` and recommend targeted re-ingestion when critical confidence is low.
- **Contract thresholds (`references/contract.yaml`):**
  - `manifest_coverage`: `100%`
  - `min_compression_ratio`: `0.3`
  - `max_low_confidence_percent`: `20`
  - `min_chunk_count`: `5`
  - `max_chunk_count`: `1000`
