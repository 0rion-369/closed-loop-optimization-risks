# Mathematical Model
## Formal Foundations of the Closed-Loop Optimization Risk Framework

---

## 1. Core Setup

Let a generative system at time *t* be characterized by a policy:

```
πₜ : X → Δ(Y)
```

Where:
- `X` = input space (prompts, contexts)
- `Y` = output space (tokens, actions)  
- `Δ(Y)` = probability simplex over outputs
- `t` = iteration index (t = 0, 1, ..., T)

---

## 2. Entropy as the Primary Observable

We measure **Shannon entropy** of outputs as the key indicator of informational capacity:

```
H(πₜ) = −∑ᵧ πₜ(y) · log₂ πₜ(y)    [bits per character]
```

**Empirical baseline** (from extended validation, n=2000):

```
H₀ ≈ 4.55 bits/char    (initial entropy, iterations 0-2)
```

---

## 3. Closed-Loop Dynamics

### 3.1 Definition

In a **closed-loop** system, the input at iteration *t+1* is derived exclusively from the output at iteration *t*:

```
xₜ₊₁ = f(yₜ)    where yₜ ~ πₜ(· | xₜ)
```

The training or generation distribution contracts over the system's own outputs:

```
Dₜ₊₁ ⊆ support(πₜ)
```

### 3.2 Entropy Collapse Theorem (Informal)

Under closed-loop dynamics with no exogenous input:

```
E[H(πₜ₊₁)] ≤ H(πₜ)
```

Entropy is non-increasing in expectation. The system cannot generate information it has not already learned to generate.

### 3.3 Empirical Confirmation

**Extended validation (100 iterations × 10 seeds, n=2000):**

```
Shannon entropy slope (closed-loop):   β = −0.000417  (p < 0.001)
Shannon entropy slope (exogenous):     β = −0.000008  (p = 0.900, ns)
```

Observed trajectory:
```
H₀ ≈ 4.55  →  H₁₀₀ ≈ 4.35    (−4.4% over 100 iterations)
```

**Temporal model (linear approximation):**
```
H(t) ≈ H₀ + β·t    where β = −0.000417
```

Projected long-horizon collapse:
```
H(500)  ≈ 4.55 − (0.000417 × 500) ≈ 4.34
H(1000) ≈ 4.55 − (0.000417 × 1000) ≈ 4.13
H(5000) ≈ 4.55 − (0.000417 × 5000) ≈ 2.47    [severe collapse]
```

*Note: Linear extrapolation assumes no saturation. Actual trajectory may exhibit non-linear dynamics.*

---

## 4. The Structured Noise Finding

### 4.1 The Paradox

Classical collapse theory predicts:

```
Exploration collapse  →  lower LZ complexity  (more compressible, simpler)
```

**Empirical observation (extended validation):**

```
LZ complexity (closed-loop):   0.031 ± 0.009   (HIGH variance)
LZ complexity (exogenous):     0.024 ± 0.003   (LOW variance)
```

Closed-loop exhibits **higher** LZ complexity, not lower.

### 4.2 Formal Distinction

Define two independent measures:

```
H(πₜ)     = Shannon entropy      (informational content)
C(πₜ)     = LZ complexity        (algorithmic complexity)
```

These are **orthogonal dimensions**:

```
High C, High H  →  Rich, complex information
High C, Low H   →  Structured noise          ← OBSERVED in closed-loop
Low C,  High H  →  Simple but informative
Low C,  Low H   →  Degenerate repetition
```

### 4.3 Structured Noise Definition

A system exhibits **structured noise** when:

```
C(πₜ) ↑   AND   H(πₜ) ↓
```

Equivalently: high algorithmic complexity with declining informational content.

**Empirical signature (extended validation):**

```
Closed-loop:
  LZ slope:      +0.000064  (p < 0.001)  →  complexity increasing
  Shannon slope: −0.000417  (p < 0.001)  →  information decreasing

Exogenous:
  LZ slope:      +0.000007  (p = 0.175, ns)  →  stable
  Shannon slope: −0.000008  (p = 0.900, ns)  →  stable
```

### 4.4 Theoretical Implication

The structured noise regime is epistemically dangerous because:

```
Observable behavior:   Complex, varied, non-repetitive    (appears healthy)
Actual state:          Low informational content           (informationally impoverished)
Detection difficulty:  High                               (complexity masks collapse)
```

---

## 5. Exogenous Injection Model

### 5.1 Mixed Distribution

With exogenous injection at ratio `(1 − α)`:

```
Dₜ = α · Dₜᵉⁿᵈᵒ + (1−α) · Xₜ

where:
  Dₜᵉⁿᵈᵒ  = endogenous distribution (system's own outputs)
  Xₜ      = exogenous distribution  (external variance source)
  α ∈ [0,1] = endogenous weight
```

**Experimental configuration (α = 0.5):**
```
Dₜ = 0.5 · yₜ[:250] + 0.5 · xₜᵉˣᵒ[:250]
```

### 5.2 Entropy Preservation Under Injection

If `H(Xₜ) > H(Dₜᵉⁿᵈᵒ)`, then:

```
H(Dₜ) ≥ H(Dₜᵉⁿᵈᵒ)
```

Exogenous injection acts as an **entropy floor**, preventing collapse below `H(Xₜ)`.

### 5.3 Empirical Confirmation

```
Exogenous condition (α = 0.5):
  Shannon entropy:   4.425 ± 0.05   (stable across 100 iterations)
  LZ complexity:     0.024 ± 0.003  (low variance, stable)
  Temporal slope:    −0.000008      (not significantly different from zero)
```

