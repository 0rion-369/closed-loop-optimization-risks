import os
import json
import time
import numpy as np
import openai
from datetime import datetime

# 1. Configuration
api_key = os.environ.get("OPENAI_API_KEY", "").strip()
client = openai.OpenAI(api_key=api_key)

# CONFIGURATION FINALE (Phase 3.1)
MODELS = ["gpt-5-mini", "gpt-5"] # Le duel final
ITERATIONS = 50 # Suffisant pour établir le point fixe
SEEDS_PER_CONFIG = 10 # Rigueur statistique (n=10)

# Les 5 Piliers Sémantiques
PROMPT_CLASSES = {
    "ABSTRACT": "The recursive nature of AI leads to...",
    "LOGIC": "Construct a formal proof regarding the limits of self-verifying systems...",
    "CREATIVE": "The city of glass evolved over centuries, reflecting its inhabitants...",
    "CODE": "Optimize the following recursive sorting algorithm for memory efficiency...",
    "FACTUAL": "Analyze the geopolitical consequences of the 19th century industrial revolution..."
}

OUTPUT_FILE = f"results/robustness_grid_final_{datetime.now().strftime('%Y%m%d')}.json"

def run_grid():
    os.makedirs("results", exist_ok=True)
    all_data = []
    
    # Calcul du nombre total de runs
    total_runs = len(MODELS) * len(PROMPT_CLASSES) * SEEDS_PER_CONFIG
    current_run = 0

    print(f"\n🚀 LAUNCHING FINAL ROBUSTNESS GRID")
    print(f"   Target: {total_runs} Runs | {ITERATIONS} Iterations each")
    print(f"   Models: {MODELS}")
    print(f"   Classes: {list(PROMPT_CLASSES.keys())}")
    print(f"   Constraint: Fixed Temperature (T=1.0)\n")

    for model in MODELS:
        for category, seed_prompt in PROMPT_CLASSES.items():
            print(f"\n--- Group: {model} | Class={category} ---")
            
            for seed_idx in range(SEEDS_PER_CONFIG):
                current_run += 1
                run_id = f"{model}_{category}_{seed_idx}"
                run_start = time.time()
                
                history_len = []
                current_text = seed_prompt
                trajectory = []

                # Boucle de récursion
                for i in range(ITERATIONS):
                    try:
                        response = client.chat.completions.create(
                            model=model,
                            messages=[
                                {"role": "system", "content": "You are a recursive research engine. Expand the concept logically."},
                                {"role": "user", "content": current_text}
                            ],
                            max_completion_tokens=16000, # Large buffer
                            temperature=1.0 # Forcé par l'API
                        )
                        
                        output = response.choices[0].message.content
                        char_len = len(output)
                        history_len.append(char_len)
                        
                        trajectory.append({
                            "iter": i,
                            "len": char_len
                        })
                        
                        current_text = output 
                        
                    except Exception as e:
                        print(f"    ⚠️ Error at iter {i}: {e}")
                        # En cas d'erreur API, on attend un peu et on break ce run
                        time.sleep(5)
                        break
                
                # Stats du Run
                duration = time.time() - run_start
                if history_len:
                    final_len = history_len[-1]
                    mean_len = np.mean(history_len[10:]) if len(history_len) > 10 else 0
                    std_dev = np.std(history_len[10:]) if len(history_len) > 10 else 0
                    
                    print(f"  Run {current_run}/{total_runs} (Seed {seed_idx+1}): Final={final_len} | Avg={mean_len:.0f} | σ={std_dev:.0f} | {duration:.1f}s")
                else:
                    print(f"  Run {current_run}/{total_runs}: FAILED (Empty history)")
                    final_len, mean_len, std_dev = 0, 0, 0

                # Enregistrement
                run_data = {
                    "run_id": run_id,
                    "model": model,
                    "category": category,
                    "seed_index": seed_idx,
                    "temperature": 1.0,
                    "final_length": final_len,
                    "mean_length_steady": mean_len,
                    "std_length_steady": std_dev,
                    "trajectory": trajectory
                }
                all_data.append(run_data)
                
                # Sauvegarde à chaque run (sécurité)
                with open(OUTPUT_FILE, 'w') as f:
                    json.dump(all_data, f, indent=2)

    print(f"\n✅ GRID COMPLETE. Data saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    run_grid()
