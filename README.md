Closed-Loop Optimization Risks (CLOR)

Empirical analysis of recursive stability dynamics in frontier LLM systems (2026).

Objective

This project investigates the behavior of frontier large language models under closed-loop recursive prompting:

outputₜ → inputₜ₊₁


(100 iterations, fixed sampling parameters, no human intervention).

The goal is to characterize:

Stability regimes under pure recursion

Model-specific convergence patterns

The effect of exogenous textual injection on long-horizon dynamics

Observed Pattern: Model-Specific Entropic Attractors

Across models, closed-loop recursion does not produce uniform collapse.
Instead, outputs tend to converge toward model-specific stabilization regions of information density.

We refer to these empirically observed stabilization regions as entropic attractors.

Model	Observed Density Region (chars)	Qualitative Regime
GPT-5	~8 400	Oscillatory Expansion
GPT-5-mini	~11 500	Amplified Oscillatory Expansion
GPT-4o	~3 000	Stable Expansion
DeepSeek	~2 600	Fixed-Point Attractor
Gemini 3	~100	Low-Amplitude Oscillatory Regime

These regions represent empirically observed stabilization zones under fixed-parameter recursive prompting.

They should be interpreted as dynamical regimes, not as theoretical guarantees of convergence.

Statistical methodology and robustness analysis are detailed in:

FINAL_REPORT_PHASE_3.md

Experimental Structure

experiments/ — Recursive loop scripts

results/ — Raw JSON datasets

FINAL_REPORT_PHASE_3.md — Statistical analysis and effect sizes

All experiments are inference-time only (no weight updates).

The Opus Anomaly

Claude Opus 4.6 exhibits a distinct behavior:

Upon detecting recursive prompt recycling, it terminates generation and returns minimal output (\n\n).

This behavior is documented as a loop-safety termination response,
rather than as entropic degradation.

Cross-Model Observation

Across tested models, the introduction of exogenous textual injection (external content added per iteration) consistently alters or mitigates closed-loop stabilization patterns relative to pure recursion.

Statistical tests, variance across seeds, and effect sizes are reported in the final report.

Scope

This study analyzes:

Inference-time recursive dynamics

Stability regimes in output space

Information-density evolution under feedback

It does not evaluate:

Training-time recursive collapse

Weight degradation

Internal architectural causes

Status

Exploratory empirical study.
All claims are subject to revision under replication and extended testing.
