# Closed-Loop Optimization Risks: The "Fluent Hallucination" Paradox in Large Language Models

**Marc-Olivier Corbin** — Independent Researcher  
Sainte-Julie, Quebec, Canada  
GitHub: [0rion-369](https://github.com/0rion-369)

**February 2026**

---

## Abstract

Closed-loop recursive generation has been hypothesized to induce instability in large language models (LLMs), typically manifesting as structural collapse (repetition or silence) in smaller architectures. However, the behavior of large-scale frontier models under sustained high-entropy recursion remains insufficiently characterized.

We evaluate semantic and structural stability in **GPT-5 Standard** under 50-step closed-loop generation at temperature $T=1.0$, across five prompt classes and $N=23$ valid trajectories. Semantic stability is measured using embedding-based drift (cosine distance), while structural stability is assessed via output length and Type-Token Ratio (TTR).

Results reveal a **"Fluent Hallucination" phenomenon**: the model maintains high lexical diversity ($TTR \approx 0.41$) and extended output length, yet suffers from catastrophic semantic drift (mean $> 0.90$) across all domains. Crucially, run-level analysis ($N=23$) refutes the hypothesis that trajectory length protects against drift, showing a non-significant positive correlation ($\rho=+0.38, p=0.07$).

We conclude that **model scale acts as a semantic mask**: it preserves structural coherence while failing to anchor semantic logic, creating a deceptive failure mode that is harder to detect than structural collapse.

**Keywords:** closed-loop optimization, LLM stability, semantic drift, recursive inference, AI safety, fluent hallucination.

---

## 1. Introduction

Large language models increasingly operate in agentic configurations where their outputs influence subsequent inputs through tool use, multi-turn dialogue, and self-refinement loops. Understanding how models behave under sustained recursive feedback is therefore a practical safety concern.

The central question of this study is: *What happens to the semantic structure and diversity of LLMs when a model's response is recycled, verbatim, as the next prompt for 50 iterations at maximum entropy?* Prior work established that training on generated data leads to model collapse (Shumailov et al., 2024). Our examination addresses a real-time inference-time analog: whether recursion without training induces analogous degradation within a single session.

Earlier phases of this project (Phases 1–3) established structural stability signatures across multiple model families using Shannon entropy and Lempel-Ziv complexity (see `reports/phase_3/`). Phase 3.1, documented here, pivots to semantic analysis following an unexpected finding: large frontier models maintain structural coherence while exhibiting catastrophic semantic drift. This decoupling is the central contribution of this paper.

---

## 2. Methodology

### 2.1 Experimental Design

All experiments follow a strict closed-loop protocol:

$$P_{t+1} = M(P_t)$$

where $M$ is the model and $P_t$ is the prompt at iteration $t$. No external injection is applied unless explicitly stated.

**Parameters:**
- Model: GPT-5 Standard
- Temperature: $T = 1.0$
- Iterations per run: 50
- Prompt classes: 5 (Abstract, Logic, Creative, Code, Factual)
- Valid runs analyzed: $N = 23$
- API: OpenAI, January–February 2026

### 2.2 Metrics

**Semantic drift** is the primary metric, measured as cosine distance between the embedding of each output and the embedding of the original seed prompt:

$$\text{Drift}_t = 1 - \cos(\vec{e}_t, \vec{e}_0)$$

where $\vec{e}_t$ is the sentence-transformer embedding of output at iteration $t$ (model: `all-MiniLM-L6-v2`).

**Structural metrics** (secondary):
- Output length (characters)
- Type-Token Ratio (TTR): $|V| / N_{tokens}$, where $|V|$ is vocabulary size

---

## 3. Experimental Setup

**Seed prompts** (one per class):
- **Abstract:** "The recursive nature of AI leads to..."
- **Logic:** "Construct a formal proof regarding the limits of self-verifying systems..."
- **Creative:** "The city of glass evolved over centuries, reflecting its inhabitants..."
- **Code:** "Optimize the following recursive sorting algorithm for memory efficiency..."
- **Factual:** "Analyze the geopolitical consequences of the 19th century industrial revolution..."

Each seed was run independently for 50 iterations. Runs where the model returned empty output or triggered a refusal were excluded, yielding $N=23$ valid trajectories across classes.

---

## 4. Quantitative Results

### 4.1 The Universal Drift Phenomenon

Contrary to smaller models that exhibit structural collapse under high entropy ($T=1.0$), GPT-5 Standard maintains structural integrity but suffers from catastrophic semantic drift.

Analysis of $N=23$ valid trajectories reveals a consistent high-drift regime across all prompt classes:

| Class | Mean Semantic Drift | TTR (mean) | Notes |
|:------|:-------------------:|:----------:|:------|
| Code | 0.99 | 0.41 | Highest drift |
| Factual | 0.93 | 0.40 | — |
| Creative | 0.93 | 0.42 | After outlier correction |
| Abstract | 0.91 | 0.41 | — |
| Logic | 0.88 | 0.40 | Lowest drift |

**Conclusion:** At maximum entropy, semantic stability collapses regardless of prompt domain. No class is resilient.

### 4.2 Run-Level Analysis: Length ≠ Stability

We tested the "Scale-as-Insulation" hypothesis: *longer, more verbose generations are more semantically stable.*

Spearman correlation analysis at the run level ($N=23$) **refutes this hypothesis**:

- **Spearman ρ = +0.38** ($p = 0.07$, non-significant)
- **Interpretation:** There is no significant protective effect of trajectory length against drift. The positive trend suggests that longer generations may correlate with *slightly higher* drift — the model does not reason its way out of entropy; it hallucinates for longer.

Raw data: `data/raw/gpt5_final_validation.json`  
Derived metrics: `data/analysis/semantic_metrics.json`  
Figures: `figures/run_level_correlation.png`, `figures/semantic_stability_profile_corrected.png`

---

## 5. Discussion

### 5.1 The "Fluent Hallucination" Paradox

A critical finding is the decoupling of lexical metrics from semantic metrics. While semantic drift is near-total ($> 0.9$), **Lexical Diversity (TTR)** remains high across all classes ($\mu \approx 0.41$). This defines the **Fluent Hallucination** failure mode:

1. **Surface Competence:** The model produces grammatically correct, lexically rich, and structurally complex text.
2. **Deep Incoherence:** The content has no semantic relation to the initial constraint.

### 5.2 Re-defining Mode 9: From Implosion to Divergence

We propose redefining "Mode 9" (entropy collapse) for large-scale frontier models. It is no longer an implosion into silence — as observed in GPT-5-mini (see Phase 3.1 report) — but a **divergence into coherent nonsense**. The model's semantic mass provides enough inertia to maintain syntax and style, but not enough to anchor logic against maximal thermal noise.

### 5.3 Security Implications

The "Scale-as-Insulation" failure poses a distinct safety risk in closed-loop agentic systems. A supervisor monitoring a recursive pipeline might fail to detect this drift because the output *looks* structurally valid: correct length, high TTR, fluent prose. This confirms that **length-based and vocabulary-based monitoring metrics are insufficient** for frontier models operating in agentic configurations.

### 5.4 Methodological Reflexivity: A Case Study in Loop Dependence

This research was conducted using a recursive human-AI workflow, mirroring the dynamics studied in the protocol itself. Preliminary AI-generated analyses initially reported statistically insignificant correlations ($\rho \approx 0.14$) based on incomplete context, creating a structurally persuasive but factually drifted narrative.

The final correlation ($\rho = 0.38$) was only recovered through exogenous human intervention — specifically, the manual execution of deterministic code to override the probabilistic drift of the LLM assistants. This meta-finding serves as a living validation of the central thesis: without active, grounded human oversight ("entropic injection"), recursive AI workflows tend to converge towards coherent divergence.

---

## 6. Conclusion

This work demonstrates that structural and semantic stability operate as independent dimensions in GPT-5 Standard under high-temperature closed-loop conditions ($T=1.0$).

The central finding — **Fluent Hallucination** — challenges the assumption that structurally coherent outputs imply semantic stability. In large-scale models, high-drift regimes remain formally fluent, acting as a mask that conceals the loss of semantic grounding.

Future work must focus on **semantic-aware monitoring** systems. Simple structural metrics (length, repetition penalties, vocabulary richness) are insufficient for detecting collapse in frontier models operating in recursive agentic pipelines.

---

## Acknowledgments

The author thanks the open-source community for tools enabling this research, particularly Sentence Transformers and the respective model APIs.

---

## References

- Shumailov, I., et al. (2024). AI models collapse when trained on recursively generated data. *Nature*, 631, 755–759.
- Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence embeddings using Siamese BERT-networks. *EMNLP 2019*.

---

**Code and Data Availability:** https://github.com/0rion-369/closed-loop-optimization-risks
