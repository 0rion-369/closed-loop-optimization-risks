import math
import random
from collections import Counter

class Pacemaker:
    def __init__(self, mode="AGENT"):
        self.mode = mode  # "RESEARCH" (Observe) ou "AGENT" (Intervient)
        self.stats_history = []

    def calculate_entropy(self, text):
        """Calcule l'entropie de Shannon du texte (densité d'information)."""
        if not text: return 0
        counts = Counter(text)
        total = len(text)
        return -sum((count/total) * math.log2(count/total) for count in counts.values())

    def check_vitals(self, text, config):
        """Analyse multidimensionnelle de la santé cognitive."""
        h_entropy = self.calculate_entropy(text)
        length = len(text)
        
        # Diagnostic
        state = "OK"
        if h_entropy < config.ENTROPY_THRESHOLD or length < config.COLLAPSE_THRESHOLD:
            state = "COLLAPSE"
        elif length > config.OVERHEAT_THRESHOLD:
            state = "OVERHEAT"
            
        # Archive pour la recherche
        self.stats_history.append({"H": h_entropy, "L": length, "state": state})
        
        return state, h_entropy

    def shock(self, state):
        """Décide d'intervenir ou non selon le mode."""
        if self.mode == "RESEARCH":
            # En mode recherche, on ne modifie pas le prompt, on observe l'effondrement
            return "" 
            
        if state == "COLLAPSE":
            # Ici on pourra brancher ton Kinetic-RNG plus tard
            return "\n[PACEMAKER]: Entropie critique. Injection de chaos exogène requise."
        if state == "OVERHEAT":
            return "\n[PACEMAKER]: Surchauffe détectée. Force la synthèse sémantique."
        return ""
