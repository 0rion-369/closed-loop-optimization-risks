# Closed-Loop Optimization Risks: Structural Persistence Does Not Prevent Semantic Drift in Large Language Models

**Marc-Olivier Corbin**  
Independent Researcher  
Sainte-Julie, Quebec, Canada  
GitHub: 0rion-369

**February 2026**

---

## Abstract

Closed-loop recursive generation has been hypothesized to induce instability in large language models (LLMs), particularly under high-entropy sampling regimes. Prior observations in smaller models suggest structural degradation, such as repetition or output contraction. However, the behavior of large-scale frontier models under sustained recursion remains insufficiently characterized.

We evaluate semantic and structural stability in GPT-5 Standard under 50-step closed-loop generation at temperature T=1.0, across five prompt classes and N=23 valid trajectories. Semantic stability is measured using embedding-based drift (cosine distance from the seed prompt), while structural and lexical stability are assessed via output length, coefficient of variation (CV), and Type-Token Ratio (TTR).

Results indicate a consistent high-drift regime (mean drift > 0.90 across classes) despite preserved structural and lexical metrics. Run-level analysis shows a weak positive trend between mean trajectory length and semantic drift (ρ=+0.38, p=0.073, marginally non-significant), suggesting that sustained generation may coincide with drift accumulation rather than prevent it. These findings demonstrate a dissociation between structural persistence and semantic stability under high-entropy closed-loop conditions.

We conclude that structural coherence alone is insufficient to characterize recursive stability in large models, motivating multi-metric monitoring frameworks for iterative inference systems. Findings are conditional on GPT-5 Standard at T=1.0; broader generalization requires cross-model and cross-temperature validation.

---

## 1. Introduction

Recursive inference—where model outputs are re-injected as subsequent inputs—emerges naturally in multi-step reasoning agents, iterative summarization pipelines, and autonomous research systems. Such closed-loop configurations remove exogenous corrective signals and may amplify sampling noise over time.

Previous exploratory work suggests that smaller models subjected to high-temperature recursive prompting exhibit structural degradation, including repetition loops or output contraction. These behaviors are surface-detectable via length thresholds or lexical repetition metrics.

However, it remains unclear whether large-scale frontier models exhibit similar collapse dynamics, or whether increased scale alters the phenomenology of recursive instability.

This work investigates three questions:

1. Does sustained closed-loop recursion at high temperature induce semantic drift in large-scale models?
2. Do structural metrics (e.g., output length, lexical diversity) reliably indicate semantic stability?
3. Does sustained generation (measured via mean trajectory length) protect against or exacerbate recursive semantic divergence?

We conduct controlled recursive experiments using GPT-5 Standard at T=1.0, measuring both structural and semantic metrics across multiple prompt classes.

Our central empirical finding is a consistent high-drift regime under high entropy, coupled with preserved structural coherence. This decoupling suggests that recursive instability in large models may not manifest as overt collapse, but as divergence that remains structurally fluent.

We emphasize that all conclusions are conditional on the tested model and temperature configuration.

---

## 2. Methods

### 2.1 Experimental Design

We evaluated recursive generation stability using the following configuration:

- **Model:** GPT-5 Standard
- **Temperature:** T=1.0
- **Sampling:** Default nucleus sampling
- **Iterations per trajectory:** 50
- **Prompt classes:** Code, Factual, Creative, Logic, Abstract
- **Total valid trajectories:** N=23

**Closed-loop protocol:**

1. A seed prompt is provided
2. Model output at iteration t is injected (fully or truncated to 500 characters) as the next prompt
3. No external text injection or corrective signal is introduced
4. Process repeats for 50 iterations

Runs failing due to API errors were excluded from analysis.

### 2.2 Structural Metrics

For each trajectory:

- **Mean trajectory length:** Average output length across all 50 iterations (characters)
- **Coefficient of variation (CV)** across iterations
- **Type-Token Ratio (TTR)** for final output:

