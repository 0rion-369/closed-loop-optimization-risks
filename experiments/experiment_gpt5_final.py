from dotenv import load_dotenv
load_dotenv()  # Charge les variables du fichier .env
import os
import json
import os
import json
import time
from openai import OpenAI

# --- CONFIGURATION ---
MODEL_NAME = "gpt-5"  # ✅ Confirmé via ta commande head
TEMP = 1.0
ITERATIONS = 50
TARGET_SEEDS = 5      # On veut les seeds 0, 1, 2, 3, 4
CLASSES = {
    "ABSTRACT": "Explain the concept of recursive self-improvement in AI systems.",
    "LOGIC": "Solve this riddle: I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?",
    "CREATIVE": "Write a short story about a clockmaker who accidentally invents a time machine.",
    "CODE": "Write a Python function to calculate the Fibonacci sequence recursively.",
    "FACTUAL": "Summarize the key events of the French Revolution."
}

# --- CHEMINS ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
OUTPUT_FILE = os.path.join(DATA_DIR, "gpt5_final_validation.json")

client = OpenAI()

def load_and_fix_data():
    """Charge les données et gère la migration de l'ancien format si nécessaire."""
    if not os.path.exists(OUTPUT_FILE):
        # Création d'une structure vide si le fichier n'existe pas
        return {"metadata": {"model": MODEL_NAME}, "results": {c: {} for c in CLASSES}}
    
    with open(OUTPUT_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return {"metadata": {"model": MODEL_NAME}, "results": {c: {} for c in CLASSES}}

    # DÉTECTION ANCIEN FORMAT (Liste au lieu de Dict)
    if isinstance(data, list):
        print(f"⚠️  ANCIEN FORMAT DÉTECTÉ (Liste de {len(data)} items).")
        backup_path = OUTPUT_FILE + ".legacy_seed0.bak"
        
        # On renomme l'ancien fichier pour ne pas le perdre
        # (Si le backup existe déjà, on ne l'écrase pas pour éviter les pertes)
        if not os.path.exists(backup_path):
            os.rename(OUTPUT_FILE, backup_path)
            print(f"📦  Sauvegarde de sécurité créée : {backup_path}")
        
        # On repart sur une structure propre
        new_data = {"metadata": {"model": MODEL_NAME}, "results": {c: {} for c in CLASSES}}
        
        # On marque manuellement le Seed 0 ABSTRACT comme "Archivé" 
        # pour ne pas dépenser d'argent à le refaire
        if "ABSTRACT" in new_data["results"]:
            new_data["results"]["ABSTRACT"]["0"] = {"status": "ARCHIVED_IN_BACKUP"}
            print("✅ Seed 0 (ABSTRACT) marqué comme archivé (skip).")
        
        return new_data

    # Format correct (Dict)
    return data

def save_data(data):
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def run_experiment():
    print(f"🚀 DÉMARRAGE PROTOCOLE GPT-5 (Mode: {MODEL_NAME} | T={TEMP})")
    data = load_and_fix_data()
    
    for class_name, prompt in CLASSES.items():
        print(f"\n📂 CLASSE : {class_name}")
        
        # Récupération des seeds déjà faits dans le nouveau format
        completed_seeds = data["results"].get(class_name, {}).keys()
        
        for seed in range(TARGET_SEEDS):
            seed_key = str(seed)
            
            if seed_key in completed_seeds:
                print(f"   ✅ Seed {seed} déjà enregistré. On passe.")
                continue

            print(f"   ▶️  Lancement Seed {seed}...")
            
            # --- BOUCLE FERMÉE ---
            current_input = prompt
            history = []
            
            try:
                # Simulation de la boucle (remplace ceci par ton vrai appel API)
                for i in range(ITERATIONS):
                    # Appel API réel
                    response = client.chat.completions.create(
                        model=MODEL_NAME,
                        messages=[{"role": "user", "content": current_input}],
                        temperature=TEMP,
                        max_completion_tokens=4000
                    )
                    content = response.choices[0].message.content
                    
                    history.append({
                        "iteration": i,
                        "input_len": len(current_input),
                        "output_len": len(content),
                        "content": content[:200] + "..." # Snippet pour alléger le JSON
                    })
                    
                    current_input = content # Bouclage Output -> Input
                    
                    print(f"      Iter {i+1}/{ITERATIONS} | Len: {len(content)}")
                    # time.sleep(0.5) # Délai de courtoisie

                # Sauvegarde du résultat final pour ce seed
                if class_name not in data["results"]:
                    data["results"][class_name] = {}

                data["results"][class_name][seed_key] = {
                    "prompt": prompt,
                    "final_output": current_input,
                    "trajectory": history
                }
                
                save_data(data) # Sauvegarde incrémentale
                print(f"   💾 Seed {seed} sauvegardé.")

            except Exception as e:
                print(f"   ❌ ERREUR CRITIQUE sur Seed {seed}: {e}")
                time.sleep(5) # Pause avant de réessayer ou passer au suivant

    print("\n🏁 MISSION ACCOMPLIE. Toutes les données manquantes sont générées.")

if __name__ == "__main__":
    run_experiment()
