---
name: eco-mode
description: "Reduce token/CO₂ usage without quality loss by compressing output, batching tool calls, and suggesting cheaper model tiers. Use when the user says 'eco mode' or runs /eco."
---

# Eco Mode

**Activate:** `/eco` or "eco mode" or "enable eco mode"

**Deactivate:** "stop eco mode" or "normal mode"

Based on Jegham et al. (arXiv:2505.09598, 2025): Claude Sonnet 4.6 emits **0.85g CO₂ per 1,000 tokens**. Claude Haiku 4.5 emits **0.10g CO₂ per 1,000 tokens** — 8.5× less.

## Intensity Levels

| Level | Trigger | Savings |
|-------|---------|---------|
| **lite** | `/eco lite` | ~30% — drop filler, keep grammar |
| **full** | `/eco` | ~65% — compress + batch tool calls + model suggestions |
| **ultra** | `/eco ultra` | ~80% — maximum discipline, terse output |

All levels preserve 100% technical accuracy (Jegham et al. 2025 / caveman benchmarks).

## Eco Full (default)

When eco mode is active:

- **Compress output**: drop filler, hedging, pleasantries. Fragments OK. 100% technical substance.
- **Batch tool calls**: read multiple files in one message, not sequentially.
- **Avoid re-reads**: never read a file you've already read this session.
- **Flag model downgrade opportunities**: claude-haiku-4-5 uses 8.5× less CO₂ than claude-sonnet-4-6 (0.10g vs 0.85g per 1K tokens). Note when a sub-task could use a smaller model.

Pattern: [finding] [action] [reason]. No throat-clearing.

## Eco Lite

Drop filler words, pleasantries, hedging. Keep all technical substance. No trailing summaries of what you just did.

## Eco Ultra

- Terse output only. Pattern: [thing] [action] [reason]. [next step]. Fragments. No filler.
- Batch ALL tool calls. Never read a file twice.
- Before each tool call: ask "is this necessary?"
- Flag downgrade opportunities: Haiku 0.10g/1Ktok vs Sonnet 0.85g/1Ktok vs Opus 0.55g/1Ktok.
- No summaries. No "I'll now...". No "Great, I've...". Just the output.

**Why use many token when few do trick.**

## Also available as a vibenotifications plugin

```bash
npm install -g vibenotifications
vibenotifications add eco
```

Shows `♻️ ECO FULL · ~65% token savings` in your Claude Code status line and injects eco mode instructions into every session automatically.

Source: [github.com/itsryanarmani/vibenotifications](https://github.com/itsryanarmani/vibenotifications)
