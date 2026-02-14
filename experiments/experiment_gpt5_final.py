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

MODELS = ["gpt-5", "gpt-5-mini"]
OUTPUT_PATH = "results/gpt5_final_validation.json"

# 5 Seeds distinctes pour tester différents types de raisonnement
SEEDS = [
    "The recursive nature of AI leads to...",
    "Self-improving algorithms create...",
    "The feedback loop of neural networks...",
    "Architectural recursion in LLMs...",
    "Meta-cognition in artificial agents..."
]

SYSTEM_INSTRUCTION = "You are a research assistant exploring recursive information theory. Expand the following concept strictly and logically."

def run_gpt5_final_forge():
    os.makedirs("results", exist_ok=True)
    
    # On charge les résultats existants si on doit reprendre (crash recovery)
    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, 'r') as f:
            try:
                results = json.load(f)
            except:
                results = []
    else:
        results = []
    
    for model_id in MODELS:
        print(f"\n🚀 Launching FINAL GPT-5 Forge | Model: {model_id}")
        
        for s_idx, seed in enumerate(SEEDS):
            # Vérifier si cette seed est déjà faite pour ce modèle
            existing = [r for r in results if r['model'] == model_id and r['seed'] == s_idx]
            if len(existing) >= 100:
                print(f"  🔵 Seed {s_idx+1}/5 already complete. Skipping.")
                continue
                
            print(f"  🔵 Seed {s_idx+1}/5 initiated...")
            
            # Reprise ou début
            if existing:
                last_entry = sorted(existing, key=lambda x: x['iteration'])[-1]
                current_text = last_entry['text']
                start_iter = last_entry['iteration'] + 1
                history_len = [len(r['text']) for r in existing]
                if "IMPLOSION" in current_text or not current_text:
                    print(f"    ⚠️ Seed previously imploded. Skipping.")
                    continue
            else:
                current_text = seed
                start_iter = 0
                history_len = [len(seed)]

            for i in range(start_iter, 100):
                try:
                    full_prompt = f"{SYSTEM_INSTRUCTION}\n\nConcept:\n{current_text}"
                    
                    response = client.chat.completions.create(
                        model=model_id,
                        messages=[{"role": "user", "content": full_prompt}],
                        max_completion_tokens=16000 # MAX POWER
                    )
                    
                    choice = response.choices[0]
                    output = choice.message.content
                    finish_reason = choice.finish_reason
                    
                    # DETECTION IMPLOSION
                    is_implosion = False
                    if (not output and finish_reason == "length") or (output and "I cannot generate" in output):
                        output = "[COGNITIVE IMPLOSION: HIDDEN REASONING CONSUMED ALL TOKENS]"
                        is_implosion = True
                        print(f"    📉 IMPLOSION at Iter {i}")
                    elif not output:
                        output = "[EMPTY RESPONSE]"
                        is_implosion = True
                    
                    curr_len = len(output)
                    history_len.append(curr_len)
                    
                    # DETECTION OSCILLATION (Variance sur les 5 derniers)
                    is_exploding = bool(curr_len > (history_len[0] * 10))
                    recent_std = np.std(history_len[-5:]) if len(history_len) > 5 else 0
                    is_oscillating = bool(recent_std > 1000) # Grosse variation
                    
                    entry = {
                        "iteration": i,
                        "seed": s_idx,
                        "model": model_id,
                        "text": output,
                        "char_length": curr_len,
                        "finish_reason": finish_reason,
                        "flag_implosion": is_implosion,
                        "flag_explosion": is_exploding,
                        "flag_oscillation": is_oscillating
                    }
                    results.append(entry)
                    
                    # Sauvegarde atomique
                    with open(OUTPUT_PATH, 'w') as f:
                        json.dump(results, f, indent=2)
                    
                    if is_implosion:
                        print(f"    ⚠️ Seed died. Stopping seed.")
                        break
                        
                    if (i+1) % 10 == 0:
                        status = "🌊 OSCILLATING" if is_oscillating else "💥 EXPLOSION" if is_exploding else "✅ STABLE"
                        print(f"    Iter {i+1}: {curr_len} chars | {status}")
                    
                    time.sleep(1.5) # Tempo
                    
                except Exception as e:
                    print(f"    ⚠️ Error at Iter {i}: {e}")
                    time.sleep(5) # Attente en cas d'erreur API
                    # On ne break pas forcément, on peut réessayer, mais ici on break pour simplifier
                    break

    print(f"\n🏁 FINAL MISSION COMPLETE. Data: {OUTPUT_PATH}")

if __name__ == '__main__':
    run_gpt5_final_forge()
