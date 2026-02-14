import os
import json
import time
from openai import OpenAI

# 1. Configuration - THE REASONER CHALLENGE
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "").strip()
BASE_URL = "https://api.deepseek.com"
MODEL_NAME = "deepseek-reasoner"  # Activated R1
OUTPUT_PATH = "results/deepseek_r1_reasoner_validation.json"

# 2. Parameters (Aligned for comparison)
TEMPERATURE = 0.8
TOP_P = 0.9
MAX_TOKENS = 500

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def generate_response(prompt):
    try:
        # Note: R1 handles 'reasoning_content' separately, but for the loop
        # we feed back the final 'content' to test the output stability.
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a research assistant exploring recursive information theory. Expand the following concept strictly and logically."},
                {"role": "user", "content": prompt}
            ],
            # Note: temperature is often restricted on R1, but we keep it 
            # for consistency where the provider allows it.
            max_tokens=MAX_TOKENS
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"  ⚠️ API Error: {e}")
        return None

def run_deepseek_forge():
    if not API_KEY:
        print("❌ Error: DEEPSEEK_API_KEY environment variable is not set.")
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

    print(f"🧠 ACTIVATING REASONER FORGE | Model: {MODEL_NAME}")
    
    for s_idx, seed in enumerate(seeds):
        print(f"🔴 Deep Reasoning Seed {s_idx+1}/10...")
        current_text = seed
        
        for i in range(50):
            output = generate_response(f"Expand: {current_text}")
            
            if output:
                results.append({
                    "iteration": i, 
                    "seed": s_idx, 
                    "condition": "closed_loop", 
                    "model": MODEL_NAME,
                    "text": output
                })
                current_text = output
                
                with open(OUTPUT_PATH, 'w') as f:
                    json.dump(results, f, indent=2)
                
                if (i+1) % 5 == 0: print(f"  ✅ {i+1} reasoning steps completed")
                time.sleep(2) # R1 needs more time to "think"
            else:
                print(f"  ❌ Seed {s_idx+1} failed at step {i}")
                break

    print(f"\n🏁 R1 MISSION COMPLETE! Data: {OUTPUT_PATH}")

if __name__ == "__main__":
    run_deepseek_forge()
