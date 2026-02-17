import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

# --- CONFIGURATION ---
load_dotenv()
MODEL_NAME = "gpt-5" # Pour l'étiquetage des données
INPUT_FILE = "data/raw/gpt5_final_validation.json" # Il va lire tes données existantes (les Seeds à 20$)
OUTPUT_FILE = "data/analysis/semantic_metrics.json"

def run_validation():
    print("🧠 LOADING NLP MODEL (all-MiniLM-L6-v2)...")
    # Ce modèle tourne en local sur ton CPU (Gratuit)
    embedder = SentenceTransformer('all-MiniLM-L6-v2') 
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Fichier introuvable : {INPUT_FILE}. Lance d'abord experiment_gpt5_final.py")
        return

    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

    results = {}
    print(f"📂 ANALYZING DATA from {MODEL_NAME}...")

    for class_name, seeds in data['results'].items():
        print(f"   Processing Class: {class_name}")
        class_metrics = []

        for seed_id, seed_data in seeds.items():
            traj = seed_data.get('trajectory', [])
            if not traj: continue
            
            # 1. Extraction des textes
            texts = [t.get('content', '') for t in traj if len(t.get('content', '')) > 0]
            if len(texts) < 2: continue

            # 2. Vectorisation (Embeddings)
            embeddings = embedder.encode(texts)
            
            # 3. Métriques
            # Drift: Distance entre le début et la fin
            drift = 1 - cosine_similarity([embeddings[0]], [embeddings[-1]])[0][0]
            
            # Variance: Est-ce que le modèle tourne en rond (faible) ou explore (haute) ?
            variance = np.var(embeddings, axis=0).mean()
            
            # TTR (Type-Token Ratio) - Richesse du vocabulaire
            all_words = " ".join(texts).lower().split()
            unique_words = set(all_words)
            ttr = len(unique_words) / len(all_words) if all_words else 0

            class_metrics.append({
                "seed": seed_id,
                "semantic_drift": float(drift),
                "embedding_variance": float(variance),
                "lexical_diversity_ttr": float(ttr)
            })

        results[class_name] = class_metrics

    # Sauvegarde
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✅ VALIDATION COMPLETE. Metrics saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    run_validation()
