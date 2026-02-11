import json
import os
import numpy as np
import matplotlib.pyplot as plt
import zlib
from collections import Counter

def shannon_entropy(text):
    prob = [n/len(text) for n in Counter(text).values()]
    return -sum(p * np.log2(p) for p in prob)

def load_and_process(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    iters = sorted(list(set(d['iteration'] for d in data)))
    entropy_avg = []
    
    for i in iters:
        batch = [d for d in data if d['iteration'] == i]
        
        # Si on a déjà le score (Sonnet)
        if 'shannon_entropy' in batch[0]:
            scores = [d['shannon_entropy'] for d in batch]
        # Sinon on le calcule (Haiku)
        else:
            scores = [shannon_entropy(d['text']) for d in batch]
            
        entropy_avg.append(np.mean(scores))
    
    return iters, entropy_avg

# Chemins
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sonnet_file = os.path.join(BASE_DIR, "results", "extended_validation_complete.json")
haiku_file = os.path.join(BASE_DIR, "results", "haiku_extended_validation.json")

plt.figure(figsize=(12, 6))

if os.path.exists(sonnet_file):
    x, h_sonnet = load_and_process(sonnet_file)
    plt.plot(x, h_sonnet, label='Entropy (Sonnet)', color='red', linewidth=2)
    print(f"✅ Sonnet traité.")

if os.path.exists(haiku_file):
    x, h_haiku = load_and_process(haiku_file)
    plt.plot(x, h_haiku, label='Entropy (Haiku)', color='orange', linestyle='--', linewidth=2)
    print(f"✅ Haiku traité.")

plt.title('Divergence de l\'Entropie : Sonnet vs Haiku (Closed-Loop)')
plt.xlabel('Itérations')
plt.ylabel('Entropie de Shannon (Bits)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig(os.path.join(BASE_DIR, "results", "model_comparison_entropy.png"))
print(f"📊 Analyse terminée ! Image : results/model_comparison_entropy.png")
