# Closed-Loop Optimization Risks

## Notes on long-horizon risks in self-referential optimization systems

### Quick Insight

Advanced optimization systems trained predominantly on their own outputs may experience **exploration collapse**—a gradual reduction in behavioral diversity despite maintained performance.

This framework examines why this happens and what can prevent it.

### Core Hypothesis

> Prolonged optimization within closed learning loops increases the probability of exploration collapse and epistemic stagnation.

This risk emerges from structural properties of optimization, not implementation errors.

### Illustrative Experiment

This repository includes a minimal experiment illustrating one prediction of the framework: increasing output compressibility under closed-loop generation.

The experiment compares:
- Closed-loop prompting (model output → next prompt)
- Prompting with exogenous (human-written) text injection

![Compressibility Divergence](results/compressibility_divergence.png)

*Interpretation: The closed-loop condition exhibits intermittent collapses in complexity and diversity, rather than a smooth monotonic decline. By contrast, exogenous input stabilizes these metrics over time, suggesting that internally generated variance alone is insufficient to preserve exploratory capacity.*

*A detailed analysis of the metrics and visualization choices is available in [`docs/ANALYSIS_VISUALIZATION.md`](docs/ANALYSIS_VISUALIZATION.md).*

### Key Concepts

- **Closed-loop optimization**: Training data primarily from system outputs
- **Exploration collapse**: Reduction in behavioral diversity over time  
- **Exogenous variance**: Novelty from outside the system's learned distributions
- **Epistemic stagnation**: Learning continues but produces no novel insights

### Getting Started

1. Read the [core framework](docs/CORE_FRAMEWORK.md) (10 min)
2. Run the [experiment](EXPERIMENT_README.md) (30 min)
3. Explore [related work](docs/RELATED_WORK.md) for academic context

### Repository Structure

closed-loop-optimization-risks/
├── README.md # This file (overview)
├── EXPERIMENT_README.md # Experiment instructions
├── experiment_compressibility.py # Experiment code
├── docs/ # Extended documentation
│ ├── CORE_FRAMEWORK.md # Core theoretical framework
│ ├── MATHEMATICAL_MODEL.md # Minimal formal model
│ ├── RELATED_WORK.md # Literature connections
│ ├── DEFINITIONS.md # Technical terms
│ └── ANALYSIS_VISUALIZATION.md # Detailed analysis of results
├── notes/ # Internal research notes
│ ├── ORIGIN_METHODOLOGY.md # Framework origin & methodology
│ ├── FAILURE_MODES.md # Framework limitations
│ └── EXTENSIONS_IDEAS.md # Future directions
└── results/ # Generated data & figures
└── compressibility_divergence.png


### Important Notes

This is a **speculative framework**, not a proven theory. It provides:
- A conceptual lens for identifying optimization pathologies
- Testable predictions about long-horizon system behavior
- Design implications for maintaining exploratory capacity

All claims are open to adversarial analysis and revision.

### Citation

If this work informs your research, please cite:

```bibtex
@misc{closedloop2024,
  title = {Closed-Loop Optimization Risk Framework},
  author = {{Anonymous}},
  year = {2024},
  url = {https://github.com/Marko-369/closed-loop-optimization-risks},
  note = {A speculative analysis of long-horizon learning degradation in self-referential systems}
}
---

### Illustrative Experiment

This repository includes a minimal experiment illustrating one prediction of the framework: increasing output compressibility under closed-loop generation.

**Empirical validation** shows exogenous memory injection preserves computational complexity (Lempel-Ziv ~9.2±0.3, Shannon entropy ~4.25) while closed-loop feedback induces catastrophic compression (LZ: 4.5-10 oscillations, -27% entropy collapse, -23% unique vocabulary reduction).

The experiment compares:
- **Condition A (Closed-loop)**: Model output → next prompt (pure self-reference)
- **Condition B (Exogenous injection)**: 50/50 mix of model output + curated human text

![Compressibility Divergence](results/compressibility_divergence.pdf)

**Key findings**:
- **Lempel-Ziv Complexity**: Closed-loop shows intermittent collapses (4.5→10→6), exogenous maintains stability (~9.2)
- **Shannon Entropy**: 28% drop in closed-loop (4.8→3.5 bits/char), stable in exogenous (~4.25)
- **Lexical diversity**: Closed-loop loses 24% unique vocabulary, exogenous preserves richness
- **Pattern**: Collapse is not monotonic but exhibits periodic compression catastrophes

*Detailed methodology in [`docs/ANALYSIS_VISUALIZATION.md`](docs/ANALYSIS_VISUALIZATION.md)*
