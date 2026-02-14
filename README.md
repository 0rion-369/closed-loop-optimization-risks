
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