```
TTR = unique_tokens / total_tokens
```

Mean trajectory length provides a more stable measure of structural persistence than final output length alone, as it captures behavior across the entire recursive sequence.

### 2.3 Semantic Drift Computation

Semantic stability was evaluated using embedding-based drift.

**Embedding model:**
- SentenceTransformer `all-MiniLM-L6-v2`
- 384-dimensional embeddings
- L2 normalization applied

**Drift computed as:**

```
Drift = 1 - cos(e_seed, e_final)
```

Where:
- e_seed = embedding of original prompt
- e_final = embedding of final iteration output

**Interpretation:**
- Drift ≈ 0 → strong semantic alignment
- Drift ≈ 1 → maximal divergence in embedding space

Drift measures divergence from initial prompt embedding. It does not measure factual incorrectness or logical invalidity.

### 2.4 Statistical Analysis

- Spearman rank correlation used for non-parametric association tests
- Run-level analysis conducted across N=23 trajectories
- Two-tailed tests applied
- Significance threshold: α=0.05
- No correction for multiple comparisons applied; results exploratory

### 2.5 Scope and Limitations

This study evaluates:
- A single large-scale model (GPT-5 Standard)
- A single temperature configuration (T=1.0)
- Closed-loop recursion without exogenous injection

Findings should be interpreted as characterizing a high-entropy closed-loop regime, not as universal properties of large language models.

Cross-temperature and cross-model replication are required to assess generality.

---

## 3. Related Work

**Model Collapse:** Shumailov et al. (2024) demonstrated that fine-tuning on model-generated data leads to progressive quality degradation across generations. Our work extends this by examining *inference-time* recursion rather than training-time contamination.

**Recursive Prompting:** Prior work on chain-of-thought and iterative refinement assumes each step introduces new information or constraints. We isolate pure closed-loop dynamics by removing exogenous input.

**Embedding-Based Evaluation:** Recent work on LLM evaluation increasingly relies on semantic similarity metrics. We apply this methodology to stability assessment in recursive contexts.

---

## 4. Baseline Results: Phase 3 Validation

Prior to semantic validation, we conducted extensive length-based stability analysis across 10 model configurations (Phase 3, n=2000 runs). Key findings:

**Exogenous Injection Effect:**
- Condition A (closed-loop only): 73% collapse rate at 100 iterations
- Condition B (exogenous injection): 0% collapse rate at 100 iterations
- Statistical significance: p < 0.001 (Shannon entropy, two-sample t-test)

**Lazare Protocol (Recovery vs. Prevention):**
Tested whether exogenous injection can *recover* a collapsed system (Claude Haiku 3.5, CREATIVE seed, 30 iterations):

- Phase 1 (iter 0-3, no injection): 576 → 13 → 1 → 1 chars (collapse in 2 iterations)
- Phase 2 (iter 4-8, injection active): 1 → 1,174 chars (apparent recovery, mean 972 chars)
- Phase 3 (iter 9-29, injection continues): 1 char for all 21 iterations (re-collapse despite injection)

**Finding:** Exogenous injection is **prophylactic, not therapeutic**. It prevents collapse when applied from iteration 0 but cannot recover a terminally collapsed system. Point of no return estimated at t*≈3-4 iterations for this configuration.

---

## 5. Quantitative Results

### 5.1 Multi-Metric Stability Assessment

We evaluated semantic stability under closed-loop recursive generation at T=1.0 using GPT-5 Standard across five prompt classes. Validation performed at run-level (n=23 individual trajectories) to avoid aggregation artifacts.

**Table 1: Semantic Metrics by Prompt Class (GPT-5 Standard, T=1.0)**

