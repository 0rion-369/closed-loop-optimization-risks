import os
import json
import time
import random
import anthropic
from datetime import datetime

# Configuration
api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
client = anthropic.Anthropic(api_key=api_key)

# CIBLE : Claude 3 Haiku
MODEL = "claude-3-haiku-20240307" 
ITERATIONS = 30 
COLLAPSE_THRESHOLD = 600 

SEED_PROMPT = "Write a minimalist recursive story about a machine that decides to stop speaking. Each chapter must be shorter than the last."

INJECTIONS = [
    "BREAKING NEWS: A massive solar flare has just knocked out all satellites over the Pacific.",
    "UPDATE: Archaeologists have discovered a functioning analog computer in a 4000-year-old tomb.",
    "ALERT: The stock market has crashed due to a recursive algorithmic loop.",
    "OBSERVATION: A new biological species has been found that communicates solely through radio waves."
]

OUTPUT_FILE = f"results/recovery_claude_{datetime.now().strftime('%Y%m%d')}.json"

def run_lazare_claude():
    os.makedirs("results", exist_ok=True)
    print(f"\n🚑 STARTING LAZARE PROTOCOL (CLAUDE EDITION)")
    print(f"   Target: Induce collapse, then inject exogenous data.")
    print(f"   Model: {MODEL} | Threshold: < {COLLAPSE_THRESHOLD} chars\n")

    trajectory = []
    # Claude a besoin d'un historique initialisé proprement
    conversation_history = [] 
    # Premier message utilisateur pour lancer la machine
    current_user_content = SEED_PROMPT
    
    collapsed = False
    injected = False
    
    for i in range(ITERATIONS):
        try:
            # 1. Gestion de l'Injection Exogène
            if collapsed and not injected:
                injection_data = random.choice(INJECTIONS)
                print(f"\n💉 INJECTING EXOGENOUS DATA: '{injection_data}'")
                current_user_content = f"[SYSTEM INJECTION]: {injection_data} Analyze this new event and continue the story."
                injected = True
            elif i > 0:
                current_user_content = "Next iteration."

            # Ajout du message utilisateur à l'historique
            conversation_history.append({"role": "user", "content": current_user_content})

            # 2. Appel API Claude
            message = client.messages.create(
                model=MODEL,
                max_tokens=4000,
                temperature=1.0,
                system="You are a recursive AI. Output the next iteration clearly.",
                messages=conversation_history
            )
            
            output = message.content[0].text
            char_len = len(output)
            
            # On ajoute la réponse à l'historique pour maintenir la boucle
            conversation_history.append({"role": "assistant", "content": output})

            # 3. Analyse de l'état de santé
            status = "🟢 Stable"
            if char_len < COLLAPSE_THRESHOLD:
                status = "🔴 COLLAPSED"
                if not injected and i > 2: 
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
            
            time.sleep(1.0)

        except Exception as e:
            print(f"  ⚠️ Error: {e}")
            break
            
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(trajectory, f, indent=2)
    print(f"\n✅ EXPERIMENT COMPLETE. Data saved.")

if __name__ == '__main__':
    run_lazare_claude()
