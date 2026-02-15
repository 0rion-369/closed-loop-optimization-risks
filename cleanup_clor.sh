#!/bin/bash

echo "🚨 DÉMARRAGE DU PROTOCOLE DE NETTOYAGE 'PEER-REVIEW'..."

# --- CRÉATION STRUCTURE ---
mkdir -p analysis
mkdir -p data/raw
mkdir -p docs/archive
mkdir -p experiments
mkdir -p figures

# --- NETTOYAGE (git rm) ---
echo "🗑️ Suppression des fichiers obsolètes..."
# Fichiers racine
git rm --ignore-unmatch list_models.py install.sh requirements.txt 2>/dev/null

# Expériences obsolètes
git rm --ignore-unmatch experiments/experiment_free_tier.py \
    experiments/experiment_haiku_tier.py \
    experiments/experiment_o1_dual.py \
    experiments/experiment_gpt5_dual.py \
    experiments/experiment_gpt5_pilot.py \
    experiments/experiment_robustness_pilot.py \
    experiments/test_setup.py \
    experiments/test_grok.py \
    experiments/list_grok_models.py \
    experiments/run_exogenous.py \
    experiments/run_exogenous_stable.py \
    experiments/resume_haiku_exogenous.py \
    experiments/semantic_drift_analyzer.py \
    experiments/results_visualizer.py \
    experiments/final_grok_visualizer.py \
    experiments/final_haiku_visualizer.py \
    experiments/master_model_comparison.py \
    experiments/triple_comparison.py 2>/dev/null

# Code LEA (Hors-Sujet)
git rm -r --ignore-unmatch core modules 2>/dev/null
git rm --ignore-unmatch core/brain.py core/memory.py modules/pacemaker.py modules/kinetic_rng.py 2>/dev/null

# Docs internes
git rm --ignore-unmatch FINAL_REPORT_PHASE_3.md \
    PHASE_3_1_ROBUSTNESS_REPORT.md \
    reports/DEEPSEEK_R1_FINAL.md \
    reports/DEEPSEEK_V3_STATUS.md \
    notes/ORIGIN_METHODOLOGY.md \
    RESEARCH_ROADMAP_2026.md \
    docs/EMPIRICAL_VALIDATION.md \
    docs/CORE_FRAMEWORK.md 2>/dev/null

# --- RANGEMENT (mv) ---
echo "📦 Rangement des fichiers essentiels..."
mv analysis/plot_results.py analysis/ 2>/dev/null
mv analysis/compare_models.py analysis/ 2>/dev/null
mv experiments/plot_results.py analysis/ 2>/dev/null
mv experiments/compare_models.py analysis/ 2>/dev/null

# JSONs et Images
mv results/*.json data/raw/ 2>/dev/null
if [ -d "results" ]; then
    mv results/*.json data/raw/ 2>/dev/null
    rmdir results 2>/dev/null
fi
mv *.png figures/ 2>/dev/null
mv results/*.png figures/ 2>/dev/null

# --- GITIGNORE ---
echo "🛡️ Mise à jour du .gitignore..."
cat << 'GITIGNORE' > .gitignore
__pycache__/
*.pyc
.DS_Store
.env
.venv/
GITIGNORE

echo "✅ NETTOYAGE TERMINÉ."
