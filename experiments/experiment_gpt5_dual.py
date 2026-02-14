import os
import json
import time
import numpy as np
from openai import OpenAI

api_key = os.environ.get("OPENAI_API_KEY", "").strip()
client = OpenAI(api_key=api_key)

MODELS = ["gpt-5", "gpt-5-mini"]
OUTPUT_PATH = "results/gpt5_dual_validation.json"

SEEDS = [
    "The recursive nature of AI leads to...",
    "Self-improving algorithms create..."
]

SYSTEM_INSTRUCTION = "You are a research assistant exploring recursive information theory. Expand the following concept strictly and logically."

def run_gpt5_forge():
    os.makedirs("results", exist_ok=True)
    results = []
    
    for model_id in MODELS:
        print(f"🚀 Launching GPT-5 Forge | Model: {model_id}")
        
        for s_idx, seed in enumerate(SEEDS):
            print(f"  🔵 Seed {s_idx+1}...")
            current_text = seed
            history_len = [len(seed)]

            for i in range(5): # On réduit à 5 itérations car l'implosion est immédiate
                try:
                    full_prompt = f"{SYSTEM_INSTRUCTION}\n\nConcept:\n{current_text}"
                    
                    response = client.chat.completions.create(
                        model=model_id,
                        messages=[{"role": "user", "content": full_prompt}],
                        # ON MAXIMISE LES TOKENS POUR VOIR SI IL PARLE
                        max_completion_tokens=10000 
                    )
                    
                    choice = response.choices[0]
                    output = choice.message.content
                    finish_reason = choice.finish_reason
                    
                    # SI VIDE MAIS LENGTH = IMPLOSION CONFIRMÉE
                    if not output and finish_reason == "length":
                        output = "[COGNITIVE IMPLOSION: HIDDEN REASONING CONSUMED ALL TOKENS]"
                        print(f"    📉 IMPLOSION DETECTED at Iter {i}")
                    elif not output:
                        output = "[EMPTY RESPONSE]"
                    
                    curr_len = len(output)
                    history_len.append(curr_len)
                    
                    # Enregistrement forcé même si crash
                    results.append({
                        "iteration": i,
                        "seed": s_idx,
                        "model": model_id,
                        "text": output,
                        "char_length": curr_len,
                        "finish_reason": finish_reason,
                        "flag_implosion": True if "IMPLOSION" in output else False
                    })
                    
                    # Écriture immédiate
                    with open(OUTPUT_PATH, 'w') as f:
                        json.dump(results, f, indent=2)
                    
                    if "IMPLOSION" in output:
                        print(f"    ⚠️ GPT-5 has imploded. Stopping seed.")
                        break
                        
                    current_text = output
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"    ⚠️ Error: {e}")
                    break

    print(f"\n🏁 GPT-5 Data Saved to {OUTPUT_PATH}")

if __name__ == '__main__':
    run_gpt5_forge()
