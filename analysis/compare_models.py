import json
import os
import numpy as np
import matplotlib.pyplot as plt
import zlib
from collections import Counter

def shannon_entropy(text):
    if not text: return 0
    prob = [n/len(text) for n in Counter(text).values()]
    return -sum(p * np.log2(p) for p in prob)

def load_and_process(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    iters = sorted(list(set(d['iteration'] for d in data)))
    entropy_avg = []
    
    for i in iters:
        batch = [d for d in data if d['iteration'] == i]
        
        # Détection du format : métrique pré-calculée ou texte brut
        if 'shannon_entropy' in batch[0]:
            scores = [d['shannon_entropy'] for d in batch]
        else:
            scores = [shannon_entropy(d.get('text', '')) for d in batch]
            
        entropy_avg.append(np.mean(scores))
    
    return iters, entropy_avg

# Configuration des chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sonnet_file = os.path.join(BASE_DIR, "results", "extended_validation_complete.json")
haiku_file = os.path.join(BASE_DIR, "results", "haiku_extended_validation.json")

plt.figure(figsize=(12, 7))

# Traitement Sonnet (La référence)
if os.path.exists(sonnet_file):
    x_s, h_s = load_and_process(sonnet_file)
    plt.plot(x_s, h_s, label='Entropy (Sonnet - Pro)', color='#e74c3c', linewidth=2.5)
    print(f"✅ Données Sonnet intégrées.")

# Traitement Haiku (Le test actuel)
if os.path.exists(haiku_file):
    x_h, h_h = load_and_process(haiku_file)
    plt.plot(x_h, h_h, label='Entropy (Haiku - Light)', color='#f39c12', linestyle='--', linewidth=2.5)
    print(f"✅ Données Haiku calculées.")

plt.title('Analyse de l\'Effondrement Entropique : Sonnet vs Haiku', fontsize=14)
plt.xlabel('Itérations (Boucle Fermée)', fontsize=12)
plt.ylabel('Entropie de Shannon (Bits)', fontsize=12)
plt.legend()
plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.tight_layout()

# Sauvegarde
output_path = os.path.join(BASE_DIR, "results", "model_comparison_entropy.png")
plt.savefig(output_path)
print(f"📊 Graphique comparatif généré : {output_path}")
