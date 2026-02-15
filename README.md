# Closed-Loop Optimization Risks (CLOR)

> **Empirical analysis of recursive stability dynamics in frontier LLM systems (2026)**

---

## Abstract

Recursive self-conditioning is increasingly relevant in autonomous LLM pipelines. While prior work has examined collapse during recursive training, less attention has been given to inference-time recursive dynamics under fixed weights.

We empirically investigate ten frontier LLMs under closed-loop prompting (output → input, 100 iterations, fixed parameters). Across models, outputs converge toward model-specific stabilization regions of information density characterized by oscillatory or fixed-point dynamics. We refer to these empirical stabilization regimes as *entropic attractors*.

When exogenous textual injection is introduced at each iteration, these stabilization patterns are consistently altered or mitigated.

These findings suggest that recursive inference dynamics may induce stable low-dimensional regimes in output space, even in the absence of weight updates.

---

## 🎯 Objective

This project investigates the behavior of frontier large language models under **closed-loop recursive prompting**:

outputₜ → inputₜ₊₁

(100 iterations, fixed sampling parameters, no human intervention).

The goal is to characterize:

- Stability regimes under pure recursion  
- Model-specific convergence patterns  
- The effect of exogenous textual injection on long-horizon dynamics  

---

# 📈 Central Result

<p align="center">
  <img src="results/compressibility_divergence.png" width="80%">
</p>

<p align="center">
  <em>Example stabilization dynamics under closed-loop vs exogenous injection.</em>
</p>

Closed-loop recursion does not produce uniform collapse.  
Instead, outputs converge toward **model-specific stabilization regions of information density**.

---

## 🔬 Observed Pattern: Model-Specific Entropic Attractors

We define *entropic attractors* as empirically observed stabilization regions of output information density under fixed-parameter recursive prompting.

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

## 📅 Update: Phase 3.1 (February 2026)
**Robustness & Recovery Analysis**
New experiments focus on Temperature sensitivity (T=1.0) and the "Lazare Protocol" for system recovery.

* **Report:** [reports/phase_3/PHASE_3_1_ROBUSTNESS_REPORT.md](reports/phase_3/PHASE_3_1_ROBUSTNESS_REPORT.md)
* **Key Finding:** Exogenous injection is *prophylactic*, not *therapeutic*. Once semantic collapse sets in (approx iteration 4), the system cannot be recovered even with active injection.
* **New Mode:** "Semantic Implosion" identified in Creative prompts at high temperatures.
