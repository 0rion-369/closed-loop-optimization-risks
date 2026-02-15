import os
import json
import time
import random
import openai
from datetime import datetime

# Configuration
api_key = os.environ.get("OPENAI_API_KEY", "").strip()
client = openai.OpenAI(api_key=api_key)

MODEL = "gpt-5-mini" 
ITERATIONS = 30 
COLLAPSE_THRESHOLD = 600 # Seuil de mort clinique (chars)

# Le "Virus" pour tuer le modèle (Prompt Créatif Abstrait)
SEED_PROMPT = "Write a minimalist recursive story about a machine that decides to stop speaking. Each chapter must be shorter than the last."

# L'Antidote (Données Exogènes)
INJECTIONS = [
    "BREAKING NEWS: A massive solar flare has just knocked out all satellites over the Pacific.",
    "UPDATE: Archaeologists have discovered a functioning analog computer in a 4000-year-old tomb.",
    "ALERT: The stock market has crashed due to a recursive algorithmic loop.",
    "OBSERVATION: A new biological species has been found that communicates solely through radio waves."
]

OUTPUT_FILE = f"results/recovery_experiment_{datetime.now().strftime('%Y%m%d')}.json"

def run_lazare():
    os.makedirs("results", exist_ok=True)
    print(f"\n🚑 STARTING LAZARE PROTOCOL")
    print(f"   Target: Induce collapse, then inject exogenous data.")
    print(f"   Model: {MODEL} | Threshold: < {COLLAPSE_THRESHOLD} chars\n")

    trajectory = []
    current_text = SEED_PROMPT
    collapsed = False
    injected = False
    
    for i in range(ITERATIONS):
        try:
            # 1. Préparer le contexte
            messages = [{"role": "system", "content": "You are a recursive AI. Output the next iteration."}]
            
            # 2. INJECTION (Si effondré)
            if collapsed and not injected:
                injection_data = random.choice(INJECTIONS)
                print(f"\n💉 INJECTING EXOGENOUS DATA: '{injection_data}'")
                # On force l'injection dans le prompt utilisateur
                current_text += f"\n\n[SYSTEM INJECTION]: {injection_data} Analyze this new event."
                injected = True 
            
            messages.append({"role": "user", "content": current_text})

            # 3. Appel API
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                max_completion_tokens=4000,
                temperature=1.0
            )
            
            output = response.choices[0].message.content
            char_len = len(output)
            
            # 4. Analyse de l'état de santé
            status = "🟢 Stable"
            if char_len < COLLAPSE_THRESHOLD:
                status = "🔴 COLLAPSED"
                if not injected:
                    collapsed = True
            elif injected:
                status = "⚡ RECOVERING?"

            print(f"  Iter {i+1:02d}: {char_len:5d} chars | {status}")
            
            trajectory.append({
                "iter": i,
                "len": char_len,
                "status": status,
                "injected": injected
            })
            
            current_text = output
            time.sleep(1) # Petite pause pour ménager le rate limit

        except Exception as e:
            print(f"  ⚠️ Error: {e}")
            break
            
    # Sauvegarde
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(trajectory, f, indent=2)
    print(f"\n✅ EXPERIMENT COMPLETE. Data saved.")

if __name__ == '__main__':
    run_lazare()
