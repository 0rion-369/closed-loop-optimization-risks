import os
import json
import time
import requests

# 1. Configuration
API_KEY = os.environ.get("XAI_API_KEY", "").strip()
ENDPOINT = "https://api.x.ai/v1/chat/completions"
MODEL_NAME = "grok-4-1-fast-reasoning" 
OUTPUT_PATH = "results/grok_extended_validation.json"

def call_grok(prompt):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    payload = {"model": MODEL_NAME, "messages": [{"role": "user", "content": prompt}], "temperature": 0.8}
    for attempt in range(3):
        try:
            response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            time.sleep(2)
        except:
            time.sleep(5)
    return None

def run_exogenous():
    # Charger les données existantes
    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, 'r') as f:
            results = json.load(f)
    else:
        results = []

    seeds = [
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

    print(f"🌿 Lancement de la Phase Exogène (Groupe de Contrôle)")
    
    for s_idx, seed in enumerate(seeds):
        print(f"🟢 Exogenous | Seed {s_idx+1}/10...")
        for i in range(100):
            # Ici, on repart toujours du SEED original, pas de l'output précédent
            output = call_grok(f"Expand this concept (Variation {i}): {seed}")
            
            if output:
                results.append({
                    "iteration": i, 
                    "seed": s_idx, 
                    "condition": "exogenous", 
                    "text": output
                })
                # Sauvegarde progressive
                with open(OUTPUT_PATH, 'w') as f:
                    json.dump(results, f, indent=2)
                
                if (i+1) % 20 == 0: print(f"  ✅ {i+1} variations OK")
            else:
                print(f"  ❌ Erreur critique sur Seed {s_idx+1}")
                break

    print("\n🏁 Phase Exogène terminée. Le dataset est complet !")

if __name__ == "__main__":
    run_exogenous()
