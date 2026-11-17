# Token Optimizer Plugin

**Version:** 1.0.0  
**Author:** Aveek Sengupta (<aveekforyou@gmail.com>)  
**License:** public  

A local-first, prompt-only, end-to-end token-optimization toolkit for VS Code Copilot. It attacks both halves of a turn's token cost:

- **Input side** — compress large workspace context fed INTO the agent into a reversible, traceable context pack (`temp/context_pack_vN/`), so the agent reasons over compressed context with full source traceability.
- **Output side** — rewrite the agent's own replies coming OUT into lean, high-signal language ("Shrink the mouth, not the brain").

One inviolable invariant spans both sides: **code, commands, file paths / URLs / identifiers, error & log lines, and numbers / versions stay byte-for-byte exact**. Everything runs as prompt instructions + deterministic stdlib Python helpers — no network calls, no telemetry, no external LLM APIs. The agent is the LLM.

---

## Components

### Three Skills + Three Agents

| Component | Kind | Side | Role |
| :--- | :--- | :--- | :--- |
| `token-optimizer` | skill | input+output | Combined entrypoint; activates both sides; delegates all real work to the two sibling skills, adds no new compression logic. Supports one-shot and session mode. |
| `input-token-optimizer` | skill | input | Builds the context pack (5 artifacts) under `temp/context_pack_vN/`. |
| `output-token-optimizer` | skill | output | Lean output-style rewriter + companion actions (`speak`, `lean-commit`, `lean-review`, `lean-compress-file`). |
| `token-optimizer-agent` | agent | input+output | Thin wrapper → `token-optimizer` skill → combined YAML verdict. |
| `input-token-optimizer-agent` | agent | input | Thin wrapper → `input-token-optimizer` skill → input YAML verdict. |
| `output-token-optimizer-agent` | agent | output | Thin wrapper → `output-token-optimizer` skill → output YAML verdict. |

---

## Input-Side Compression Modes & Savings Bands

| Mode | Behaviour | Savings Band |
| :--- | :--- | :--- |
| `quick` | Aggressive compression, precision over coverage | 60–80% |
| `balanced` (default) | Blend of coverage and compression | 40–60% |
| `lossless` | Broader detail retention, lower savings | 20–40% |

### Required Input Artifacts (`temp/context_pack_vN/`)
1. `context_pack.md` — task-focused compressed context (human-readable).
2. `context_manifest.json` — reversible chunk → source mapping (`100%` manifest coverage).
3. `context_retrieval_index.json` — tag/symbol/file/time lookup.
4. `context_stats.md` — compression statistics + confidence metrics.
5. `context_pack_reasoning_log.md` — audit trail of compression decisions.

---

## Output-Side Compression Levels

| Level | Behaviour | Example |
| :--- | :--- | :--- |
| `lite` | Full sentences; no preamble/hedging/question-restatement | `"Wrap the object in useMemo; a new reference is created every render."` |
| `full` (default) | Sentence fragments, imperative voice, minimal connectives | `"New ref each render. Wrap object in useMemo."` |
| `ultra` | Telegraphic fragments, symbols over words | `"New ref/render — useMemo it."` |

Say `normal mode`, `verbose`, or `stop terse` at any time to revert.

---

## Runtime Requirements & Testing

- **Python 3.9+** (stdlib only — no third-party packages, no `pip install` required).
- Run the full aggregate test suite (33 tests across both sibling suites) from the plugin root:

```bash
python skills/token-optimizer/assets/tests/run_all_tests.py
```
