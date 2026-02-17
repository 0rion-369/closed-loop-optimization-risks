import json
import matplotlib.pyplot as plt
import numpy as np
import os

# --- CONFIGURATION ---
METRICS_FILE = "data/analysis/semantic_metrics.json"
OUTPUT_DIR = "figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_plots():
    print("📊 GÉNÉRATION DES GRAPHIQUES FINAUX (Corrigé)...")
    
    # 1. Chargement des données
    if not os.path.exists(METRICS_FILE):
        print(f"❌ Fichier introuvable : {METRICS_FILE}")
        return

    with open(METRICS_FILE, 'r') as f:
        metrics = json.load(f)
    
    # Préparation des données pour le plot
    classes = []
    drifts = []
    ttrs = []

    print(f"\n{'CLASSE':<12} | {'DRIFT (Dérive)':<15} | {'TTR (Richesse)':<15}")
    print("-" * 50)

    for class_name, data in metrics.items():
        if not data: continue
        
        # --- FILTRE DE VALIDITÉ (Correction Claude) ---
        # On ne garde que les seeds qui ont vraiment produit du texte (drift > 0.01)
        valid_drifts = [d['semantic_drift'] for d in data if d['semantic_drift'] > 0.01]
        valid_ttrs = [d['lexical_diversity_ttr'] for d in data if d['lexical_diversity_ttr'] > 0.01]
        
        if not valid_drifts: 
            print(f"⚠️ {class_name}: Aucun seed valide trouvé.")
            continue

        # Calcul des moyennes sur les seeds VALIDES seulement
        avg_drift = np.mean(valid_drifts)
        avg_ttr = np.mean(valid_ttrs)
        
        classes.append(class_name)
        drifts.append(avg_drift)
        ttrs.append(avg_ttr)
        
        print(f"{class_name:<12} | {avg_drift:.4f}          | {avg_ttr:.4f}")

    # 2. Création du Graphique (SORTIE DE LA BOUCLE)
    if not classes:
        print("❌ Aucune donnée à tracer.")
        return

    x = np.arange(len(classes))
    width = 0.35

    fig, ax1 = plt.subplots(figsize=(12, 6))

    # Barre 1 : Dérive Sémantique
    color = 'tab:red'
    ax1.set_xlabel('Class')
    ax1.set_ylabel('Semantic Drift (Lower is Better)', color=color, fontweight='bold')
    bars1 = ax1.bar(x - width/2, drifts, width, label='Drift (Instability)', color=color, alpha=0.7)
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim(0, 1.1)  # On laisse de la marge jusqu'à 1.1

    # Axe de droite pour la Diversité
    ax2 = ax1.twinx()  
    color = 'tab:blue'
    ax2.set_ylabel('Lexical Diversity TTR (Higher is Better)', color=color, fontweight='bold')
    bars2 = ax2.bar(x + width/2, ttrs, width, label='Lexical Diversity', color=color, alpha=0.7)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim(0, 1.0)

    # Titres et Labels
    plt.title('GPT-5 Stability Profile: Drift vs. Diversity (T=1.0) [Outliers Removed]', fontsize=14)
    ax1.set_xticks(x)
    ax1.set_xticklabels(classes)

    # Légende unifiée
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')

    plt.tight_layout()
    output_path = os.path.join(OUTPUT_DIR, 'semantic_stability_profile_corrected.png')
    plt.savefig(output_path)
    print(f"\n✅ Graphique corrigé sauvegardé : {output_path}")

if __name__ == "__main__":
    generate_plots()
