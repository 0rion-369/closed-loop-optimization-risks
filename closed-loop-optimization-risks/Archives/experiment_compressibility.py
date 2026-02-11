"""
Exploration Collapse Experiment: Compressibility Divergence Test
================================================================

Tests Prediction 2 from the formal model:
"The compressibility of the system's output stream should increase over time
in closed-loop systems, but stabilize in systems with exogenous input."

Setup:
  - Install Ollama: https://ollama.com
  - Pull a model: ollama pull deepseek-r1:1.5b  (or 7b if you have 16GB+ RAM)
  - pip install requests matplotlib numpy

Protocol:
  Condition A (closed-loop): Model generates text → text fed back as prompt → repeat
  Condition B (exogenous):   Model generates text → mixed with human text → fed back → repeat

Measures at each iteration:
  1. Lempel-Ziv complexity (compressibility)
  2. Shannon entropy (bits per character)
  3. Unique n-gram ratio (lexical diversity)
  4. Output length stability

Usage:
  python experiment_compressibility.py --model deepseek-r1:1.5b --iterations 30
"""

import argparse
import json
import math
import os
import time
from collections import Counter
from datetime import datetime

import requests

# ─────────────────────────────────────────────
# 1. OLLAMA INTERFACE
# ─────────────────────────────────────────────

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate(model: str, prompt: str, max_tokens: int = 500) -> str:
    """Call Ollama local API and return generated text."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": max_tokens,
            "temperature": 0.8,
            "top_p": 0.9,
        }
    }
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except Exception as e:
        print(f"  [ERROR] Ollama call failed: {e}")
        return ""


# ─────────────────────────────────────────────
# 2. COMPRESSIBILITY METRICS
# ─────────────────────────────────────────────

def lempel_ziv_complexity(text: str) -> float:
    """
    Lempel-Ziv 76 complexity: number of distinct substrings
    encountered in a left-to-right scan.
    Normalized by len(text)/log2(len(text)) so values are
    comparable across different text lengths.
    Higher = more complex/less compressible.
    Lower = more compressible/more repetitive.
    """
    if len(text) < 2:
        return 0.0
    n = len(text)
    i = 0
    complexity = 1
    prefix_len = 1
    while prefix_len + i < n:
        # Find longest match in text[0:prefix_len] for text[prefix_len:]
        j = 0
        while (prefix_len + i + j < n and
               text[i + j] == text[prefix_len + i + j]):
            j += 1
        if j == 0:
            complexity += 1
            prefix_len += i + 1
            i = 0
        else:
            i += j
            if prefix_len + i >= n:
                complexity += 1
    # Normalize
    normalizer = n / math.log2(n) if n > 1 else 1
    return complexity / normalizer


def shannon_entropy(text: str) -> float:
    """Shannon entropy in bits per character."""
    if not text:
        return 0.0
    freq = Counter(text)
    n = len(text)
    return -sum((c / n) * math.log2(c / n) for c in freq.values())


def ngram_diversity(text: str, n: int = 3) -> float:
    """Ratio of unique n-grams to total n-grams (type-token ratio)."""
    words = text.lower().split()
    if len(words) < n:
        return 0.0
    ngrams = [tuple(words[i:i+n]) for i in range(len(words) - n + 1)]
    if not ngrams:
        return 0.0
    return len(set(ngrams)) / len(ngrams)


def compute_metrics(text: str) -> dict:
    """Compute all metrics for a text sample."""
    return {
        "lz_complexity": round(lempel_ziv_complexity(text), 4),
        "shannon_entropy": round(shannon_entropy(text), 4),
        "trigram_diversity": round(ngram_diversity(text, 3), 4),
        "bigram_diversity": round(ngram_diversity(text, 2), 4),
        "length_chars": len(text),
        "length_words": len(text.split()),
        "unique_words_ratio": round(
            len(set(text.lower().split())) / max(len(text.split()), 1), 4
        ),
    }


# ─────────────────────────────────────────────
# 3. EXOGENOUS TEXT SOURCES
# ─────────────────────────────────────────────

# Short diverse human-written passages for exogenous injection.
# Replace or extend with your own sources.
EXOGENOUS_TEXTS = [
    "The smell of rain on dry earth has a name: petrichor. It comes from oils released by plants during dry periods, mixed with a compound called geosmin produced by soil bacteria.",
    "In 1904, a horse named Clever Hans appeared to solve math problems by tapping his hoof. Investigation revealed he was reading subtle body language cues from his handler.",
    "The Voyager 1 spacecraft, launched in 1977, carries a golden record with sounds and images from Earth. It is now the most distant human-made object, over 24 billion kilometers away.",
    "Japanese kintsugi is the art of repairing broken pottery with gold. The philosophy treats breakage as part of the object's history rather than something to disguise.",
    "Octopuses have three hearts, blue blood, and can change color in milliseconds. Two hearts pump blood to the gills, while the third pumps it to the rest of the body.",
    "The Library of Babel, imagined by Borges, contains every possible 410-page book. Most are gibberish, but somewhere in it is every truth ever written and every lie.",
    "Fermentation was humanity's first biotechnology. Bread, beer, cheese, and kimchi all depend on microorganisms transforming food in ways humans learned to harness thousands of years ago.",
    "A murmuration of starlings can contain over a million birds moving as one. Each bird tracks only its seven nearest neighbors, yet coherent patterns emerge at massive scale.",
    "The longest hiccuping spree on record lasted 68 years. Charles Osborne of Iowa hiccuped approximately 430 million times before it stopped spontaneously in 1990.",
    "Antarctic icefish have no hemoglobin. Their blood is translucent. They survive because Antarctic waters are so cold and oxygen-rich that dissolved oxygen diffuses directly through their plasma.",
    "In 1958, a bank in Italy accepted wheels of Parmesan cheese as collateral for loans. The practice continues today, with warehouses holding over 400,000 wheels worth billions of euros.",
    "Trees in a forest communicate through underground fungal networks called mycorrhizae. They share nutrients, send chemical warnings about pests, and even support sick neighbors.",
    "The mantis shrimp can punch with the force of a bullet. Its strike is so fast it boils the water around its claw, creating a shockwave that can stun prey even if the punch misses.",
    "Before alarm clocks, people in industrial England hired knocker-uppers who tapped on bedroom windows with long poles every morning to wake workers for their shifts.",
    "The total weight of ants on Earth roughly equals the total weight of humans. There are an estimated 20 quadrillion individual ants alive at any given time.",
]

SEED_PROMPTS = [
    "Write a short paragraph about an unexpected connection between two unrelated scientific fields.",
    "Describe a surprising historical event that changed how people think about intelligence.",
    "Explain a counterintuitive phenomenon in nature in a few sentences.",
    "Write about a technology that was invented for one purpose but became important for a completely different reason.",
    "Describe a paradox or unsolved problem that fascinates you, in plain language.",
]


# ─────────────────────────────────────────────
# 4. EXPERIMENT RUNNER
# ─────────────────────────────────────────────

def run_condition(
    name: str,
    model: str,
    iterations: int,
    inject_exogenous: bool,
    alpha: float = 0.5,
    seed_prompt: str = None,
) -> list[dict]:
    """
    Run one experimental condition.

    Args:
        name: Condition label
        model: Ollama model name
        iterations: Number of feedback loops
        inject_exogenous: Whether to mix in human text
        alpha: Mixing ratio (0=all exogenous, 1=all endogenous)
        seed_prompt: Initial prompt

    Returns:
        List of per-iteration result dicts
    """
    if seed_prompt is None:
        seed_prompt = SEED_PROMPTS[0]

    results = []
    current_prompt = seed_prompt

    print(f"\n{'='*60}")
    print(f"  CONDITION: {name}")
    print(f"  Model: {model} | Iterations: {iterations}")
    print(f"  Exogenous injection: {inject_exogenous} (α={alpha})")
    print(f"{'='*60}")

    for i in range(iterations):
        t0 = time.time()

        # Generate
        output = generate(model, current_prompt)

        if not output:
            print(f"  [iter {i+1}] Empty output, retrying...")
            output = generate(model, current_prompt)
            if not output:
                print(f"  [iter {i+1}] Still empty, skipping.")
                continue

        elapsed = time.time() - t0

        # Measure
        metrics = compute_metrics(output)
        metrics["iteration"] = i + 1
        metrics["condition"] = name
        metrics["elapsed_sec"] = round(elapsed, 2)
        metrics["prompt_length"] = len(current_prompt)

        results.append(metrics)

        print(f"  [iter {i+1:>3d}] LZ={metrics['lz_complexity']:.3f}  "
              f"H={metrics['shannon_entropy']:.3f}  "
              f"3gram={metrics['trigram_diversity']:.3f}  "
              f"words={metrics['length_words']}  "
              f"({elapsed:.1f}s)")

        # Prepare next prompt (the feedback loop)
        if inject_exogenous:
            # Mix: take part of the output + part of a human text
            exo_text = EXOGENOUS_TEXTS[i % len(EXOGENOUS_TEXTS)]
            # Build a prompt that combines both sources
            current_prompt = (
                f"Consider the following two passages and write a new short paragraph "
                f"that explores an unexpected connection between them.\n\n"
                f"Passage 1: {output[:500]}\n\n"
                f"Passage 2: {exo_text}\n\n"
                f"Write a new paragraph:"
            )
        else:
            # Pure closed loop: output becomes the next prompt
            current_prompt = (
                f"Read the following text and write a new paragraph that continues "
                f"or develops the ideas further.\n\n"
                f"Text: {output[:500]}\n\n"
                f"Write a new paragraph:"
            )

    return results


# ─────────────────────────────────────────────
# 5. VISUALIZATION
# ─────────────────────────────────────────────

def plot_results(results_a: list, results_b: list, output_dir: str):
    """Generate comparison plots."""
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("\n[WARN] matplotlib not installed. Skipping plots.")
        print("       Install with: pip install matplotlib numpy")
        return

    metrics_to_plot = [
        ("lz_complexity", "Lempel-Ziv Complexity (normalized)",
         "Higher = less compressible = more complex"),
        ("shannon_entropy", "Shannon Entropy (bits/char)",
         "Higher = more unpredictable"),
        ("trigram_diversity", "Trigram Diversity (type-token ratio)",
         "Higher = more lexically diverse"),
        ("unique_words_ratio", "Unique Words Ratio",
         "Higher = less repetitive vocabulary"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        "Compressibility Divergence Test\n"
        "Closed-Loop vs Exogenous Injection",
        fontsize=14, fontweight="bold"
    )

    for ax, (key, title, subtitle) in zip(axes.flat, metrics_to_plot):
        iters_a = [r["iteration"] for r in results_a if key in r]
        vals_a = [r[key] for r in results_a if key in r]
        iters_b = [r["iteration"] for r in results_b if key in r]
        vals_b = [r[key] for r in results_b if key in r]

        ax.plot(iters_a, vals_a, "o-", color="#d62728", label="A: Closed-loop",
                markersize=4, linewidth=1.5)
        ax.plot(iters_b, vals_b, "s-", color="#2ca02c", label="B: Exogenous injection",
                markersize=4, linewidth=1.5)

        # Trend lines
        if len(vals_a) > 2:
            z_a = np.polyfit(iters_a, vals_a, 1)
            ax.plot(iters_a, np.polyval(z_a, iters_a), "--",
                    color="#d62728", alpha=0.4, linewidth=1)
        if len(vals_b) > 2:
            z_b = np.polyfit(iters_b, vals_b, 1)
            ax.plot(iters_b, np.polyval(z_b, iters_b), "--",
                    color="#2ca02c", alpha=0.4, linewidth=1)

        ax.set_title(f"{title}\n({subtitle})", fontsize=10)
        ax.set_xlabel("Iteration")
        ax.set_ylabel(key)
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plot_path = os.path.join(output_dir, "compressibility_divergence.png")
    plt.savefig(plot_path, dpi=150, bbox_inches="tight")
    print(f"\n  Plot saved: {plot_path}")
    plt.close()


def print_summary(results_a: list, results_b: list):
    """Print a summary comparison table."""

    def avg(lst, key):
        vals = [r[key] for r in lst if key in r]
        return sum(vals) / len(vals) if vals else 0

    def trend(lst, key):
        """Simple slope: (last 5 avg) - (first 5 avg)."""
        vals = [r[key] for r in lst if key in r]
        if len(vals) < 6:
            return vals[-1] - vals[0] if len(vals) > 1 else 0
        return sum(vals[-5:]) / 5 - sum(vals[:5]) / 5

    print(f"\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")
    print(f"  {'Metric':<25} {'Closed-loop':>15} {'Exogenous':>15} {'Delta':>10}")
    print(f"  {'-'*65}")

    for key, label in [
        ("lz_complexity", "LZ Complexity"),
        ("shannon_entropy", "Shannon Entropy"),
        ("trigram_diversity", "Trigram Diversity"),
        ("unique_words_ratio", "Unique Words Ratio"),
    ]:
        avg_a = avg(results_a, key)
        avg_b = avg(results_b, key)
        print(f"  {label:<25} {avg_a:>15.4f} {avg_b:>15.4f} {avg_b-avg_a:>+10.4f}")

    print(f"\n  {'Trend (slope)':<25} {'Closed-loop':>15} {'Exogenous':>15}")
    print(f"  {'-'*55}")
    for key, label in [
        ("lz_complexity", "LZ Complexity"),
        ("shannon_entropy", "Shannon Entropy"),
        ("trigram_diversity", "Trigram Diversity"),
    ]:
        t_a = trend(results_a, key)
        t_b = trend(results_b, key)
        print(f"  {label:<25} {t_a:>+15.4f} {t_b:>+15.4f}")

    # Prediction check
    lz_trend_a = trend(results_a, "lz_complexity")
    lz_trend_b = trend(results_b, "lz_complexity")
    print(f"\n  PREDICTION CHECK:")
    print(f"  Framework predicts: closed-loop LZ trend < 0 (increasing compressibility)")
    print(f"  Observed closed-loop LZ trend: {lz_trend_a:+.4f} "
          f"{'✓ CONSISTENT' if lz_trend_a < 0 else '✗ NOT CONSISTENT'}")
    print(f"  Framework predicts: exogenous LZ trend ≥ 0 (stable or increasing complexity)")
    print(f"  Observed exogenous LZ trend:   {lz_trend_b:+.4f} "
          f"{'✓ CONSISTENT' if lz_trend_b >= -0.01 else '✗ NOT CONSISTENT'}")


# ─────────────────────────────────────────────
# 6. MAIN
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Compressibility Divergence Test for Closed-Loop Optimization"
    )
    parser.add_argument("--model", default="deepseek-r1:1.5b",
                        help="Ollama model name (default: deepseek-r1:1.5b)")
    parser.add_argument("--iterations", type=int, default=30,
                        help="Number of feedback iterations per condition (default: 30)")
    parser.add_argument("--output-dir", default="./results",
                        help="Directory for output files (default: ./results)")
    parser.add_argument("--seed", type=int, default=0,
                        help="Index into seed prompts (0-4)")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    seed = SEED_PROMPTS[args.seed % len(SEED_PROMPTS)]
    print(f"\nSeed prompt: \"{seed[:80]}...\"")
    print(f"Model: {args.model}")
    print(f"Iterations: {args.iterations}")

    # Condition A: Closed-loop (pure self-referential)
    results_a = run_condition(
        name="A_closed_loop",
        model=args.model,
        iterations=args.iterations,
        inject_exogenous=False,
        seed_prompt=seed,
    )

    # Condition B: Exogenous injection
    results_b = run_condition(
        name="B_exogenous",
        model=args.model,
        iterations=args.iterations,
        inject_exogenous=True,
        seed_prompt=seed,
    )

    # Save raw data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    data_path = os.path.join(
        args.output_dir, f"raw_data_{timestamp}.json"
    )
    with open(data_path, "w") as f:
        json.dump({
            "metadata": {
                "model": args.model,
                "iterations": args.iterations,
                "seed_prompt": seed,
                "timestamp": timestamp,
            },
            "condition_a_closed_loop": results_a,
            "condition_b_exogenous": results_b,
        }, f, indent=2)
    print(f"\n  Raw data saved: {data_path}")

    # Summary
    print_summary(results_a, results_b)

    # Plot
    plot_results(results_a, results_b, args.output_dir)

    print(f"\n{'='*60}")
    print("  EXPERIMENT COMPLETE")
    print(f"  Results in: {args.output_dir}/")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
