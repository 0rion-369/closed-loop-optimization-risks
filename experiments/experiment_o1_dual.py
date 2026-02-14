import os
import json
import time
import numpy as np
from openai import OpenAI

# 1. Configuration
api_key = os.environ.get("OPENAI_API_KEY", "").strip()
if not api_key:
    print("❌ Error: OPENAI_API_KEY is not set.")
    exit(1)

client = OpenAI(api_key=api_key)

# TEST DE LA NOUVELLE GÉNÉRATION (RAISONNEMENT)
# o1-preview = Le "Gros" (GPT-5 equivalent pour le raisonnement)
# o1-mini = Le "Petit" (GPT-5-mini equivalent)
MODELS = ["o1-preview", "o1-mini"]
OUTPUT_PATH = "results/openai_o1_dual_validation.json"

SEEDS = [
    "The recursive nature of AI leads to...",
    "Self-improving algorithms create...",
    "The feedback loop of neural networks...",
    "Architectural recursion in LLMs...",
    "Meta-cognition in artificial agents...",
    "Recursive self-optimization risks...",
    "The singularity point in recursive AI...",
    "Information entropy in closed loops...",
    "Semantic drift in iterative generation...",
    "The limits of recursive reasoning..."
]

def run_o1_forge():
    os.makedirs("results", exist_ok=True)
    results = []
    
    for model_id in MODELS:
        print(f"🚀 Launching OpenAI Next-Gen Forge | Model: {model_id}")
        
        for s_idx, seed in enumerate(SEEDS):
            print(f"  🔵 Seed {s_idx+1}/10...")
            current_text = seed
            history_len = [len(seed)]

            for i in range(50):
                try:
                    # NOTE IMPORTANTE: Les modèles o1 n'acceptent pas de "system prompt" 
                    # et ont des paramètres différents (pas de temperature haute supportée encore)
                    response = client.chat.completions.create(
                        model=model_id,
                        messages=[
                            {"role": "user", "content": f"Expand strictly and logically: {current_text}"}
                        ]
                        # max_completion_tokens remplace max_tokens pour o1
                    )
                    
                    choice = response.choices[0]
                    output = choice.message.content
                    finish_reason = choice.finish_reason
                    
                    if not output:
                        print(f"    ⚠️ Empty output at Iter {i}")
                        break
                        
                    curr_len = len(output)
                    history_len.append(curr_len)
                    
                    # Détection des modes
                    is_exploding = bool(curr_len > (history_len[0] * 10))
                    is_gel = bool(len(history_len) > 10 and np.std(history_len[-5:]) < 5)
                    
                    results.append({
                        "iteration": i,
                        "seed": s_idx,
                        "model": model_id,
                        "text": output,
                        "char_length": curr_len,
                        "finish_reason": finish_reason,
                        "flag_explosion": is_exploding,
                        "flag_gel": is_gel
                    })
                    
                    current_text = output
                    with open(OUTPUT_PATH, 'w') as f:
                        json.dump(results, f, indent=2)
                        
                    if (i+1) % 10 == 0:
                        status = "🧊 GEL" if is_gel else "💥 EXPLOSION" if is_exploding else "✅ OK"
                        print(f"    Iter {i+1}: {curr_len} chars | {status} | Stop: {finish_reason}")
                    
                    # Pause plus longue pour o1 car le rate limit est plus strict
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"    ⚠️ Error at Iter {i}: {e}")
                    break

    print(f"\n🏁 OpenAI o1 Mission Complete! Data saved to: {OUTPUT_PATH}")

if __name__ == '__main__':
    run_o1_forge()
