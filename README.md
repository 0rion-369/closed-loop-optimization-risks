# Closed-Loop Optimization Risks (CLOR)

> Measuring Entropic Stability in Recursive LLM Systems — 10 models, 3 families (2026).

## 🎯 Objective
Map the degradation modes of frontier LLMs under closed-loop 
recursive feedback (output → input, 100 iterations, no human 
intervention). Validate whether exogenous injection universally 
prevents collapse.

## 🏆 Core Discovery: The Entropic Attractor
Under closed-loop conditions, models do not simply explode or 
freeze — they stabilize around model-specific attractors of 
information density with distinct dynamical signatures:

| Model     | Attractor (chars) | Mode                    |
|-----------|-------------------|-------------------------|
| GPT-5     | ~8 400            | Expansion Oscillante    |
| GPT-5-mini| ~11 500           | Exp. Oscillante Amplifiée|
| GPT-4o    | ~3 000            | Expansion Stable        |
| DeepSeek  | ~2 600            | Attracteur Fixe         |
| Gemini 3  | ~100              | Micro-Oscillation       |

## 📂 Structure
* `experiments/`: Recursive loop scripts (the "Forge")
* `results/`: Raw JSON datasets
    * `gpt5_final_validation.json`: GPT-5 + GPT-5-mini (1 000 records, 5 seeds × 100 iter each)
    * `opus_final_validation.json`: The Safety Collapse documentation
* `FINAL_REPORT_PHASE_3.md`: Full statistical analysis

## ⚠️ The Opus Anomaly
**Claude Opus 4.6** triggers a Loop-Safety Mechanism upon 
detecting recursive prompt recycling, returning `\n\n` after 
a single substantive response. Documented as **Retrait 
Épistémique** — the only model that refuses participation 
rather than exhibiting entropic degradation.

## 🔬 Universal Finding
Exogenous injection (external text introduced per iteration) 
prevents collapse across all tested models (Sonnet, Haiku, 
Grok, DeepSeek). Confirmed p < 0.001.

---
*Marc-Olivier Corbin — 2026*
