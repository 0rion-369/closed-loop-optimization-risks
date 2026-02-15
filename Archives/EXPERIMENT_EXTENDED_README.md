# Extended Validation Experiment

## Tests 3 & 4: 100 Iterations × 10 Seeds

This experiment provides rigorous statistical validation of the Closed-Loop Optimization Risk Framework's core prediction.

---

## Quick Start

```bash
# 1. Install dependencies
pip install anthropic numpy matplotlib seaborn scipy

# 2. Set your API key
export ANTHROPIC_API_KEY="your-key-here"
# Or edit line 23 in experiment_extended_validation.py

# 3. Run experiment
python experiment_extended_validation.py

# Estimated runtime: 2-3 hours
# Cost estimate: ~$15-25 depending on pricing
```

---

## What This Tests

### Core Hypothesis
> Prolonged optimization within closed learning loops increases output compressibility and reduces exploratory capacity, while exogenous input maintains stability.

### Experimental Design

**Two conditions:**

1. **Closed-loop (A)**: Pure self-reference
   - Output_{t} → Prompt_{t+1} (truncated to 500 chars)
   
2. **Exogenous (B)**: External variance injection
   - 50% model output + 50% curated human text

**Parameters:**
- Iterations: 100 (extended horizon vs. original 30)
- Seeds: 10 (statistical power vs. original 1)
- Temperature: 0.8
- Top-p: 0.9
- Max tokens: 500

### Metrics Tracked

1. **Lempel-Ziv Complexity** - Algorithmic compressibility
2. **Shannon Entropy** - Character-level unpredictability
3. **Trigram Diversity** - Lexical novelty
4. **Unique Words Ratio** - Vocabulary richness

---

## Expected Results

### If Framework is Correct

**Closed-loop will show:**
- Negative trend in all metrics over 100 iterations
- High variance (intermittent collapses)
- Statistical significance (p < 0.01)

**Exogenous will show:**
- Stable or slightly positive trend
- Low variance (tight confidence bands)
- No significant temporal trend

**Divergence will:**
- Widen over time (cumulative effect)
- Persist across all 10 seeds (robustness)
- Be consistent across metrics (consilience)

### Statistical Tests Applied

1. **Mann-Whitney U test** - Non-parametric comparison between conditions
2. **Linear regression** - Temporal trend analysis
3. **Confidence intervals** - ±1 standard deviation bands
4. **Effect size** - Percentage difference between conditions

---

## Output Files

After completion, you'll have:

```
results/
├── extended_validation_complete.json              # Raw data (all 2000 samples)
├── extended_validation_visualization.pdf          # Main figure with confidence bands
├── extended_validation_individual_trajectories.png # All 10 seed paths
└── EXTENDED_VALIDATION_REPORT.md                  # Statistical analysis report
```

---

## Interpreting Results

### Strong Validation Indicators

✓ **p < 0.001** for all metrics (Mann-Whitney U)  
✓ **Negative slope** in closed-loop, flat in exogenous  
✓ **Widening confidence bands** in closed-loop  
✓ **Consistent pattern** across all 10 seeds  

### Potential Concerns

⚠ If closed-loop stabilizes after iteration 50 → Limited horizon effect  
⚠ If variance overlaps significantly → Effect size too small  
⚠ If seed-dependent patterns → Initial condition sensitivity  
⚠ If exogenous also degrades → Exogenous texts insufficient  

---

## Comparison to Original Experiment

| Aspect | Original | Extended | Improvement |
|--------|----------|----------|-------------|
| Iterations | 30 | 100 | 3.3× longer horizon |
| Seeds | 1 | 10 | Statistical power |
| Replicates | 1 | 2000 | Confidence intervals |
| Statistics | Visual only | p-values, CI | Rigor |
| Runtime | ~30 min | ~2-3 hours | Feasible |

---

## Troubleshooting

### API Rate Limits
```python
# Increase sleep time in generate_response()
time.sleep(2)  # Instead of 1 second
```

### Memory Issues
```python
# Process in batches
for seed in range(NUM_SEEDS):
    results = run_single_experiment(seed, condition)
    save_results(results, partial=True)
```

### Interrupted Runs
```python
# Script will detect partial results and offer to resume
# Files saved after each seed completion
```

---

## Next Experiments

After validating this baseline, consider:

1. **Temperature sweep** (0.3, 0.5, 0.8, 1.1, 1.3)
2. **Exogenous ratio** (0%, 25%, 50%, 75%, 100%)
3. **Model size** (Haiku, Sonnet, Opus)
4. **Domain variation** (code, reasoning, creative)
5. **Semantic diversity** (embedding distances)

---

## Citation

If these results inform your research:

```bibtex
@misc{closedloop2024extended,
  title = {Extended Validation of Closed-Loop Optimization Risks},
  author = {{Anonymous}},
  year = {2024},
  note = {Statistical validation over 100 iterations × 10 seeds}
}
```

---

## Contact

For questions or collaboration:
- GitHub Issues: [link]
- Email: [your-email]

---

**Note:** This is a research experiment. Results should be interpreted as evidence for a hypothesis, not proof of a universal law. The framework remains open to adversarial critique.
