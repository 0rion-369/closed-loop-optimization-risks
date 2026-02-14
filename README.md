# Closed-Loop Optimization Risks (CLOR)

> Mapping stability dynamics in recursive LLM systems (2026).

## Objective

Study the degradation modes of frontier LLMs under closed-loop
recursive feedback (output → input, 100 iterations, no human intervention),
and evaluate whether exogenous injection mitigates collapse dynamics.

## Observed Pattern: Model-Specific Entropic Attractors

Under closed-loop conditions, models tend to stabilize around
model-specific regions of information density, exhibiting
distinct dynamical signatures rather than uniform collapse.

| Model      | Observed Density Region (chars) | Qualitative Mode            |
|------------|----------------------------------|-----------------------------|
| GPT-5      | ~8 400                           | Oscillatory Expansion       |
| GPT-5-mini | ~11 500                          | Amplified Oscillation       |
| GPT-4o     | ~3 000                           | Stable Expansion            |
| DeepSeek   | ~2 600                           | Fixed-Point Attractor       |
| Gemini 3   | ~100                             | Micro-Oscillation Collapse  |

These regions are empirically observed stabilization zones
under fixed-parameter recursive prompting.
See `FINAL_REPORT_PHASE_3.md` for statistical details.

## Structure

- `experiments/`: Recursive loop scripts
- `results/`: Raw JSON datasets
- `FINAL_REPORT_PHASE_3.md`: Statistical analysis

## The Opus Anomaly

Claude Opus 4.6 terminates recursion after detecting prompt recycling,
returning minimal outputs (`\n\n`). This behavior is documented
as a loop-safety response rather than entropic degradation.

## Cross-Model Observation

Across tested models, exogenous injection consistently
reduces collapse dynamics relative to pure closed-loop runs.

Statistical methods and effect sizes are detailed in the final report.