The 50/50 injection is **sufficient** to prevent collapse at T=0.8.

---

## 6. Variance Asymmetry

### 6.1 Definition

Define the **variance ratio** for metric M:

```
VR(M) = Var(M | closed-loop) / Var(M | exogenous)
```

### 6.2 Empirical Values

```
LZ Complexity:   VR = (0.009)² / (0.003)² = 9.0x
Shannon Entropy: VR = (0.08)²  / (0.05)²  = 2.56x
```

**Closed-loop exhibits 9× higher LZ variance than exogenous.**

This is the quantitative signature of the structured noise regime: not just lower information, but **unstable information** oscillating chaotically.

### 6.3 Attractor Structure

The individual trajectory data (n=10 seeds) reveals:

```
Exogenous:    Converges to stable region    H ≈ [4.40, 4.45], LZ ≈ [0.022, 0.026]
Closed-loop:  Converges to lower region     H ≈ [4.33, 4.40], LZ ≈ [0.015, 0.055]
```

Two distinct attractors in (H, LZ) space, reached within approximately **t = 10-20 iterations**.

---

## 7. Phase Transition Hypothesis

### 7.1 Observation

The individual trajectory plots show rapid divergence in early iterations (t < 20), followed by stabilization around distinct attractors.

This suggests a **critical transition** rather than gradual drift:

```
t < t*:   Transient phase     (both conditions similar)
t ≥ t*:   Attractor phase     (conditions diverge and stabilize)
t* ≈ 10-20 iterations         (estimated from trajectory data)
```

### 7.2 Formal Hypothesis

Let `ΔH(t) = H(exogenous, t) − H(closed-loop, t)` be the divergence:

```
ΔH(t) ≈ 0           for t < t*
ΔH(t) → Δ∞ > 0     for t ≥ t*
```

Where `Δ∞` is the asymptotic entropy gap.

**Estimated from data:**
```
Δ∞ ≈ 4.425 − 4.383 = 0.042 bits/char
t* ≈ 15 ± 5 iterations
```

### 7.3 Test for Future Work

To confirm the phase transition:

```python
# Autocorrelation analysis
lags = range(1, 20)
autocorr_closed = [pearsonr(H_closed[:-lag], H_closed[lag:])[0] for lag in lags]
autocorr_exo    = [pearsonr(H_exo[:-lag],    H_exo[lag:])[0]    for lag in lags]

# Prediction: autocorr_closed drops sharply at t*, autocorr_exo stays high
```

---

## 8. Summary of Empirically Validated Claims

| Claim | Formal Statement | Empirical Support | p-value |
|-------|-----------------|-------------------|---------|
| Entropy collapse | `β_closed < 0` | slope = −0.000417 | < 0.001 |
| Exogenous stability | `β_exo ≈ 0` | slope = −0.000008 | 0.900 |
| Entropy divergence | `H_exo > H_closed` | +1.0% mean difference | < 0.001 |
| Structured noise | `C_closed > C_exo` AND `H_closed < H_exo` | LZ +21.4%, H −1.0% | < 0.001 |
| Variance asymmetry | `Var_closed >> Var_exo` | LZ: 9x, H: 2.56x | — |
| Temporal divergence | `ΔH(t)` increases | slopes significantly different | < 0.001 |

---

## 9. Open Questions

### 9.1 Saturation
Does entropy collapse saturate at some floor `H_min > 0`, or does it continue indefinitely?

```
H_min = ?    (requires T > 100 iterations)
```

### 9.2 Minimum Exogenous Dose
What is the minimum injection ratio `(1−α)` sufficient to prevent collapse?

```
α_critical = ?    (requires dose-response experiment: α ∈ {0.9, 0.75, 0.5, 0.25, 0.1})
```

### 9.3 Temperature Dependence
Does higher temperature `T` substitute for exogenous injection?

```
Hypothesis: High T delays but does not prevent collapse
Test: T ∈ {0.3, 0.5, 0.8, 1.1, 1.3} × {closed-loop, exogenous}
```

### 9.4 Semantic Drift
Does entropy collapse correspond to semantic convergence in embedding space?

```
Hypothesis: cosine_distance(embed(yₜ), embed(yₜ₊₁)) decreases in closed-loop
Test: Add sentence-transformer embeddings to metric suite
```

---

## 10. Relationship to Existing Theory

| Theory | Connection |
|--------|-----------|
| **Model Collapse** (Shumailov et al., 2024) | Entropy collapse is an instance of model collapse in generation space |
| **Shannon Information Theory** | H(π) directly measures exploratory capacity |
| **Dynamical Systems** | Attractor convergence, phase transitions |
| **Goodhart's Law** | Proxy optimization degrades true objective |
| **Free Energy Principle** (Friston) | Closed systems minimize surprise → minimize entropy |

---

## Notation Reference

| Symbol | Definition |
|--------|-----------|
| `πₜ` | Policy/generative distribution at iteration t |
| `H(πₜ)` | Shannon entropy of outputs |
| `C(πₜ)` | Lempel-Ziv complexity of outputs |
| `β` | Linear regression slope over time |
| `α` | Endogenous weight in mixed distribution |
| `Xₜ` | Exogenous input at iteration t |
| `Dₜ` | Training/generation distribution at t |
| `t*` | Critical transition iteration |
| `Δ∞` | Asymptotic entropy gap |
| `VR` | Variance ratio (closed/exogenous) |

---

*All empirical values from: Extended Validation (100 iterations × 10 seeds, n=2000, T=0.8, top-p=0.9)*
*See [results/EXTENDED_VALIDATION_REPORT.md](../results/EXTENDED_VALIDATION_REPORT.md)*
