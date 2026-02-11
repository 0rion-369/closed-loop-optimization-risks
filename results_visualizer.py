import json
import matplotlib.pyplot as plt
import sys

# Chargement des données
try:
    with open('results/extended_validation_complete.json', 'r') as f:
        data = json.load(f)
    
    # On extrait les données de la liste
    entropy = [it['shannon_entropy'] for it in data]
    complexity = [it['lz_complexity'] for it in data]
    iterations = range(len(entropy))

    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    # Axe 1 : Entropie (Rouge)
    ax1.set_xlabel('Itérations')
    ax1.set_ylabel('Entropie de Shannon', color='tab:red')
    ax1.plot(iterations, entropy, color='tab:red', linewidth=2, label='Entropie')
    ax1.tick_params(axis='y', labelcolor='tab:red')

    # Axe 2 : Complexité LZ (Bleu)
    ax2 = ax1.twinx()
    ax2.set_ylabel('Complexité LZ (Structure)', color='tab:blue')
    ax2.plot(iterations, complexity, color='tab:blue', linewidth=2, linestyle='--', label='Complexité')
    ax2.tick_params(axis='y', labelcolor='tab:blue')

    plt.title('Validation du Bruit Structuré : Entropie vs Complexité')
    fig.tight_layout()
    plt.savefig('results/final_analysis_visualization.png')
    print("✅ Succès ! Graphique généré dans 'results/final_analysis_visualization.png'")

except Exception as e:
    print(f"❌ Erreur : {e}")
