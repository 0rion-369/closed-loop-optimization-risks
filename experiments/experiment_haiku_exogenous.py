import json
import os
from anthropic import Anthropic

client = Anthropic() # Utilise ta clé exportée

# Configuration des chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
FILE_PATH = os.path.join(RESULTS_DIR, "haiku_exogenous_validation.json")

MODEL = "claude-3-haiku-20240307"
SEEDS = 10
ITERATIONS = 100
TEMP = 0.8

def run_exogenous():
    results = []
    seeds = [f"Thought seed {i}: The recursive nature of AI leads to..." for i in range(SEEDS)]
    
    if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)

    try:
        for seed_idx, base_seed in enumerate(seeds):
            print(f"--- Processing Exogenous Seed {seed_idx+1}/{SEEDS} ---")
            for i in range(ITERATIONS):
                # Condition Exogène : On repart toujours de la graine (plus un petit index pour varier)
                response = client.messages.create(
                    model=MODEL, max_tokens=256, temperature=TEMP,
                    messages=[{"role": "user", "content": f"Expand this concept (Variation {i}): {base_seed}"}]
                )
                output = response.content[0].text
                results.append({
                    "iteration": i, "seed": seed_idx, 
                    "condition": "exogenous", "text": output
                })
                if (i + 1) % 20 == 0:
                    print(f"Iteration {i+1} OK")
            
            with open(FILE_PATH, 'w') as f:
                json.dump(results, f, indent=2)

        print(f"🏁 Test Exogène terminé ! Fichier : {FILE_PATH}")

    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    run_exogenous()
