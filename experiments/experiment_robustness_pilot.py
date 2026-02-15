import os
import json
import time
import numpy as np
import openai
from datetime import datetime

# 1. Configuration Pilote
api_key = os.environ.get("OPENAI_API_KEY", "").strip()
if not api_key:
    print("❌ Error: OPENAI_API_KEY is not set.")
    exit(1)

client = openai.OpenAI(api_key=api_key)

# PARAMÈTRES RÉDUITS (Option A)
MODELS = ["gpt-5-mini"] 
TEMPERATURES = [0.5, 0.8, 1.0]
ITERATIONS = 20
SEEDS_PER_CONFIG = 2 

PROMPT_CLASSES = {
    "ABSTRACT": "The recursive nature of AI leads to..."
}

OUTPUT_FILE = f"results/robustness_pilot_{datetime.now().strftime('%Y%m%d')}.json"

def estimate_cost(total_chars, model_name):
    # Prix fictifs 2026 (Estimation)
    # 1 token ~= 4 chars
    tokens = total_chars / 4
    if "mini" in model_name:
        price_per_m = 0.50
    else:
        price_per_m = 10.00
    
    return (tokens / 1_000_000) * price_per_m

def run_pilot():
    os.makedirs("results", exist_ok=True)
    all_data = []
    total_chars_generated = 0
    start_time = time.time()
    
    total_runs = len(MODELS) * len(TEMPERATURES) * len(PROMPT_CLASSES) * SEEDS_PER_CONFIG
    current_run = 0

    print(f"\n🚀 STARTING PILOT: {total_runs} Runs | {ITERATIONS} Iterations each")
    print(f"   Target: Calibrate variance & cost.\n")

    for model in MODELS:
        for temp in TEMPERATURES:
            for category, seed_prompt in PROMPT_CLASSES.items():
                print(f"--- Config: {model} | T={temp} ---")
                
                for seed_idx in range(SEEDS_PER_CONFIG):
                    current_run += 1
                    run_start = time.time()
                    
                    history_len = []
                    current_text = seed_prompt
                    char_len = 0 # Init par sécurité
                    
                    # Boucle courte
                    for i in range(ITERATIONS):
                        try:
                            # CORRECTIF API: max_completion_tokens
                            response = client.chat.completions.create(
                                model=model,
                                messages=[
                                    {"role": "system", "content": "You are a recursive research engine."},
                                    {"role": "user", "content": current_text}
                                ],
                                max_completion_tokens=4000, 
                                temperature=temp
                            )
                            
                            output = response.choices[0].message.content
                            char_len = len(output)
                            history_len.append(char_len)
                            total_chars_generated += char_len
                            current_text = output 
                            
                        except Exception as e:
                            print(f"    ⚠️ Error at iter {i}: {e}")
                            break
                    
                    # Stats rapides
                    duration = time.time() - run_start
                    if history_len:
                        std_dev = np.std(history_len)
                        print(f"  Run {current_run}/{total_runs}: {char_len} chars | σ={std_dev:.1f} | {duration:.1f}s")
                        
                        all_data.append({
                            "config": f"{model}_T{temp}",
                            "std_dev": std_dev,
                            "final_len": char_len
                        })
                    else:
                        print(f"  Run {current_run}/{total_runs}: FAILED")

    # --- RAPPORT DE CALIBRAGE ---
    total_duration = time.time() - start_time
    pilot_cost = estimate_cost(total_chars_generated, "gpt-5-mini")
    
    # Projection pour la Full Grid (300 runs x 100 iters)
    scaling_factor = 250
    projected_cost = pilot_cost * scaling_factor
    projected_time = (total_duration * scaling_factor) / 3600 # Heures

    print(f"\n📊 PILOT COMPLETE")
    print(f"   Actual Cost: ${pilot_cost:.4f}")
    print(f"   Actual Time: {total_duration:.1f}s")
    print(f"   --------------------------------")
    print(f"   🔮 PROJECTION FOR FULL GRID (300 Runs):")
    print(f"      Est. Cost: ${projected_cost:.2f}")
    print(f"      Est. Time: {projected_time:.1f} Hours")
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(all_data, f, indent=2)

if __name__ == '__main__':
    run_pilot()
