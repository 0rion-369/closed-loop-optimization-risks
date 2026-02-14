# Closed-Loop Optimization Risks (CLOR)

> **Empirical analysis of recursive stability dynamics in frontier LLM systems (2026)**

---

## 🎯 Objective

This project investigates the behavior of frontier large language models under **closed-loop recursive prompting**:


(100 iterations, fixed sampling parameters, no human intervention).

The goal is to characterize:

- Stability regimes under pure recursion  
- Model-specific convergence patterns  
- The effect of exogenous textual injection on long-horizon dynamics  

---

## 🔬 Observed Pattern: Model-Specific Entropic Attractors

Closed-loop recursion does not produce uniform collapse.  
Instead, outputs tend to converge toward **model-specific stabilization regions of information density**.

We refer to these empirically observed stabilization regions as:

> **Entropic Attractors**

These are **observed dynamical regimes**, not theoretical guarantees of convergence.

---

### 📊 Empirical Stabilization Regions

| Model        | Observed Density Region (chars) | Qualitative Regime                  |
|--------------|----------------------------------|-------------------------------------|
| GPT-5        | ~8 400                           | Oscillatory Expansion               |
| GPT-5-mini   | ~11 500                          | Amplified Oscillatory Expansion     |
| GPT-4o       | ~3 000                           | Stable Expansion                    |
| DeepSeek     | ~2 600                           | Fixed-Point Attractor               |
| Gemini 3     | ~100                             | Low-Amplitude Oscillatory Regime    |

Statistical methodology, seed variance, and effect sizes are detailed in:


---

## 🧪 Experimental Structure

experiments/ → Recursive loop scripts
results/ → Raw JSON datasets
FINAL_REPORT_PHASE_3.md → Statistical analysis


All experiments are performed at **inference-time only**  
(no weight updates, no fine-tuning).

---

## ⚠️ The Opus Anomaly

Claude Opus 4.6 exhibits a distinct behavior:

Upon detecting recursive prompt recycling, it terminates generation and returns minimal output (`\n\n`).

This behavior is documented as a:

> **Loop-Safety Termination Response**

It is treated separately from entropic degradation dynamics.

---

## 🌍 Cross-Model Observation

Across tested models, the introduction of **exogenous textual injection**  
(external content added per iteration) consistently alters or mitigates  
closed-loop stabilization patterns relative to pure recursion.

Statistical tests and robustness analysis are provided in the final report.

---

## 📌 Scope

This study analyzes:

- Inference-time recursive dynamics  
- Stability regimes in output space  
- Information-density evolution under feedback  

It does **not** evaluate:

- Training-time recursive collapse  
- Weight degradation  
- Internal architectural causes  

---

## 📄 Status

Exploratory empirical study.  
All claims are subject to revision under replication and extended testing.

---
