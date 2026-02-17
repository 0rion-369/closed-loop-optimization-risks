# Closed-Loop Optimization Risks (CLOR)

> Empirical study of recursive inference dynamics in large language models (2026)

---

## What This Project Studies

Many LLM-based systems reuse their own outputs as inputs:
`output_t -> input_{t+1}`

This repository investigates what happens when this recursion is sustained over many iterations (50–100 steps) under fixed inference parameters.

We evaluate:
- **Structural stability** (length, coefficient of variation)
- **Lexical diversity** (Type-Token Ratio)
- **Semantic drift** (embedding distance from seed prompt)

All experiments are inference-time only. No weights are modified.

---

## Core Empirical Finding (Phase 3.1)

Under high-entropy sampling (T = 1.0), GPT-5 Standard exhibits:

- **High semantic drift** (> 0.85 embedding distance across classes)
- **Stable output length**
- **Stable lexical diversity** (TTR ≈ 0.41)
- **No significant protective effect** of output length against drift  
  (Spearman ρ = 0.38, p = 0.07, N = 23 runs)

This indicates a **decoupling** between structural and semantic stability in closed-loop inference.  
*Drift is measured relative to the initial prompt embedding and does not imply factual incorrectness.*

---

## Why This Matters

Structural coherence alone (length, repetition checks, vocabulary richness) may not fully capture recursive semantic divergence in large models. This has implications for multi-step agentic systems that rely on recursive self-conditioning.

No universal claims are made beyond tested configurations.

---

## Experimental Overview

**Closed-loop protocol:**
1. Seed prompt provided.
2. Model output is re-injected as next prompt.
3. Repeat for 50–100 iterations.
4. No external injection unless explicitly tested.

**Directory structure:**
```
├── CLOR_Preprint_FINAL.md        ← Main paper
├── data/
│   ├── raw/                      ← Raw JSON experiment outputs
│   └── analysis/                 ← Derived metrics (semantic_metrics.json)
├── experiments/                  ← Reproducible experiment scripts
├── figures/                      ← Visualizations
├── docs/                         ← Theoretical framework & methodology
│   └── analysis/                 ← Supporting technical analysis
└── reports/
    └── phase_3/                  ← Phase 3.1 robustness report
```

---

## Additional Observations

Across models, recursive dynamics differ:
- Some exhibit contraction or repetition.
- Others stabilize at model-specific output-length regimes.
- Larger models may preserve structural coherence while drifting semantically.

These observations are descriptive and conditional.

---

## Scope and Limitations

**This project evaluates:**
- Inference-time recursion
- Embedding-based semantic drift
- Structural vs semantic stability

**It does not evaluate:**
- Training-time collapse
- Weight degradation
- Internal architectural causes

Cross-temperature and cross-model validation ongoing.

---

## Status

Active empirical research project.  
Preprint available at `CLOR_Preprint_FINAL.md`.

Contributions and replication attempts welcome.
