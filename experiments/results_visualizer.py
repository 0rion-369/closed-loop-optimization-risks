import json
import matplotlib.pyplot as plt
import sys

# On ajoute "../" car le script est maintenant dans experiments/
PATH_DATA = '../results/extended_validation_complete.json'
PATH_SAVE = '../results/final_analysis_visualization.png'

try:
    with open(PATH_DATA, 'r') as f:
        data = json.load(f)
    
    entropy = [it['shannon_entropy'] for it in data]
    complexity = [it['lz_complexity'] for it in data]
    iterations = range(len(entropy))

    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    ax1.set_xlabel('Itérations')
    ax1.set_ylabel('Entropie de Shannon', color='tab:red')
    ax1.plot(iterations, entropy, color='tab:red', linewidth=2, label='Entropie')
    ax1.tick_params(axis='y', labelcolor='tab:red')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Complexité LZ (Structure)', color='tab:blue')
    ax2.plot(iterations, complexity, color='tab:blue', linewidth=2, linestyle='--', label='Complexité')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    plt.title('Validation du Bruit Structuré : Entropie vs Complexité')
    fig.tight_layout()
    plt.savefig(PATH_SAVE)
    print(f"✅ Succès ! Graphique mis à jour dans {PATH_SAVE}")

except Exception as e:
    print(f"❌ Erreur de chemin : {e}")
