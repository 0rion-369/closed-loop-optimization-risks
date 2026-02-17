# Closed-Loop Optimization Risks: The "Fluent Hallucination" Paradox in Large Language Models

**Marc-Olivier Corbin** Independent Researcher  
Sainte-Julie, Quebec, Canada  
GitHub: 0rion-369  

**February 16, 2026**

---

## Abstract

Closed-loop recursive generation has been hypothesized to induce instability in large language models (LLMs), typically manifesting as structural collapse (repetition or silence) in smaller architectures. However, the behavior of large-scale frontier models under sustained high-entropy recursion remains insufficiently characterized.

We evaluate semantic and structural stability in **GPT-5 Standard** under 50-step closed-loop generation at temperature $T=1.0$, across five prompt classes and $N=23$ valid trajectories. Semantic stability is measured using embedding-based drift (cosine distance), while structural stability is assessed via output length and Type-Token Ratio (TTR).

Results reveal a **"Fluent Hallucination" phenomenon**: the model maintains high lexical diversity ($TTR \approx 0.41$) and extended output length, yet suffers from catastrophic semantic drift (mean $> 0.90$) across all domains. Crucially, run-level analysis ($N=23$) refutes the hypothesis that trajectory length protects against drift, showing a non-significant positive correlation ($\rho=+0.38, p=0.07$).

We conclude that **model scale acts as a semantic mask**: it preserves structural coherence while failing to anchor semantic logic, creating a deceptive failure mode that is harder to detect than structural collapse.

---

## 1. Introduction
*(Preserved from original draft - Contextualizing CLOR and recursion risks)*

## 2. Methodology
*(Preserved from original draft - Setup describing GPT-5 Standard, T=1.0, and 5 classes)*

## 3. Experimental Setup
*(Preserved from original draft - Prompts and Closed-Loop Architecture)*

## 4. Metrics
*(Preserved from original draft - Definitions of Output Len, TTR, Drift)*

---

## 5. Quantitative Results

### 5.1 The Universal Drift Phenomenon
Contrary to smaller models that exhibit "structural collapse" (silence or repetition) under high entropy ($T=1.0$), the GPT-5 Standard model maintains structural integrity but suffers from catastrophic semantic drift.

Analysis of $N=23$ valid trajectories reveals a consistent high-drift regime:
* **High Drift across all classes:** Semantic drift scores consistently exceeded **0.85**, with *Code* (**0.99**) and *Factual* (**0.93**) being the most affected.
* **The "Creative" Myth:** Even the *Creative* class, previously hypothesized to be resilient, exhibited a mean drift of **0.93** (after outlier correction).
* **Conclusion:** At maximum entropy, semantic stability collapses regardless of the prompt domain.

### 5.2 Run-Level Analysis: Length $\neq$ Stability
We tested the "Scale-as-Insulation" hypothesis, which posits that longer, more verbose generations are more semantically stable.

Spearman correlation analysis at the run level ($N=23$) **refutes this hypothesis**:
* **Correlation ($\rho$):** **+0.38** ($p=0.07$).
* **Interpretation:** There is no significant protective effect of trajectory length against drift. The positive trend suggests that longer generations may even correlate with slightly *higher* drift. The model does not "reason" its way out of entropy; it simply hallucinates for longer.

---

## 6. Discussion

### 6.1 The "Fluent Hallucination" Paradox
A critical finding is the decoupling of lexical metrics from semantic metrics. While semantic drift is near-total ($>0.9$), the **Lexical Diversity (TTR)** remains high across all classes ($\mu \approx 0.41$).

This defines the **Fluent Hallucination** failure mode:
1.  **Surface Competence:** The model produces grammatically perfect, lexically rich, and structurally complex text.
2.  **Deep Incoherence:** The content has zero semantic relation to the initial constraint.

### 6.2 Re-defining Mode 9: From Implosion to Divergence
We propose redefining "Mode 9" (entropy collapse) for large-scale models. It is no longer an implosion into silence (as seen in GPT-5-Mini), but a **divergence into coherent nonsense**. The model's "Semantic Mass" provides enough inertia to maintain syntax and style, but not enough to anchor logic against maximal thermal noise.

### 6.3 Security Implications
This "Scale-as-Insulation" effect poses a distinct safety risk in Closed-Loop Optimization (CLO). A supervisor AI monitoring a loop might fail to detect this drift because the output *looks* structurally valid (correct length, high TTR). This confirms that **length-based and vocabulary-based monitoring metrics are insufficient** for next-generation models.

---

## 7. Conclusion

This work demonstrates that structural and semantic stability operate as independent dimensions in GPT-5 Standard under high-temperature closed-loop conditions ($T=1.0$).

The central finding—**Fluent Hallucination**—challenges the assumption that structurally coherent outputs imply semantic stability. In large-scale models, high-drift regimes remain formally fluent, acting as a mask that hides the loss of control.

Future work must focus on **Semantic-Aware Monitoring** systems, as simple structural metrics (length, repetition penalties) are obsolete for detecting collapse in frontier models.

---

## Acknowledgments
The author thanks the open-source community for tools enabling this research, particularly Sentence Transformers and the OpenAI API.

## References
* Shumailov, I., et al. (2024). The Curse of Recursion. *arXiv preprint*.
* Reimers, N., & Gurevych, I. (2019). Sentence-BERT. *EMNLP*.

---
**Code and Data Availability:** https://github.com/0rion-369/closed-loop-optimization-risks