---
name: token-optimizer
description: Combined end-to-end token optimization entrypoint that activates BOTH sides at once — input-side workspace context compression and output-side lean reply compression. Supports one-shot and session mode.
argument-hint: "[goal=<text> scope_paths=<paths>] [mode=quick|balanced|lossless] [level=lite|full|ultra] [session=on|off]"
---

# token-optimizer (Combined Entrypoint)

> **You (Copilot) are the LLM for this skill. Do not call external LLM APIs, make network requests, or emit telemetry. This skill delegates all real work to `input-token-optimizer` and `output-token-optimizer` and adds no new compression logic of its own.**

## 1. Inputs

| Input | Required | Applies to | Default | Values |
| :--- | :--- | :--- | :--- | :--- |
| `goal` | yes (one-shot) | input | — | free text (task objective) |
| `scope_paths` | yes (one-shot) | input | — | one or more folders/files |
| `mode` | no | input | `balanced` | `quick`, `balanced`, `lossless` |
| `level` | no | output | `full` | `lite`, `full`, `ultra` |
| `max_files`, `max_chars`, `include_patterns`, `exclude_patterns` | no | input | see `input-token-optimizer` | ingestion controls |

## 2. One-Shot Procedure

1. **Turn on the output side first** (so every subsequent reply is lean) — follow `skills/output-token-optimizer/SKILL.md` at the requested `level` (default `full`); persists for the session until `"normal mode"`.
2. **Run the input side** — follow `skills/input-token-optimizer/SKILL.md` with `goal`, `scope_paths`, `mode`; write all 5 required outputs under a new `temp/context_pack_vN/`.
3. **Report in lean style** — emit the input-side savings summary (raw vs compressed token estimate, ratio, savings %, low-confidence %) as a tight list; note output-side compression is now active.

## 3. Session Mode (Keep Both On for the Whole Chat)

- **Turn on:** `token-optimizer session on` (optionally with `level=` / `mode=`).
- **Output side:** Always on at the active `level` (session-sticky).
- **Input side:** Applied on demand, automatically: before any large/multi-file task (multi-file review, migration/debug triage, repeated runs over the same area) build or refresh a pack for the inferred scope at the active `mode` and reason over the pack. Reuse the latest `temp/context_pack_vN/` when scope is unchanged; build `vN+1` only when scope/goal changes; skip for trivial single-file edits or trivial questions. Infer `scope_paths` / `goal` from the task; ask only if genuinely ambiguous.
- **Banner:** State the activation banner once, not every turn.
- **Change mid-session:** `token-optimizer session level=ultra` / `token-optimizer session mode=quick`.
- **Turn off:** `token-optimizer session off`, `normal mode`, `verbose`, or `stop terse` — stop both sides; context packs already on disk stay.

## 4. Invariants (Restated, Never Overridden Here)

- **Output side:** Code, commands, paths/URLs/identifiers, error/log lines, numbers/versions stay byte-for-byte exact.
- **Input side:** Every retained chunk maps to a source file + 1-based line range (`context_manifest.json`); no invented facts.
