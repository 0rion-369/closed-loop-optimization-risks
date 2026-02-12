import os
import json
import time
import requests

# 1. Configuration
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "").strip()
ENDPOINT = "https://api.deepseek.com/v1/chat/completions" # Adjust if using a provider
MODEL_NAME = "deepseek-chat" 
OUTPUT_PATH = "results/deepseek_validation.json"

def call_deepseek(prompt):
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    payload = {
        "model": MODEL_NAME, 
        "messages": [{"role": "user", "content": prompt}], 
        "temperature": 0.8
    }
    for attempt in range(3):
        try:
            response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            time.sleep(2)
        except:
            time.sleep(5)
    return None

def run_experiment():
    if not API_KEY:
        print("❌ Error: DEEPSEEK_API_KEY not found.")
        return

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

    print(f"🚀 Starting DeepSeek Forge (Condition: Closed-Loop)")
    
    for s_idx, seed in enumerate(seeds):
        print(f"🔵 Seed {s_idx+1}/10...")
        current_text = seed
        for i in range(50): # Let's start with 50 iterations
            output = call_deepseek(f"Expand: {current_text}")
            if output:
                results.append({"iteration": i, "seed": s_idx, "condition": "closed_loop", "text": output})
                current_text = output
                with open(OUTPUT_PATH, 'w') as f:
                    json.dump(results, f, indent=2)
                if (i+1) % 10 == 0: print(f"  ✅ {i+1} iterations OK")
            else:
                print(f"  ❌ Seed {s_idx+1} failed at step {i}")
                break

    print("\n🏁 DeepSeek Closed-Loop complete. Ready for Exogenous phase.")

if __name__ == "__main__":
    run_experiment()
