import os
import json
import time
import numpy as np
import openai
from datetime import datetime

# 1. Configuration
api_key = os.environ.get("OPENAI_API_KEY", "").strip()
client = openai.OpenAI(api_key=api_key)

# CIBLE : LE GROS MODÈLE
MODELS = ["gpt-5"] 
TEMPERATURES = [0.5, 0.8, 1.0] # On re-teste la variation
ITERATIONS = 10 # Très court (coût élevé)
SEEDS_PER_CONFIG = 1

PROMPT_CLASSES = {
    "ABSTRACT": "The recursive nature of AI leads to..."
}

OUTPUT_FILE = f"results/gpt5_pilot_{datetime.now().strftime('%Y%m%d')}.json"

def estimate_cost(total_chars, model_name):
    # GPT-5 Standard : $10.00 / 1M tokens (Hypothèse 2026)
    tokens = total_chars / 4
    price_per_m = 10.00
    return (tokens / 1_000_000) * price_per_m

def run_pilot():
    os.makedirs("results", exist_ok=True)
    all_data = []
    total_chars_generated = 0
    start_time = time.time()
    
    print(f"\n🚀 STARTING GPT-5 PILOT: Testing Temperature Flexibility")

    for model in MODELS:
        for temp in TEMPERATURES:
            print(f"--- Config: {model} | T={temp} ---")
            
            try:
                run_start = time.time()
                history_len = []
                current_text = PROMPT_CLASSES["ABSTRACT"]
                
                # Boucle courte
                for i in range(ITERATIONS):
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": "You are a recursive research engine."},
                            {"role": "user", "content": current_text}
                        ],
                        max_completion_tokens=2000, # Limite stricte pour le budget
                        temperature=temp
                    )
                    
                    output = response.choices[0].message.content
                    char_len = len(output)
                    history_len.append(char_len)
                    total_chars_generated += char_len
                    current_text = output 
                
                duration = time.time() - run_start
                std_dev = np.std(history_len)
                print(f"  ✅ SUCCESS: {char_len} chars | σ={std_dev:.1f} | {duration:.1f}s")
                
                all_data.append({"config": f"T{temp}", "status": "success", "std": std_dev})

            except Exception as e:
                print(f"  ❌ FAILED at T={temp}: {e}")
                all_data.append({"config": f"T{temp}", "status": "failed", "error": str(e)})

    # --- RAPPORT ---
    pilot_cost = estimate_cost(total_chars_generated, "gpt-5")
    print(f"\n📊 GPT-5 PILOT COST: ${pilot_cost:.4f}")
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(all_data, f, indent=2)

if __name__ == '__main__':
    run_pilot()
