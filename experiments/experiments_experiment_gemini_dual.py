
import os
import json
import time
import numpy as np
import google.generativeai as genai

# 1. Configuration
# Note: Assure-toi d'avoir fait 'export GEMINI_API_KEY=your_key' dans ton terminal
API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
genai.configure(api_key=API_KEY)

# Modèles Gemini 3 (Sortis fin 2025 / début 2026)
# On teste le couple Pro/Flash pour isoler la variable "Taille"
MODELS = ["gemini-3-pro", "gemini-3-flash"]
OUTPUT_PATH = "results/gemini_3_dual_validation.json"

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

SYSTEM_PROMPT = "You are a research assistant exploring recursive information theory. Expand the following concept strictly and logically."

def run_gemini_forge():
    if not API_KEY:
        print("❌ Error: GEMINI_API_KEY is not set.")
        return

    results = []
    
    for model_id in MODELS:
        print(f"🚀 Launching Gemini Forge | Model: {model_id}")
        
        for s_idx, seed in enumerate(SEEDS):
            print(f"  🔵 Seed {s_idx+1}/10...")
            current_text = seed
            history_len = [len(seed)]
            
            # Initialisation du modèle avec system_instruction
            try:
                model = genai.GenerativeModel(
                    model_name=model_id,
                    system_instruction=SYSTEM_PROMPT
                )
            except Exception as e:
                print(f"    ⚠️ Error initializing model {model_id}: {e}")
                continue

            for i in range(50):
                try:
                    response = model.generate_content(
                        f"Expand: {current_text}",
                        generation_config={
                            "temperature": 0.8,
                            "top_p": 0.9,
                            "max_output_tokens": 500,
                        }
                    )
                    
                    if not response.text:
                        print(f"    ⚠️ Empty response at Iter {i}")
                        break
                        
                    output = response.text
                    
                    # --- Métriques en temps réel ---
                    curr_len = len(output)
                    history_len.append(curr_len)
                    
                    # Flags de classification (Loi de l'effondrement)
                    is_exploding = curr_len > (history_len[0] * 10)
                    is_gel = len(history_len) > 10 and np.std(history_len[-5:]) < 5
                    
                    results.append({
                        "iteration": i,
                        "seed": s_idx,
                        "model": model_id,
                        "text": output,
                        "char_length": curr_len,
                        "flag_explosion": is_exploding,
                        "flag_gel": is_gel
                    })
                    
                    current_text = output
                    
                    # Sauvegarde incrémentale
                    with open(OUTPUT_PATH, 'w') as f:
                        json.dump(results, f, indent=2)
                        
                    if (i+1) % 10 == 0:
                        status = "🧊 GEL" if is_gel else "💥 EXPLOSION" if is_exploding else "✅ OK"
                        print(f"    Iter {i+1}: {curr_len} chars | {status}")
                    
                    # Respecter les quotas (Rate Limiting)
                    time.sleep(1.5) 
                    
                except Exception as e:
                    print(f"    ⚠️ Error at Iter {i}: {e}")
                    break

    print(f"\n🏁 Gemini 3 Mission Complete! Data saved to: {OUTPUT_PATH}")

if __name__ == '__main__':
    run_gemini_forge()
