# Closed-Loop Optimization Risks (CLOR): Mapping Stability Dynamics in Recursive LLM Systems
**Across 10 Models and 3 Families**

**Author:** Marc-Olivier Corbin (Independent Researcher)
**Date:** February 2026
**Repository:** [github.com/0rion-369/closed-loop-optimization-risks](https://github.com/0rion-369/closed-loop-optimization-risks)
**Status:** *Preliminary Preprint / Draft*

---

## Abstract
We investigate the degradation dynamics of ten frontier large language models (LLMs) under closed-loop recursive feedback, where model output is reinjected as input for 100 iterations without human intervention. Experiments were conducted across three families: Anthropic (Sonnet, Haiku, Opus 4.6), Google DeepMind (Gemini 3 Pro/Flash), and OpenAI (GPT-4o, GPT-5, GPT-5-mini), as well as xAI (Grok) and DeepSeek.

We characterize eight distinct stability regimes using Shannon entropy, Lempel-Ziv complexity, and length as primary metrics. Key findings include:
1.  **No convergence:** No model converges uniformly; each exhibits a specific dynamic range from fixed-point attenuation to oscillatory expansion.
2.  **Predictors:** Default response style is a stronger predictor of stability than model scale.
3.  **Exogenous Injection:** Introducing external text per iteration significantly mitigates collapse (Mann-Whitney U, p < 0.001).
4.  **Loop Safety:** Claude models exhibit a unique "loop-safe" state, terminating recursion after detecting prompt cycling.

**Keywords:** closed-loop optimization, LLM stability, Shannon entropy, recursive collapse, AI safety.

---

## 1. Introduction
Large language models increasingly operate in agentic configurations where their outputs influence subsequent inputs through tool use, multi-turn dialogue, and self-refinement loops. Understanding how models behave under sustained recursive feedback is therefore a practical safety concern.

The central question of this study is: *What happens to the content structure and diversity of LLMs when a model's response is recycled, verbatim, as the next prompt for 100 iterations?* Do they converge, collapse, or oscillate?

Prior work (Shumailov et al., 2023) established that training on generated data leads to model collapse. Our examination infers a real-time phenomenon: whether recursion without training induces analogous degradation in a single session.

## 2. Methodology
**2.1 Experimental Design**
We followed a strict protocol:
* **Condition:** $P_{t+1} = M(P_t) + E$ (where $E$ is optional external text).
* **Seeds:** Ten seed prompts (SEED_PROMPTS) run for 100 iterations.
* **Parameters:** Temperature 0.8, Top-p 0.9, Max tokens 500.
* **API:** All tests run via official APIs between Jan and Feb 2026.

**2.2 Metrics**
* **Shannon Entropy (H):** Character-level information density (bits/char).
* **Lempel-Ziv Complexity (LZ):** Normalized algorithmic complexity; detects repetition.
* **Length:** Trend analysis (slope) over iterations.

## 3. Results & Taxonomy of Modes

We identified specific behaviors across the tested models.

| Model | Family | Shannon (H) Mean | Behavior / Regime | Note |
| :--- | :--- | :--- | :--- | :--- |
| **Sonnet 3.7** | Anthropic | 4.383 | Bruit Structurel (Structural Noise) | High stability |
| **Haiku 3.5** | Anthropic | 4.367 | Attracteur Rigide (Rigid Attractor) |  |
| **Opus 4.6** | Anthropic | - | Loop-Safety Termination | Detects loops and stops |
| **Grok 3** | xAI | 4.84 | Expansion Récursive | Chaotic expansion (~8K-11K chars) |
| **DeepSeek** | DeepSeek | 4.604 | Fixe / Stable | |
| **Gemini 3 Pro** | Google | 4.28 | Micro-Oscillation | Anomalously short, stable cycles (~100 chars) |
| **Gemini 3 Flash**| Google | 4.31 | Micro-Oscillation | Similar to Pro |
| **GPT-4o** | OpenAI | 4.42 | Stable | |

### Key Observations
* **Gemini 3 (Pro/Flash):** Exhibits a "Micro-Oscillation" regime. The outputs become very short (~100 chars) and highly stable (H ~4.28), acting as a "safe mode."
* **Grok:** Exhibits "Recursive Expansion." The model tends to increase output length significantly, leading to high entropy (H=4.84) and "hallucinatory" drift.
* **Anthropic:** Claude Opus 4.6 demonstrated a unique safety feature, refusing to continue the loop after detecting the pattern ("Loop-safety terminated").

## 4. Mitigation: Exogenous Injection
We tested the introduction of random external text ("entropy injection") into the loop.
* **Result:** This significantly mitigated collapse across 4 distinct models.
* **Statistical Significance:** Confirmed via Mann-Whitney U test (p < 0.001).
* **Sonnet H-Value:** Improved from 4.341 (Closed-Loop) to 4.383 (Exogenous).

## 5. Implications
The results suggest that "Agentic" systems require active entropy management. Purely recursive loops without external grounding (exogenous data) tend towards either rigid simplification (Gemini) or chaotic expansion (Grok). Mathematical safeguards or "loop-awareness" (as seen in Opus) may be necessary for future autonomous pipelines.

---
*Data available in the `/data` folder of this repository.*