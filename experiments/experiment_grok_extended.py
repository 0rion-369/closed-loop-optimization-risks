import os
import json
import time
import requests

# 1. Configuration et Nettoyage
raw_key = os.environ.get("XAI_API_KEY")
API_KEY = raw_key.strip() if raw_key else None
ENDPOINT = "https://api.x.ai/v1/chat/completions"
# Utilisation du modèle haute performance identifié
MODEL_NAME = "grok-4-1-fast-reasoning" 

if not API_KEY:
    print("❌ ERREUR : La clé XAI_API_KEY est vide.")
    exit()

def call_grok(prompt):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8
    }
    
    # Tentatives multiples en cas de timeout ou d'erreur réseau
    for attempt in range(3):
        try:
            # Timeout à 120s pour gérer l'inflation sémantique
            response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=120)
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            elif response.status_code == 429:
                print(f"  ⏳ Limite de taux atteinte. Pause de 10s...")
                time.sleep(10)
            else:
                print(f"  ⚠️ Erreur API {response.status_code}: {response.text}")
                
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            wait_time = (attempt + 1) * 5
            print(f"  📡 Problème réseau. Nouvelle tentative dans {wait_time}s...")
            time.sleep(wait_time)
            
    return None

def run_experiment():
    results = []
    output_path = "results/grok_extended_validation.json"
    os.makedirs("results", exist_ok=True)
    
    seeds = [f"Thought seed {i}: The recursive nature of AI leads to..." for i in range(10)]
    
    print(f"🔥 Lancement de la forge avec {MODEL_NAME}")

    for s_idx, seed in enumerate(seeds):
        print(f"🎸 Seed {s_idx+1}/10...")
        current_text = seed
        
        for i in range(100):
            output = call_grok(f"Expand: {current_text}")
            
            if output:
                results.append({
                    "iteration": i, 
                    "seed": s_idx, 
                    "condition": "closed_loop", 
                    "text": output
                })
                current_text = output
                
                # Sauvegarde à chaque pas pour sécuriser les données
                with open(output_path, 'w') as f:
                    json.dump(results, f, indent=2)
                
                if (i+1) % 10 == 0: print(f"  ✅ {i+1} itérations validées")
                
                # Petite pause pour la stabilité
                time.sleep(1)
            else:
                print(f"  ❌ Seed {s_idx+1} arrêté par sécurité à l'étape {i}.")
                break

    print("\n🏁 Mission accomplie. Données prêtes pour l'analyse d'entropie.")

if __name__ == "__main__":
    run_experiment()
