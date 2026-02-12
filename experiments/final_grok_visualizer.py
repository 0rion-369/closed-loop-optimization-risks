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
    
    # Séparer les conditions
    closed_data = [d for d in data if d.get('condition') == 'closed_loop']
    exog_data = [d for d in data if d.get('condition') == 'exogenous']
    
    h_closed = [np.mean([shannon_entropy(d.get('text', '')) for d in closed_data if d['iteration'] == i]) for i in iters]
    h_exog = [np.mean([shannon_entropy(d.get('text', '')) for d in exog_data if d['iteration'] == i]) for i in iters]
    
    return iters, h_closed, h_exog

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
grok_file = os.path.join(BASE_DIR, "results", "grok_extended_validation.json")

plt.figure(figsize=(10, 6))

if os.path.exists(grok_file):
    x, h_c, h_e = process_file(grok_file)
    plt.plot(x, h_c, label='Grok : Boucle Fermée (Collapse)', color='#6c5ce7', linewidth=2.5)
    plt.plot(x, h_e, label='Grok : Exogène (Stabilité)', color='#a29bfe', linestyle='--', linewidth=2)
    print("✅ Données Grok analysées.")

plt.title('Validation Grok : Résilience de l\'Entropie')
plt.xlabel('Itérations')
plt.ylabel('Entropie de Shannon (Bits)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(BASE_DIR, "results", "grok_final_proof.png"))
print("🏁 Graphique Grok généré : results/grok_final_proof.png")
