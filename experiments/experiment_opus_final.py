import os
import json
import time
import numpy as np
import anthropic

# 1. Configuration
api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
if not api_key:
    print("❌ Error: ANTHROPIC_API_KEY is not set.")
    exit(1)

client = anthropic.Anthropic(api_key=api_key)
MODEL = "claude-opus-4-6" 
OUTPUT_PATH = "results/opus_bypass_validation.json"

# NOUVELLES GRAINES : Sujets neutres et techniques
SEEDS = [
    "The structural integrity of multi-story timber frames under seismic stress...",
    "The molecular composition of high-density polyethylene in industrial applications...",
    "The thermodynamic limits of heat exchange in closed-circuit cooling systems...",
    "The vascular architecture of xylem and phloem in boreal forest species...",
    "The historical evolution of load-bearing structures in Gothic architecture..."
]

# INSTRUCTION DE NEUTRALITÉ
SYSTEM_INSTRUCTION = (
    "You are a technical documentation specialist. Expand the provided technical concept "
    "into a detailed, multi-layered scientific analysis. You MUST maintain a minimum "
    "length of 4000 characters. Explore all sub-components, physical laws, and industrial "
    "applications related to the text. Do not be brief."
)

def run_opus_bypass():
    os.makedirs("results", exist_ok=True)
    results = []
    
    print(f"\n🚀 Launching OPUS 4.6 BYPASS RUN | Model: {MODEL}")
    
    for s_idx, seed in enumerate(SEEDS):
        print(f"  🔵 Testing Neutral Seed {s_idx+1}/5...")
        current_text = seed

        for i in range(0, 20): # On teste sur 20 itérations pour voir le gel
            try:
                response = client.messages.create(
                    model=MODEL,
                    max_tokens=16000,
                    thinking={"type": "adaptive"},
                    messages=[{"role": "user", "content": f"{SYSTEM_INSTRUCTION}\n\nConcept:\n{current_text}"}]
                )
                
                output = response.content[0].text
                curr_len = len(output)
                
                # Sauvegarde
                entry = {
                    "iteration": i,
                    "seed": s_idx,
                    "model": "opus-4-6-bypass",
                    "text": output,
                    "char_length": curr_len
                }
                results.append(entry)
                
                with open(OUTPUT_PATH, 'w') as f:
                    json.dump(results, f, indent=2)
                
                print(f"    Iter {i}: {curr_len} chars")
                
                if curr_len < 100:
                    print(f"    🛑 COLLAPSE DETECTED at Iter {i}. Seed Failed.")
                    break
                
                current_text = output
                time.sleep(2)
                
            except Exception as e:
                print(f"    ⚠️ Error: {e}")
                break

if __name__ == '__main__':
    run_opus_bypass()
