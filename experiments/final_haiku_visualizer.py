import json
import os
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def shannon_entropy(text):
    if not text or len(text) == 0: return 0
    prob = [n/len(text) for n in Counter(text).values()]
    return -sum(p * np.log2(p) for p in prob)

def process_file(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    iters = sorted(list(set(d['iteration'] for d in data)))
    entropy_avg = []
    for i in iters:
        batch = [d['text'] for d in data if d['iteration'] == i]
        entropy_avg.append(np.mean([shannon_entropy(t) for t in batch]))
    return iters, entropy_avg

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
closed_file = os.path.join(BASE_DIR, "results", "haiku_extended_validation.json")
exog_file = os.path.join(BASE_DIR, "results", "haiku_exogenous_validation.json")

plt.figure(figsize=(10, 6))

if os.path.exists(closed_file):
    x_c, h_c = process_file(closed_file)
    plt.plot(x_c, h_c, label='Boucle Fermée (Effondrement)', color='#ff4757', linewidth=2.5)
    print("✅ Données Boucle Fermée chargées.")

if os.path.exists(exog_file):
    x_e, h_e = process_file(exog_file)
    plt.plot(x_e, h_e, label='Injection Exogène (Stabilité)', color='#2ed573', linewidth=2.5)
    print("✅ Données Exogènes chargées.")

plt.title('Validation Haiku : Effet de la Récursion sur l\'Entropie')
plt.xlabel('Itérations')
plt.ylabel('Entropie de Shannon (Bits)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(BASE_DIR, "results", "haiku_final_proof.png"))
print("🏁 Graphique généré : results/haiku_final_proof.png")
