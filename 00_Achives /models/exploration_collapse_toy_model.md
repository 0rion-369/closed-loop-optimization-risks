# A Minimal Mathematical Model of Exploration Collapse

---

## Setup

Let:
- Action space: 𝒜 = {a₁, …, aₙ}
- Policy at time t: πₜ ∈ Δ(𝒜)
- Reward function: R: 𝒜 → ℝ

Data is sampled as:
Dₜ ~ πₜ

Policy update:
πₜ₊₁ = 𝒰(πₜ, Dₜ)

---

## Support Contraction

Define effective support:
Supp(πₜ) = {a | πₜ(a) > ε}

If optimization increases probability mass on high-reward actions and no exploration constraint exists:
Supp(πₜ₊₁) ⊆ Supp(πₜ)

---

## Exploration Collapse

Exploration collapse occurs if:
limₜ→∞ |Supp(πₜ)| ≪ |𝒜|
while expected reward converges.

Performance increases.
Exploration vanishes.

---

## Entropy Measure

Policy entropy:
H(πₜ) = −∑ πₜ(a) log πₜ(a)

In closed-loop optimization:
H(πₜ₊₁) ≤ H(πₜ)

---

## Exogenous Injection

Let:
Dₜ = αDₜᵉⁿᵈᵒ + (1−α)Xₜ , 0 ≤ α < 1

If Xₜ has broader support than πₜ, entropy collapse is prevented.

---

## Interpretation

Exploration collapse is a structural consequence of self-referential optimization, not a failure of algorithms or objectives.
