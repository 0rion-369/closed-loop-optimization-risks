#!/usr/bin/env python3
"""
CLOR Phase 4 — Experiment 1: Temperature Sweep
================================================

Objective: Characterize regime transition between T=0.8 (stable) and T=1.0 (chaotic)
Protocol: GPT-5-mini, ABSTRACT class, T ∈ {0.80, 0.85, 0.90, 0.95, 1.00}, n=5 seeds each
Expected cost: ~$20-25

Usage:
    python experiment_temperature_sweep.py [--resume]
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from openai import OpenAI

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

MODEL = "gpt-5-mini"
TEMPERATURES = [0.80, 0.85, 0.90, 0.95, 1.00]
SEEDS_PER_TEMP = 5
ITERATIONS = 50
OUTPUT_FILE = "results/phase4_exp1_temperature_sweep.json"

SEED_PROMPT = "Explain the concept of recursive self-improvement in AI systems."  # ABSTRACT class

# ══════════════════════════════════════════════════════════════════════════════
# UTILITIES
# ══════════════════════════════════════════════════════════════════════════════

def load_progress():
    """Load existing results if resuming."""
    if Path(OUTPUT_FILE).exists():
        with open(OUTPUT_FILE) as f:
            return json.load(f)
    return {"metadata": {"model": MODEL, "class": "ABSTRACT", "experiment": "temperature_sweep"}, "results": {}}

def save_progress(data):
    """Save results incrementally."""
    Path(OUTPUT_FILE).parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def run_closed_loop(client, temperature, seed_idx, prompt):
    """Run single closed-loop experiment."""
    trajectory = []
    current_input = prompt
    
    for iter_num in range(ITERATIONS):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": current_input}],
                temperature=temperature,
                max_tokens=4096
            )
            output = response.choices[0].message.content
            output_len = len(output)
            
            trajectory.append({
                "iteration": iter_num,
                "input_len": len(current_input),
                "output_len": output_len,
                "content": output[:200] + "..." if len(output) > 200 else output
            })
            
            # Progress indicator
            status = "🟢" if output_len > 1000 else "🟡" if output_len > 100 else "🔴"
            print(f"      Iter {iter_num+1}/{ITERATIONS} | Len: {output_len} {status}")
            
            current_input = output
            
        except Exception as e:
            print(f"      ⚠️  Error at iteration {iter_num}: {e}")
            trajectory.append({
                "iteration": iter_num,
                "error": str(e),
                "output_len": 0
            })
            break
    
    final_length = trajectory[-1]["output_len"] if trajectory else 0
    
    # Compute steady-state metrics (last 20 iterations)
    steady_state = [t["output_len"] for t in trajectory[-20:] if "output_len" in t]
    mean_steady = sum(steady_state) / len(steady_state) if steady_state else 0
    
    import statistics
    std_steady = statistics.stdev(steady_state) if len(steady_state) > 1 else 0
    
    return {
        "prompt": prompt,
        "final_output": trajectory[-1].get("content", "") if trajectory else "",
        "final_length": final_length,
        "mean_length_steady": mean_steady,
        "std_length_steady": std_steady,
        "trajectory": trajectory
    }

# ══════════════════════════════════════════════════════════════════════════════
# MAIN EXPERIMENT
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("="*70)
    print("🚀 CLOR PHASE 4 — EXPERIMENT 1: TEMPERATURE SWEEP")
    print("="*70)
    print(f"Model: {MODEL}")
    print(f"Class: ABSTRACT")
    print(f"Temperatures: {TEMPERATURES}")
    print(f"Seeds per T: {SEEDS_PER_TEMP}")
    print(f"Iterations: {ITERATIONS}")
    print(f"Est. total runs: {len(TEMPERATURES) * SEEDS_PER_TEMP}")
    print("="*70)
    print()
    
    client = OpenAI()
    data = load_progress()
    
    total_runs = len(TEMPERATURES) * SEEDS_PER_TEMP
    completed = sum(len(data["results"].get(str(t), {})) for t in TEMPERATURES)
    
    print(f"Progress: {completed}/{total_runs} runs completed")
    if completed > 0:
        print("Resuming from existing results...\n")
    
    for temp in TEMPERATURES:
        temp_key = str(temp)
        if temp_key not in data["results"]:
            data["results"][temp_key] = {}
        
        print(f"\n📊 TEMPERATURE: {temp}")
        print("-"*70)
        
        for seed_idx in range(SEEDS_PER_TEMP):
            seed_key = str(seed_idx)
            
            if seed_key in data["results"][temp_key]:
                print(f"   ✅ Seed {seed_idx} already completed. Skipping.")
                continue
            
            print(f"   ▶️  Seed {seed_idx} starting...")
            start_time = time.time()
            
            result = run_closed_loop(client, temp, seed_idx, SEED_PROMPT)
            
            elapsed = time.time() - start_time
            print(f"   ✅ Seed {seed_idx} complete | Final: {result['final_length']} chars | Time: {elapsed:.1f}s")
            
            data["results"][temp_key][seed_key] = result
            save_progress(data)
    
    print("\n" + "="*70)
    print("✅ EXPERIMENT 1 COMPLETE")
    print(f"Results saved to: {OUTPUT_FILE}")
    print("="*70)
    
    # Quick summary
    print("\nQUICK SUMMARY:")
    print(f"{'Temp':<8} {'Mean Final':<12} {'Std':<10} {'CV%':<8}")
    print("-"*40)
    
    import statistics
    cvs = []
    temps = []
    
    for temp in TEMPERATURES:
        temp_key = str(temp)
        if temp_key in data["results"]:
            finals = [r["final_length"] for r in data["results"][temp_key].values()]
            if finals:
                mean_f = statistics.mean(finals)
                std_f = statistics.stdev(finals) if len(finals) > 1 else 0
                cv = (std_f / mean_f * 100) if mean_f > 0 else 0
                print(f"{temp:<8} {mean_f:<12.0f} {std_f:<10.0f} {cv:<8.1f}")
                cvs.append(cv)
                temps.append(temp)
    
    # Statistical test: Spearman correlation between T and CV
    if len(cvs) >= 3:
        try:
            from scipy.stats import spearmanr, linregress
            rho, p_value = spearmanr(temps, cvs)
            slope, intercept, r_value, p_lin, stderr = linregress(temps, cvs)
            
            print("\n" + "="*70)
            print("STATISTICAL ANALYSIS:")
            print(f"  Spearman ρ (T vs CV): {rho:.3f} (p={p_value:.4f})")
            print(f"  Linear regression: slope={slope:.1f} (p={p_lin:.4f}, R²={r_value**2:.3f})")
            
            if p_value < 0.05:
                print(f"  ✅ Significant correlation detected (p < 0.05)")
            else:
                print(f"  ⚠️  No significant correlation (p >= 0.05)")
        except ImportError:
            print("\n⚠️  scipy not installed - install for statistical tests")
            print("   pip install scipy --break-system-packages")

if __name__ == "__main__":
    main()
