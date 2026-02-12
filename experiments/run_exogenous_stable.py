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
    
    # On garde le timeout à 120s pour plus de sécurité
    for attempt in range(3):
        try:
            response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=120)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            elif response.status_code == 429:
                time.sleep(10) # Pause si l'API est trop sollicitée
            else:
                print(f"  ⚠️ Erreur API {response.status_code}")
        except:
            time.sleep(5)
    return None

def run():
    if not API_KEY:
        print("❌ Erreur : XAI_API_KEY non détectée.")
        return

    # Chargement du fichier existant (pour ne pas perdre les données d'hier)
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

    print(f"🌿 Phase Exogène | Mode Stable | Modèle : {MODEL_NAME}")
    
    for s_idx, seed in enumerate(seeds):
        print(f"🟢 Germe {s_idx+1}/10...")
        for i in range(100):
            # IMPORTANT : On ne réinjecte pas la réponse. On repart toujours du Seed original.
            output = call_grok(f"Expand this concept (Variation {i}): {seed}")
            
            if output:
                results.append({
                    "iteration": i, 
                    "seed": s_idx, 
                    "condition": "exogenous", 
                    "text": output
                })
                # Sauvegarde immédiate sur le disque
                with open(OUTPUT_PATH, 'w') as f:
                    json.dump(results, f, indent=2)
                
                if (i+1) % 10 == 0:
                    print(f"  ✅ {i+1}/100 variations terminées")
                
                time.sleep(0.5) # Petite pause de confort
            else:
                print(f"  ❌ Échec définitif sur le Germe {s_idx+1}, Itération {i}")
                break

    print("\n🏁 Mission terminée. Ton dataset pour l'Axe Hybride est complet !")

if __name__ == "__main__":
    run()
