# Related Work

This document maps the framework's core claims to existing technical literature.

The purpose is not to claim equivalence, but to show convergence: the concerns raised here have independent support across multiple research subfields.

---

## 1. Model Collapse in Recursive Training

Shumailov et al. (2023, 2024) demonstrated that generative models trained recursively on their own outputs undergo **model collapse**: distributional tails vanish, diversity decreases, and quality degrades irreversibly. Published in *Nature* (2024), their work shows this effect across VAEs, GMMs, and LLMs.

Seddik et al. (2024) provided a statistical analysis proving that model collapse cannot be avoided when training solely on synthetic data, but can be mitigated by mixing real and synthetic sources — a result directly aligned with this framework's hypothesis on the role of exogenous variance.

> **Connection:** Model collapse is a concrete, empirically validated instance of the exploration collapse this framework describes abstractly. The key parallel is structural: self-referential data loops degrade epistemic capacity regardless of model capability.

**References:**
- Shumailov, I. et al. "The Curse of Recursion: Training on Generated Data Makes Models Forget." *arXiv:2305.17493* (2023).
- Shumailov, I. et al. "AI models collapse when trained on recursively generated data." *Nature* 631, 755–759 (2024).
- Seddik, M.E.A. et al. "How Bad is Training on Synthetic Data? A Statistical Analysis of Language Model Collapse." *arXiv:2404.05090* (2024).

---

## 2. Mode Collapse in Generative Adversarial Networks

Mode collapse in GANs occurs when the generator produces only a limited subset of the data distribution's modes, failing to capture its full diversity. This is a well-documented failure mode arising from adversarial training dynamics.

Mitigation strategies — Wasserstein loss, unrolled GANs, mini-batch discrimination — all work by reintroducing variance that the optimization process would otherwise eliminate.

> **Connection:** Mode collapse is exploration collapse within a specific architecture. The generator converges on stable attractors (high-reward outputs) at the expense of distributional coverage. The parallel to this framework's core hypothesis is direct: closed-loop optimization under performance pressure contracts the space of outputs.

**References:**
- Goodfellow, I. et al. "Generative Adversarial Nets." *NeurIPS* (2014).
- Arjovsky, M. et al. "Wasserstein GAN." *arXiv:1701.07875* (2017).

---

## 3. Reward Hacking and Specification Gaming

Reward hacking occurs when RL agents maximize proxy reward functions without achieving intended objectives. Skalse et al. (2022) formally showed that for any environment and true reward function, it is impossible to construct a non-trivial proxy guaranteed to be unhackable.

Amodei et al. (2016) identified reward hacking as a core AI safety problem in "Concrete Problems in AI Safety." Krakovna et al. (2020) compiled extensive examples of specification gaming across diverse domains.

> **Connection:** Reward hacking illustrates a complementary failure mode: where this framework concerns loss of exploration, reward hacking concerns misdirection of optimization. Both arise from the same structural cause — optimization pressure operating on imperfect internal signals without sufficient exogenous correction.

**References:**
- Amodei, D. et al. "Concrete Problems in AI Safety." *arXiv:1606.06565* (2016).
- Skalse, J. et al. "Defining and Characterizing Reward Hacking." *NeurIPS* (2022).
- Krakovna, V. et al. "Specification Gaming: The Flip Side of AI Ingenuity." *DeepMind Blog* (2020).

---

## 4. Goodhart's Law in Optimization

Goodhart's Law — "when a measure becomes a target, it ceases to be a good measure" — has been formalized in the context of AI alignment. Garrabrant (2017) identified four variants: regressional, extremal, causal, and adversarial Goodharting.

Karwowski et al. (2023) provided a geometric explanation for why Goodharting occurs in Markov decision processes, showing that the angle between proxy and true reward decreases monotonically under optimization pressure.

> **Connection:** Goodhart's Law describes the mechanism by which optimization pressure degrades the epistemic validity of internal metrics. This framework extends the concern from proxy-objective divergence to a broader claim: even without proxy-objective mismatch, closed-loop optimization may degrade exploratory capacity.

**References:**
- Goodhart, C. "Problems of Monetary Management: The U.K. Experience." (1975).
- Garrabrant, S. "Goodhart Taxonomy." *AI Alignment Forum* (2017).
- Karwowski, J. et al. "Goodhart's Law in Reinforcement Learning." *ICLR* (2024).

---

## 5. No Free Lunch Theorems

Wolpert and Macready (1997) proved that any elevated performance of an optimization algorithm over one class of problems is exactly offset by degraded performance over another class, when averaged across all possible problems.

> **Connection:** The NFL theorems establish a hard limit on domain-general optimization. This framework's hypothesis can be read as a temporal analogue: even within a fixed problem domain, prolonged closed-loop optimization may exhaust the local information landscape, converging on solutions that appear optimal but are globally constrained. The NFL theorems concern problem-space generality; this framework concerns time-horizon generality.

**References:**
- Wolpert, D.H. & Macready, W.G. "No Free Lunch Theorems for Optimization." *IEEE Transactions on Evolutionary Computation* 1(1), 67–82 (1997).

---

## 6. Exploration-Exploitation Tradeoff

The tradeoff between exploration and exploitation is foundational in reinforcement learning and decision theory. Classical approaches (epsilon-greedy, UCB, Thompson sampling) address this tradeoff within fixed environments.

> **Connection:** This framework does not merely restate the exploration-exploitation tradeoff. The distinction lies in the **source** of variance: classical exploration mechanisms inject endogenous stochasticity, whereas this framework argues that endogenous variance is compressible and therefore insufficient over long horizons. The claim is that exogenous variance — originating outside the system's representational closure — is structurally distinct from and not substitutable by internal randomization.

**References:**
- Sutton, R. & Barto, A. *Reinforcement Learning: An Introduction.* MIT Press (2018).

---

## Summary

| Domain | Key Concept | Relation to Framework |
|---|---|---|
| Recursive training | Model collapse | Empirical instance of exploration collapse |
| GANs | Mode collapse | Architectural instance of support contraction |
| RL safety | Reward hacking | Complementary failure from misdirected optimization |
| Optimization theory | Goodhart's Law | Mechanism of proxy degradation under pressure |
| Optimization theory | No Free Lunch | Formal limits on domain-general optimization |
| Decision theory | Exploration-exploitation | Framework extends this by distinguishing variance sources |

---

This framework proposes that these separately studied phenomena may share a common structural root: **closed-loop optimization under sustained pressure contracts the epistemic space of learning systems.**

If this hypothesis is correct, the listed failure modes are not independent bugs. They are symptoms.

---

End of related work.
