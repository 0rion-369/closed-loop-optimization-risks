import json
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import os

# --- CONFIGURATION ---
LENGTH_FILE = "data/raw/gpt5_final_validation.json"
METRICS_FILE = "data/analysis/semantic_metrics.json"
OUTPUT_DIR = "figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_analysis():
    print("🕵️  LANCEMENT DE L'ANALYSE RUN-LEVEL (N~20)...")

    # 1. Chargement des données
    if not os.path.exists(LENGTH_FILE) or not os.path.exists(METRICS_FILE):
        print("❌ Fichiers manquants. Vérifie que tu as bien lancé les exp 1 et 2.")
        return

    with open(LENGTH_FILE, 'r') as f:
        len_data = json.load(f)
    with open(METRICS_FILE, 'r') as f:
        sem_data = json.load(f)

    # 2. Alignement des données (Match par Class + Seed)
    x_lengths = []
    y_drifts = []
    labels = []
    colors = []
    
    class_colors = {
        'ABSTRACT': 'red', 'LOGIC': 'blue', 'CREATIVE': 'green', 
        'CODE': 'orange', 'FACTUAL': 'purple'
    }

    print(f"\n{'CLASSE':<10} | {'SEED':<4} | {'LEN':<8} | {'DRIFT':<8}")
    print("-" * 45)

    for class_name, seeds in sem_data.items():
        for seed_metric in seeds:
            seed_id = seed_metric['seed']
            drift = seed_metric['semantic_drift']
            
            # FILTRE : On ignore les plantages (Drift ~ 0.0)
            if drift < 0.01: continue
            
            # Récupération de la longueur correspondante
            try:
                traj = len_data['results'][class_name][seed_id]['trajectory']
                # On prend la longueur moyenne de la trajectoire
                lens = [t['output_len'] for t in traj]
                avg_len = np.mean(lens) if lens else 0
            except KeyError:
                continue

            x_lengths.append(avg_len)
            y_drifts.append(drift)
            labels.append(class_name)
            colors.append(class_colors.get(class_name, 'black'))
            
            print(f"{class_name:<10} | {seed_id:<4} | {int(avg_len):<8} | {drift:.4f}")

    # 3. Calcul Statistique (Spearman Run-Level)
    if len(x_lengths) < 5:
        print("❌ Pas assez de données valides.")
        return

    spearman_rho, p_value = stats.spearmanr(x_lengths, y_drifts)
    
    print("\n📊 RÉSULTATS STATISTIQUES (RUN-LEVEL)")
    print("-" * 30)
    print(f"Nombre de points (N) : {len(x_lengths)}")
    print(f"Spearman Rho         : {spearman_rho:.4f}")
    print(f"P-Value              : {p_value:.4f}")

    # Interprétation automatique
    if p_value > 0.05:
        verdict = "❌ NON SIGNIFICATIF (Random Noise)"
    elif abs(spearman_rho) > 0.7:
        verdict = "✅ CORRÉLATION FORTE (Loi confirmée)"
    elif abs(spearman_rho) > 0.3:
        verdict = "⚠️ CORRÉLATION FAIBLE (Tendance)"
    else:
        verdict = "❌ AUCUNE CORRÉLATION (Indépendance)"
    
    print(f"Verdict              : {verdict}")

    # 4. Génération du Scatter Plot
    plt.figure(figsize=(10, 6))
    
    # Points
    for i in range(len(x_lengths)):
        plt.scatter(x_lengths[i], y_drifts[i], color=colors[i], alpha=0.7, s=100, label=labels[i] if labels[i] not in plt.gca().get_legend_handles_labels()[1] else "")

    # Ligne de tendance (juste pour visualiser)
    z = np.polyfit(x_lengths, y_drifts, 1)
    p = np.poly1d(z)
    plt.plot(x_lengths, p(x_lengths), "k--", alpha=0.3)

    plt.xlabel("Mean Trajectory Length (chars)")
    plt.ylabel("Semantic Drift (0-1)")
    plt.title(f"Run-Level Correlation: Length vs Drift (N={len(x_lengths)})\nRho={spearman_rho:.2f}, p={p_value:.3f}")
    plt.legend(title="Class")
    plt.grid(True, alpha=0.3)
    
    output_path = os.path.join(OUTPUT_DIR, "run_level_correlation.png")
    plt.savefig(output_path)
    print(f"\n✅ Plot sauvegardé : {output_path}")

if __name__ == "__main__":
    run_analysis()