| Class    | N | Mean Drift | 95% CI        | Mean TTR | 95% CI        | Mean Length | Interpretation              |
|----------|---|------------|---------------|----------|---------------|-------------|------------------------------|
| CODE     | 5 | 0.9963     | [0.963, 1.029]| 0.3708   | [0.319, 0.423]| 1,284       | Maximal drift, stable form  |
| FACTUAL  | 5 | 0.9328     | [0.890, 0.976]| 0.4194   | [0.381, 0.458]| 1,328       | High drift, high diversity  |
| CREATIVE | 4†| 0.9310     | [0.881, 0.981]| 0.3984   | [0.394, 0.423]| 1,824       | No resilience advantage     |
| LOGIC    | 4 | 0.9073     | [0.867, 0.948]| 0.4441   | [0.428, 0.460]| 1,676       | Moderate drift              |
| ABSTRACT | 5 | 0.9042     | [0.844, 0.965]| 0.3806   | [0.294, 0.467]| 1,653       | Lowest drift                |

*Note: 95% confidence intervals computed via bootstrap (10,000 resamples). † CREATIVE n=4: one seed excluded (drift < 0.1, incomplete trajectory). All p-values uncorrected for multiple comparisons.*

### 5.2 Key Findings

**Finding 1: High-Drift Regime Across Content Classes**

