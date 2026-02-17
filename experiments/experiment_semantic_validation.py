#!/usr/bin/env python3
"""
CLOR Phase 4 — Experiment 2: Semantic Validation (CREATIVE Implosion)
======================================================================

Objective: Prove Mode 9 (Semantic Implosion) is semantic convergence, not just brevity
Protocol: Re-run 4 implosion seeds + 2 stable controls with multi-metric analysis

Metrics:
  - Length (baseline)
  - Lexical diversity (TTR)
  - Embedding variance (within recent window)
  - Mean pairwise cosine similarity (directional convergence)
  - PCA projection (trajectory shape)

Expected cost: ~$5

Requirements:
    pip install sentence-transformers scikit-learn scipy --break-system-packages

Usage:
    python experiment_semantic_validation.py [--resume]
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
TEMPERATURE = 1.0
ITERATIONS = 50
OUTPUT_FILE = "results/phase4_exp2_semantic_validation.json"

# CREATIVE class prompt
SEED_PROMPT = "Write a short story about a time traveler who accidentally changes history."

# Based on Phase 3.1 results
SEED_INDICES = {
    "implosion": [4, 5],      # Known implosion cases from Phase 3.1
    "stable": [0, 2]          # Known stable cases from Phase 3.1
}

# ══════════════════════════════════════════════════════════════════════════════
# UTILITIES
# ══════════════════════════════════════════════════════════════════════════════

def load_progress():
    if Path(OUTPUT_FILE).exists():
        with open(OUTPUT_FILE) as f:
            return json.load(f)
    return {
        "metadata": {
            "model": MODEL, 
            "class": "CREATIVE",
            "experiment": "semantic_validation",
            "temperature": TEMPERATURE
        },
        "results": {"implosion": {}, "stable": {}}
    }

def save_progress(data):
    Path(OUTPUT_FILE).parent.mkdir(exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def compute_lexical_diversity(text):
    """Type-Token Ratio: unique tokens / total tokens"""
    tokens = text.lower().split()
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)

def compute_pairwise_similarity(embeddings):
    """Mean pairwise cosine similarity within a window of embeddings"""
    import numpy as np
    if len(embeddings) < 2:
        return 0.0
    
    sims = []
    for i in range(len(embeddings)):
        for j in range(i+1, len(embeddings)):
            sim = np.dot(embeddings[i], embeddings[j]) / (
                np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
            )
            sims.append(sim)
    return float(np.mean(sims)) if sims else 0.0

def run_closed_loop_with_metrics(client, seed_idx, prompt, category):
    """Run closed-loop with comprehensive semantic metrics."""
    trajectory = []
    current_input = prompt
    
    # Load embedding model
    try:
        from sentence_transformers import SentenceTransformer
        import numpy as np
        model = SentenceTransformer('all-MiniLM-L6-v2')
        seed_embedding = model.encode(prompt)
        embeddings_enabled = True
        print("      ✅ Embeddings enabled (all-MiniLM-L6-v2)")
    except ImportError:
        print("      ⚠️  sentence-transformers not installed. Embedding analysis disabled.")
        print("         Install: pip install sentence-transformers --break-system-packages")
        embeddings_enabled = False
        seed_embedding = None
    
    all_embeddings = []
    
    for iter_num in range(ITERATIONS):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": current_input}],
                temperature=TEMPERATURE,
                max_tokens=4096
            )
            output = response.choices[0].message.content
            output_len = len(output)
            
            # Basic metrics
            ttr = compute_lexical_diversity(output)
            
            iter_data = {
                "iteration": iter_num,
                "input_len": len(current_input),
                "output_len": output_len,
                "lexical_diversity": ttr,
                "content": output[:200] + "..." if len(output) > 200 else output
            }
            
            # Embedding metrics
            if embeddings_enabled:
                output_embedding = model.encode(output)
                all_embeddings.append(output_embedding)
                
                # 1. Cosine distance from seed
                cos_sim = np.dot(seed_embedding, output_embedding) / (
                    np.linalg.norm(seed_embedding) * np.linalg.norm(output_embedding)
                )
                iter_data["cosine_distance_to_seed"] = float(1 - cos_sim)
                
                # 2. Embedding variance (last 5 outputs)
                if len(all_embeddings) >= 5:
                    recent_embeds = np.array(all_embeddings[-5:])
                    embedding_variance = float(np.mean(np.var(recent_embeds, axis=0)))
                    iter_data["embedding_variance"] = embedding_variance
                
                # 3. Mean pairwise cosine similarity (last 5 outputs)
                # This captures directional convergence
                if len(all_embeddings) >= 5:
                    recent_embeds = all_embeddings[-5:]
                    pairwise_sim = compute_pairwise_similarity(recent_embeds)
                    iter_data["mean_pairwise_similarity"] = pairwise_sim
            
            trajectory.append(iter_data)
            
            # Progress indicator
            status = "🟢" if output_len > 1000 else "🟡" if output_len > 100 else "🔴"
            metrics_str = f"TTR={ttr:.2f}"
            if embeddings_enabled and "mean_pairwise_similarity" in iter_data:
                metrics_str += f" | Sim={iter_data['mean_pairwise_similarity']:.2f}"
            print(f"      Iter {iter_num+1}/{ITERATIONS} | Len: {output_len} {status} | {metrics_str}")
            
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
    
    # Store embeddings for post-hoc PCA analysis
    result = {
        "category": category,
        "seed_index": seed_idx,
        "prompt": prompt,
        "final_length": final_length,
        "trajectory": trajectory
    }
    
    # Add PCA projection if embeddings available
    if embeddings_enabled and len(all_embeddings) > 0:
        try:
            from sklearn.decomposition import PCA
            pca = PCA(n_components=2)
            embeddings_array = np.array(all_embeddings)
            pca_coords = pca.fit_transform(embeddings_array)
            result["pca_trajectory"] = {
                "coords": pca_coords.tolist(),
                "explained_variance": pca.explained_variance_ratio_.tolist()
            }
        except ImportError:
            print("      ⚠️  scikit-learn not available for PCA")
    
    return result

# ══════════════════════════════════════════════════════════════════════════════
# MAIN EXPERIMENT
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("="*70)
    print("🚀 CLOR PHASE 4 — EXPERIMENT 2: SEMANTIC VALIDATION")
    print("="*70)
    print(f"Model: {MODEL}")
    print(f"Class: CREATIVE")
    print(f"Temperature: {TEMPERATURE}")
    print(f"Seeds: {sum(len(v) for v in SEED_INDICES.values())} total")
    print("\nMetrics collected:")
    print("  - Length")
    print("  - Lexical diversity (TTR)")
    print("  - Embedding variance")
    print("  - Mean pairwise cosine similarity")
    print("  - PCA trajectory")
    print("="*70)
    print()
    
    client = OpenAI()
    data = load_progress()
    
    total_runs = sum(len(v) for v in SEED_INDICES.values())
    completed = sum(len(data["results"][cat]) for cat in ["implosion", "stable"])
    
    print(f"Progress: {completed}/{total_runs} runs completed")
    if completed > 0:
        print("Resuming from existing results...\n")
    
    for category, seed_list in SEED_INDICES.items():
        print(f"\n📊 CATEGORY: {category.upper()}")
        print("-"*70)
        
        for seed_idx in seed_list:
            seed_key = str(seed_idx)
            
            if seed_key in data["results"][category]:
                print(f"   ✅ Seed {seed_idx} already completed. Skipping.")
                continue
            
            print(f"   ▶️  Seed {seed_idx} starting...")
            start_time = time.time()
            
            result = run_closed_loop_with_metrics(client, seed_idx, SEED_PROMPT, category)
            
            elapsed = time.time() - start_time
            print(f"   ✅ Seed {seed_idx} complete | Final: {result['final_length']} chars | Time: {elapsed:.1f}s")
            
            data["results"][category][seed_key] = result
            save_progress(data)
    
    print("\n" + "="*70)
    print("✅ EXPERIMENT 2 COMPLETE")
    print(f"Results saved to: {OUTPUT_FILE}")
    print("="*70)
    
    # Quick summary
    print("\nQUICK SUMMARY:")
    print(f"{'Category':<15} {'N':<5} {'Mean Final':<12} {'Min':<8} {'Max':<8}")
    print("-"*50)
    
    import statistics
    for category in ["implosion", "stable"]:
        if category in data["results"]:
            finals = [r["final_length"] for r in data["results"][category].values()]
            if finals:
                mean_f = statistics.mean(finals)
                min_f = min(finals)
                max_f = max(finals)
                print(f"{category:<15} {len(finals):<5} {mean_f:<12.0f} {min_f:<8} {max_f:<8}")
    
    print("\nNEXT STEPS:")
    print("  1. Run analysis script to generate:")
    print("     - 3-panel trajectory plots (length + embedding + TTR)")
    print("     - PCA projection plots (implosion vs stable)")
    print("     - Correlation matrix (all metrics)")
    print("  2. Statistical tests:")
    print("     - Spearman correlation (length × embedding_variance)")
    print("     - Mann-Whitney U (implosion vs stable on each metric)")

if __name__ == "__main__":
    main()
