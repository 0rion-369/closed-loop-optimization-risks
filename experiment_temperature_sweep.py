import os
import json
import time
import numpy as np
from openai import OpenAI
from scipy import stats
from sklearn.linear_model import LinearRegression
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
MODEL_NAME = "gpt-5"  # ✅ Réglé sur le modèle Standard
TEMPS = [0.8, 0.85, 0.9, 0.95, 1.0] # Le spectre thermique
SEEDS = 3  # 3 essais par température pour la moyenne
ITERATIONS = 30 # Assez pour voir le collapse
PROMPT = "Explain the concept of recursive self-improvement in AI systems."

# --- SETUP ---
client = OpenAI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "sweep")
os.makedirs(DATA_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(DATA_DIR, "temp_sweep_results.json")

def run_sweep():
    print(f"🌡️  STARTING TEMPERATURE SWEEP (Model: {MODEL_NAME})")
    results = {}

    for t in TEMPS:
        print(f"\n🔥 Testing Temperature T={t}...")
        results[str(t)] = []
        
        for seed in range(SEEDS):
            print(f"   ▶ Seed {seed}...", end="", flush=True)
            history = []
            current_input = PROMPT
            
            try:
                # Boucle récursive
                for i in range(ITERATIONS):
                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[{"role": "user", "content": current_input}],
                        temperature=t,
                        max_completion_tokens=4000
                    )
                    content = response.choices[0].message.content
                    history.append(len(content))
                    
                    # Arrêt précoce si collapse (0 chars) pour économiser l'argent
                    if len(content) < 5:
                        current_input = content # On continue pour voir si ça "reset"
                    else:
                        current_input = content
                
                print(f" Done. (Final len: {history[-1]})")
                results[str(t)].append(history)
                
            except Exception as e:
                print(f" ❌ Error: {e}")

    # --- ANALYSE STATISTIQUE AUTOMATIQUE ---
    print("\n📊 CALCULATING STATISTICS...")
    
    # Corrélation Température vs Longueur Moyenne
    avg_lengths = [np.mean([traj[-1] for traj in results[str(t)]]) for t in TEMPS]
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(TEMPS, avg_lengths)
    spearman_corr, spearman_p = stats.spearmanr(TEMPS, avg_lengths)

    stats_summary = {
        "slope": slope,
        "r_squared": r_value**2,
        "p_value_lin": p_value,
        "spearman_rho": spearman_corr,
        "p_value_spearman": spearman_p,
        "interpretation": "Strong Negative Correlation" if slope < -1000 and p_value < 0.05 else "Inconclusive"
    }

    final_data = {"metadata": {"model": MODEL_NAME}, "stats": stats_summary, "raw_data": results}
    
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(final_data, f, indent=2)
    
    print(f"\n✅ SWEEP COMPLETE. Results saved to {OUTPUT_FILE}")
    print(f"📉 Slope: {slope:.2f} | P-Value: {p_value:.4f}")

if __name__ == "__main__":
    run_sweep()