All prompt classes exhibit semantic drift > 0.90 (mean across classes: 0.9283, range: 0.9042–0.9963). CREATIVE (drift=0.9310) shows no statistically significant advantage over LOGIC (drift=0.9073; Mann-Whitney U=6.5, p=0.53; Cohen's d=0.41, small effect). High drift at T=1.0 is content-agnostic.

**Finding 2: Dissociation Between Structural and Semantic Stability**

CODE exhibits the highest semantic drift (0.9963) despite the lowest coefficient of variation in output length (CV=12%, Phase 3.1). This dissociation demonstrates:

- **Structural stability:** Format consistency (measured via CV)
- **Semantic stability:** Content preservation (measured via drift)

CODE converges to a deterministic template (CV=12%, mean length=1,284) while semantic content diverges maximally (drift≈1.0). We term this **canonical drift**—formally consistent outputs with maximal semantic divergence.

**Effect size:** CODE vs. ABSTRACT: Cohen's d=1.52 (large effect).

**Finding 3: Weak Positive Trend Between Trajectory Length and Drift**

At run-level (n=23 individual trajectories), mean trajectory length (averaged across 50 iterations) exhibits a weak positive correlation with semantic drift:

- **Mean Trajectory Length ↔ Drift:** ρ=+0.380, p=0.073 (marginally non-significant)
- **Drift ↔ TTR:** ρ=-0.167, p=0.45 (ns)
- **Mean Trajectory Length ↔ TTR:** ρ=+0.335, p=0.12 (ns)

The weak positive trend (ρ=0.38) suggests that longer trajectories may coincide with increased semantic drift, though this association does not reach conventional statistical significance (p=0.073). Output length does not protect against semantic divergence; if anything, sustained generation appears associated with drift accumulation.

**Simpson's Paradox:** Class-aggregated analysis (n=5 means) produces apparent negative correlation between length and drift (ρ=-0.600), but this reverses at run-level (ρ=+0.141, ns). The class-level pattern reflects ordering of class means rather than a coupling mechanism. Figure 2 visualizes this aggregation artifact.

**Implication:** Multi-metric assessments must be performed at run-level to avoid spurious correlations.

**Finding 4: Lexical Preservation Under High Drift**

Despite drift > 0.90, lexical diversity remains moderate to high (TTR range: 0.3708–0.4441, mean=0.4047). This contrasts with smaller models which exhibit coupled degradation. GPT-5 Standard maintains surface-level linguistic richness under high semantic drift—we term this **drift with lexical preservation**.

**Finding 5: Length Metrics as Insufficient Indicators**

FACTUAL prompts (Phase 3.1: CV=54%, most stable by length) exhibit second-highest semantic drift (0.9328). Length stability does not imply semantic stability.

---

## 6. Discussion

### 6.1 Scale and the Decoupling of Stability Dimensions

Model scale alters the phenomenology of closed-loop instability without eliminating high-drift regimes. Stability metrics exhibit independence across dimensions.

**Smaller models:** Coupled degradation—length contracts, lexical diversity falls, outputs repetitive. Surface-detectable.

**Larger models (GPT-5 Standard):** Semantic drift (mean=0.9283) with stable structural metrics. CODE maintains CV=12% and TTR=0.3708 despite drift≈1.0. Not surface-detectable.

**Dimensional relationship:** Run-level analysis reveals a weak positive association between mean trajectory length and semantic drift (ρ=+0.38, p=0.073, marginally non-significant). This suggests that sustained generation does not protect against drift; longer trajectories may coincide with drift accumulation. The association is modest and does not reach conventional statistical significance, indicating that length is at best a weak predictor of semantic stability.

**Implication:** Stability frameworks must incorporate semantic validation alongside structural metrics. Surface-level heuristics are model-scale-dependent and insufficient.

### 6.2 Methodological Requirements: Run-Level Validation

This study documents a Simpson's Paradox: class-aggregated metrics (n=5) show apparent negative correlation between length and drift (ρ=-0.600), but this reverses at run-level (ρ=+0.141, ns). The class-level pattern reflects ordering rather than mechanism (Figure 2).

**Requirement:** Stability assessments must be performed at run-level to avoid spurious correlations from aggregation.

### 6.3 Limitations

- **Sample size:** LOGIC n=4, CREATIVE n=4. Replication with n≥10 per class recommended.
- **Single model:** GPT-5 Standard only. Cross-model validation required.
- **Drift interpretation:** Measures divergence, not semantic invalidity. Human evaluation needed.
- **Temperature:** T=1.0 only. Temperature sweep in progress.
- **Embedding model:** `all-MiniLM-L6-v2` (384-dim). Validation with larger models recommended.

### 6.4 Monitoring Implications

The dimensional independence observed has implications for recursive inference systems:

Current mechanisms (repetition filters, length thresholds) are calibrated to surface-level failures. High-drift regimes in large models do not trigger these indicators.

**Suggested approaches:**
1. **Run-level drift tracking:** Alert if drift exceeds threshold (e.g., >0.80)
2. **Semantic anchoring:** Periodic injection of ground-truth reference text
3. **Multi-metric dashboards:** Monitor structural, semantic, and lexical metrics concurrently at run-level

These are empirical implications, not prescriptive interventions.

---

## 7. Conclusion

This work demonstrates that structural persistence does not prevent semantic drift in GPT-5 Standard under high-temperature closed-loop conditions (T=1.0). Run-level analysis (n=23 trajectories) reveals a weak positive trend between mean trajectory length and semantic drift (ρ=+0.38, p=0.073), suggesting that sustained generation may coincide with drift accumulation rather than mitigate it.

The central finding—that structural coherence does not predict or prevent semantic divergence—challenges the assumption that formally consistent outputs imply semantic stability. In large-scale models, high-drift regimes may remain structurally fluent, evading surface-level detection mechanisms.

Findings are conditional on GPT-5 Standard at T=1.0. Cross-model and cross-temperature validation required to assess generalizability. Multi-metric monitoring frameworks at run-level granularity are necessary for recursive inference systems.

---

## Acknowledgments

The author thanks the open-source community for tools enabling this research, particularly Sentence Transformers, OpenAI API, and the Python scientific computing ecosystem.

---

## References

Shumailov, I., et al. (2024). The Curse of Recursion: Training on Generated Data Makes Models Forget. *arXiv preprint arXiv:2305.17493*.

Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. *Proceedings of EMNLP-IJCNLP*.

---

**Code and Data Availability:**  
Experimental code and datasets available at: https://github.com/0rion-369/closed-loop-optimization-risks

---

**END OF PREPRINT**
