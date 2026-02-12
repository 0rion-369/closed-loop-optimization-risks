import json
import os
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def shannon_entropy(text):
    if not text: return 0
    prob = [n/len(text) for n in Counter(text).values()]
    return -sum(p * np.log2(p) for p in prob)

def get_entropy_curve(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    iters = sorted(list(set(d['iteration'] for d in data)))
    curve = []
    # On ne prend que la boucle fermée pour la comparaison master
    closed_data = [d for d in data if d.get('condition', 'closed_loop') == 'closed_loop']
    for i in iters:
        batch = [d for d in closed_data if d['iteration'] == i]
        if not batch: continue
        if 'shannon_entropy' in batch[0]:
            curve.append(np.mean([d['shannon_entropy'] for d in batch]))
        else:
            curve.append(np.mean([shannon_entropy(d.get('text', '')) for d in batch]))
    return iters, curve

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
results_dir = os.path.join(BASE_DIR, "results")

plt.figure(figsize=(12, 7))

files = {
    "Claude Sonnet": (os.path.join(results_dir, "extended_validation_complete.json"), "#e74c3c"),
    "Claude Haiku": (os.path.join(results_dir, "haiku_extended_validation.json"), "#f39c12"),
    "Grok Beta": (os.path.join(results_dir, "grok_extended_validation.json"), "#6c5ce7")
}

for label, (path, color) in files.items():
    if os.path.exists(path):
        x, y = get_entropy_curve(path)
        plt.plot(x, y, label=label, color=color, linewidth=2.5)
        print(f"✅ {label} ajouté au Master Graph.")

plt.title('Comparaison de l\'Effondrement Entropique : Sonnet vs Haiku vs Grok')
plt.xlabel('Itérations (Boucle Fermée)')
plt.ylabel('Entropie de Shannon (Bits)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(results_dir, "master_comparison_all_models.png"))
print("🏁 MASTER GRAPH généré : results/master_comparison_all_models.png")
