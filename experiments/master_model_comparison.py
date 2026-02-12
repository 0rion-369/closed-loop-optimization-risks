import json
import os
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def shannon_entropy(text):
    if not text or len(str(text)) == 0: return 0
    text_str = str(text)
    prob = [n/len(text_str) for n in Counter(text_str).values()]
    return -sum(p * np.log2(p) for p in prob)

def get_entropy_curve(file_path):
    if not os.path.exists(file_path):
        print(f"❌ Fichier introuvable : {file_path}")
        return None, None
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    if not data:
        print(f"⚠️ Le fichier {file_path} est vide !")
        return None, None

    iters = sorted(list(set(d['iteration'] for d in data)))
    curve = []
    # On filtre pour ne garder que la boucle fermée
    closed_data = [d for d in data if d.get('condition') == 'closed_loop']
    
    if not closed_data:
        print(f"⚠️ Aucune donnée 'closed_loop' dans {file_path}")
        return None, None

    for i in iters:
        batch = [d for d in closed_data if d['iteration'] == i]
        if batch:
            # Calcul direct de l'entropie
            curve.append(np.mean([shannon_entropy(d.get('text', '')) for d in batch]))
    
    return iters[:len(curve)], curve

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
results_dir = os.path.join(BASE_DIR, "results")

plt.figure(figsize=(12, 7))

# Liste des fichiers à tester
models = {
    "Claude Sonnet": os.path.join(results_dir, "extended_validation_complete.json"),
    "Claude Haiku": os.path.join(results_dir, "haiku_extended_validation.json"),
    "Grok Beta": os.path.join(results_dir, "grok_extended_validation.json")
}

colors = {"Claude Sonnet": "#e74c3c", "Claude Haiku": "#f39c12", "Grok Beta": "#6c5ce7"}

for name, path in models.items():
    x, y = get_entropy_curve(path)
    if x is not None:
        plt.plot(x, y, label=name, color=colors[name], linewidth=2.5)
        print(f"✅ {name} ajouté au graphique (n={len(x)})")

plt.title('Comparaison Master : Effondrement de l\'Entropie (n=3000+)')
plt.xlabel('Itérations')
plt.ylabel('Entropie de Shannon (Bits)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(results_dir, "master_comparison_all_models.png"))
print(f"🏁 MASTER GRAPH généré dans results/master_comparison_all_models.png")
