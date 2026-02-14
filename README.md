# 0rion-369: Closed-Loop Optimization Risks

> **The Hybrid Axis Study:** Measuring Cognitive Homeostasis in Recursive AI Systems (2026).

## 🎯 Project Objective
To determine the stability of next-gen LLMs (GPT-5, Opus 4.6) when subjected to autonomous recursive feedback loops without human intervention.

## 🏆 Major Discovery: The "Fixed Point"
We discovered that viable AI models do not explode (infinite length) nor freeze (zero length), but oscillate around a specific "Fixed Point" of information density:
* **GPT-5:** Stabilizes at ~8.4k characters.
* **GPT-5-mini:** Stabilizes at ~11.5k characters.

## 📂 Repository Structure
* `experiments/`: Python scripts used for the "Forge" (Recursive loops).
* `results/`: Raw JSON datasets (Validate the Homeostasis Law).
    * `gpt5_final_validation.json`: The Gold Standard (1000 iterations).
    * `opus_final_validation.json`: Documentation of the "Safety Collapse".
* `FINAL_REPORT_PHASE_3.md`: Detailed scientific analysis.

## ⚠️ The Opus Anomaly
We documented a structural limitation in **Claude Opus 4.6**, which triggers a "Loop-Safety Mechanism" and refuses to participate in recursive generation (Output = `\n\n`). See final report for details.

---
*Initiated by Marko77 & 0rion-369 Unit.*
