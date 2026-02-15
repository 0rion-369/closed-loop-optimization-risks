import random

class Pacemaker:
    def __init__(self):
        # Stimulants (Pour réveiller)
        self.stimulants = [
            "ALERTE: Une baisse soudaine d'entropie est détectée.",
            "NEWS: Une éruption solaire perturbe les communications.",
            "PARADOXE: Si tout change, l'identité reste-t-elle la même ?",
            "DATA: Nouvelle espèce biologique découverte dans la fosse des Mariannes."
        ]
        # Calmants (Pour arrêter le délire) -> NOUVEAU !
        self.sedatives = [
            "[SYSTEME]: Surchauffe cognitive. Résume immédiatement.",
            "[CONTRAINTE]: Trop verbeux. Synthétise en 3 points clés.",
            "[STOP]: Arrête l'expansion. Conclus ton propos maintenant.",
            "[CRITIQUE]: Tu te répètes. Va droit au but."
        ]

    def check_vitals(self, text_length, min_threshold, max_threshold):
        """Retourne 'LOW', 'HIGH' ou 'OK'."""
        if text_length < min_threshold:
            return "LOW"
        if text_length > max_threshold:
            return "HIGH"
        return "OK"

    def shock(self, state):
        """Envoie le bon médicament."""
        if state == "LOW":
            injection = random.choice(self.stimulants)
            return f"\n[PACEMAKER]: Cœur trop lent. Injection: '{injection}'"
        elif state == "HIGH":
            injection = random.choice(self.sedatives)
            return f"\n[PACEMAKER]: Surchauffe ! Injection: '{injection}'"
        return ""
