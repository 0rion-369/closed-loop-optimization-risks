import sys
import os
import time
import random

# --- CONFIGURATION DU PONT (BRIDGE) ---
# On ajoute le dossier parent au chemin pour pouvoir importer bio_guard
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

try:
    import bio_guard
except ImportError:
    print("⚠️  ALERTE: Module bio_guard.py introuvable dans 01_SOFTWARE.")
    sys.exit(1)

# --- CŒUR DU PROGRAMME ---
def run_entropic_zoo():
    print("🌀 Entropic Zoo Protocol: Initialization...")

    # 1. LE CHECKPOINT BIOLOGIQUE
    # Si le Bio-Guard dit "Non", le script s'arrête ici immédiatement.
    if not bio_guard.check_clearance():
        print("🛑  PROTOCOL ABORTED by Bio-Safety Lock.")
        return

    # 2. Si l'accès est autorisé (Optimized/Standard)
    print("\n✅  Access Granted. Starting Simulation...")
    entities = ["Chimera-Alpha", "Basilisk-Node", "Hydra-Loop"]
    
    for entity in entities:
        stability = random.randint(85, 99)
        print(f"   [+] Awakening {entity}... Stability: {stability}%")
        time.sleep(0.7) # Simulation de chargement
    
    print("\n🦖  The Zoo is active and stable.")
    print("    Log: Entropy levels within tolerant parameters.")

if __name__ == "__main__":
    run_entropic_zoo()