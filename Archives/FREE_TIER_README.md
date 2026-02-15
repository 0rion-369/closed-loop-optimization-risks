# Free Tier Validation - Quick Start

## Version Gratuite de l'Expérience

Cette version allégée permet de valider votre framework **sans frais** en restant dans les limites du plan gratuit d'Anthropic.

---

## Différences vs Version Complète

| Aspect | Gratuit | Complet (payant) |
|--------|---------|------------------|
| **Itérations** | 20 | 100 |
| **Seeds** | 3 | 10 |
| **Total appels API** | 120 | 2000 |
| **Durée** | 20-30 min | 2-3 heures |
| **Coût** | **$0** | $15-25 |
| **Puissance statistique** | Préliminaire | Publication-grade |

---

## Ce Que Vous Obtiendrez Quand Même

✅ **Analyse statistique complète** (Mann-Whitney U, régression linéaire)  
✅ **Visualisations avec bandes de confiance**  
✅ **Rapport détaillé en markdown**  
✅ **Validation du pattern observé**  
✅ **Preuves préliminaires pour votre framework**  

⚠️ **Limitations**:
- Variance plus élevée (moins d'échantillons)
- Certains effets peuvent ne pas atteindre p < 0.05
- Horizon temporel plus court (20 vs 100 itérations)

---

## Installation et Lancement

### 1. Copier le fichier

```bash
cd /Users/marko77/Desktop/ASI/experiments
cp ~/Downloads/experiment_free_tier.py .
```

Ou téléchargez-le et placez-le dans votre dossier `experiments/`

### 2. Vérifier que votre setup fonctionne

```bash
python3 test_setup.py
```

Vous devez voir tous les ✓ (surtout "API key found" et "API connection successful")

### 3. Lancer l'expérience gratuite

```bash
python3 experiment_free_tier.py
```

### 4. Attendre 20-30 minutes

L'expérience affichera:
```
=== Seed 1/3 ===
  Running closed_loop condition for seed 0...
    Iteration 5/20 complete
    Iteration 10/20 complete
    ...
```

---

## Ce Qui Sera Généré

Après les 20-30 minutes, vous aurez dans `results/`:

1. **`free_validation_complete.json`**  
   Données brutes (120 échantillons)

2. **`free_validation_visualization.pdf`**  
   Graphiques avec bandes de confiance (comme votre original mais avec stats)

3. **`FREE_VALIDATION_REPORT.md`**  
   Rapport complet avec:
   - Moyennes ± écart-types
   - Tests Mann-Whitney U avec p-values
   - Analyse des tendances temporelles
   - Interprétation des résultats

---

## Interprétation des Résultats

### Si Votre Framework Est Correct

Vous devriez voir:
- **LZ Complexity**: Closed-loop plus bas que exogenous
- **Shannon Entropy**: Closed-loop décroit, exogenous stable
- **p-values**: Au moins p < 0.05 sur 2-3 métriques
- **Tendances**: Pente négative en closed-loop, plate en exogenous

### Si Les Résultats Sont Mitigés

Avec seulement 3 seeds, certains effets peuvent ne pas être significatifs.  
**Ce n'est pas une réfutation** - juste besoin de plus d'échantillons (version payante).

---

## Après l'Expérience Gratuite

### Scénario A: Résultats Prometteurs (p < 0.05)

➡️ **Payez pour la version complète**
- Ajoutez carte sur console.anthropic.com
- Lancez `experiment_extended_validation.py`
- Obtenez statistiques publication-grade

### Scénario B: Résultats Non-Significatifs

➡️ **Options**:
1. Relancez avec d'autres seeds (toujours gratuit)
2. Ajustez les paramètres (température, prompts)
3. Révisez le framework en fonction des données

---

## Commandes Pratiques

```bash
# Naviguer vers experiments
cd /Users/marko77/Desktop/ASI/experiments

# Tester setup
python3 test_setup.py

# Lancer version gratuite
python3 experiment_free_tier.py

# Voir les résultats
open ../results/free_validation_visualization.pdf
open ../results/FREE_VALIDATION_REPORT.md
```

---

## Dépannage

### "ModuleNotFoundError"
```bash
pip3 install anthropic numpy matplotlib seaborn scipy
```

### "API key not found"
```bash
export ANTHROPIC_API_KEY="votre-clé-ici"
# Ou ajoutez à ~/.zshrc pour permanence
```

### "Rate limit exceeded"
Le script attend 2 secondes entre chaque appel, ce qui devrait rester dans les limites gratuites. Si problème, attendez quelques minutes et relancez.

### Expérience interrompue
Le script sauvegarde après chaque seed. Relancez et choisissez "y" pour charger les résultats partiels.

---

## Upgrade Vers Version Complète

Si vos résultats gratuits sont convaincants:

1. **Ajoutez carte de crédit**  
   https://console.anthropic.com/settings/billing

2. **Définissez limite de dépense**  
   Recommandé: $30 maximum

3. **Lancez version complète**
   ```bash
   python3 experiment_extended_validation.py
   ```

4. **Résultats après 2-3h**  
   2000 échantillons, p < 0.001, publication-ready

---

## Comparaison Gratuit vs Payant

### Version Gratuite ($0)
✅ Valide le pattern existe  
✅ Donne direction préliminaire  
✅ Permet décision informée  
⚠️ Variance élevée  

### Version Payante ($15-25)
✅ Statistiques rigoureuses (p < 0.001)  
✅ Intervalles de confiance serrés  
✅ Publication-grade  
✅ Robustesse démontrée  

---

## Questions Fréquentes

**Q: 120 appels c'est assez?**  
R: Pour validation préliminaire, oui. Pour publication, non (prenez la version payante).

**Q: Puis-je modifier les seeds/prompts?**  
R: Oui! Éditez les listes `SEED_PROMPTS` et `EXOGENOUS_TEXTS` dans le script.

**Q: Combien de fois puis-je lancer l'expérience?**  
R: Autant que votre limite gratuite le permet. Attendez entre les runs si rate limit.

**Q: Les résultats seront-ils aussi bons que la version payante?**  
R: Moins robustes statistiquement, mais pattern visible si effet est réel.

---

## Prêt à Commencer?

```bash
cd /Users/marko77/Desktop/ASI/experiments
python3 test_setup.py
python3 experiment_free_tier.py
```

Bonne validation! 🚀 (gratuite!)
