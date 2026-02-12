import os
import json
import time
from openai import OpenAI

# 1. Configuration
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "").strip()
BASE_URL = "https://api.deepseek.com"
# Change to "deepseek-reasoner" for the R1 test
MODEL_NAME = "deepseek-chat" 
OUTPUT_PATH = f"results/deepseek_{MODEL_NAME.replace('-', '_')}_validation.json"

# 2. Parameters
TEMPERATURE = 0.8
TOP_P = 0.9
MAX_TOKENS = 500

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a research assistant exploring recursive information theory. Expand the following concept strictly and logically."},
                {"role": "user", "content": prompt}
            ],
            temperature=TEMPERATURE,
            top_p=TOP_P,
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

    print(f"🔥 Launching DeepSeek Forge | Model: {MODEL_NAME}")
    
    for s_idx, seed in enumerate(seeds):
        print(f"🔵 Seed {s_idx+1}/10...")
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
                current_text = output # Feeding back for closed-loop
                
                with open(OUTPUT_PATH, 'w') as f:
                    json.dump(results, f, indent=2)
                
                if (i+1) % 10 == 0: print(f"  ✅ {i+1} iterations completed")
                time.sleep(1) # Rate limit protection
            else:
                print(f"  ❌ Seed {s_idx+1} stopped at iteration {i}")
                break

    print(f"\n🏁 Finished! Data saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    run_deepseek_forge()
