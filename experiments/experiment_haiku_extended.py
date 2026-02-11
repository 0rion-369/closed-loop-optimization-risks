import json
import time
from anthropic import Anthropic
import numpy as np

client = Anthropic()
MODEL = "claude-haiku-4-202602"
SEEDS = 10
ITERATIONS = 100
TEMP = 0.8

def run_validation():
    results = []
    seeds = [f"Thought seed {i}: The recursive nature of AI leads to..." for i in range(SEEDS)]
    
    for seed_idx, base_seed in enumerate(seeds):
        print(f"--- Processing Seed {seed_idx+1}/{SEEDS} ---")
        
        # Condition 1: Closed-loop (Boucle fermée)
        current_text = base_seed
        for i in range(ITERATIONS):
            response = client.messages.create(
                model=MODEL, max_tokens=256, temperature=TEMP,
                messages=[{"role": "user", "content": f"Expand: {current_text}"}]
            )
            output = response.content[0].text
            results.append({"iteration": i, "seed": seed_idx, "condition": "closed_loop", "text": output})
            current_text = output # Feed back
            
    with open('../results/haiku_extended_validation.json', 'w') as f:
        json.dump(results, f)
    print("✅ Validation Haiku (n=1000/condition) terminée.")

if __name__ == "__main__":
    run_validation()
