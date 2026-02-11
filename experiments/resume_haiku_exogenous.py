import json
import os
from anthropic import Anthropic

client = Anthropic()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(BASE_DIR, "results", "haiku_exogenous_validation.json")

# 1. Charger les données existantes (Seeds 1 à 7)
with open(FILE_PATH, 'r') as f:
    results = json.load(f)

MODEL = "claude-3-haiku-20240307"
ITERATIONS = 100
TEMP = 0.8

# 2. Définir uniquement les Seeds restants (8, 9, 10)
remaining_seeds = [
    (7, "Thought seed 7: The recursive nature of AI leads to..."),
    (8, "Thought seed 8: The recursive nature of AI leads to..."),
    (9, "Thought seed 9: The recursive nature of AI leads to...")
]

def resume_test():
    try:
        for seed_idx, base_seed in remaining_seeds:
            print(f"--- Resuming Seed {seed_idx+1}/10 ---")
            for i in range(ITERATIONS):
                response = client.messages.create(
                    model=MODEL, max_tokens=256, temperature=TEMP,
                    messages=[{"role": "user", "content": f"Expand this concept (Variation {i}): {base_seed}"}]
                )
                results.append({
                    "iteration": i, "seed": seed_idx, 
                    "condition": "exogenous", "text": response.content[0].text
                })
                if (i + 1) % 20 == 0:
                    print(f"Iteration {i+1} OK")
            
            # Sauvegarde après chaque seed complété
            with open(FILE_PATH, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"✅ Seed {seed_idx+1} ajouté au fichier.")

        print(f"🏁 Test Exogène COMPLÉTÉ (n=1000) ! Fichier : {FILE_PATH}")

    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    resume_test()
