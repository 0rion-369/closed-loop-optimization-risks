import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AGENT_NAME = "LEA-v1.2 (Entropy Observer)"
    
    # --- MODES ---
    # RESEARCH = Collecte pure sans intervention (pour tes papiers scientifiques)
    # AGENT = Mode survie actif (pour discuter avec elle)
    MODE = "AGENT" 

    PROVIDER = "ANTHROPIC"
    ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # --- SEUILS COGNITIFS ---
    COLLAPSE_THRESHOLD = 600  #
    OVERHEAT_THRESHOLD = 2500 #
    ENTROPY_THRESHOLD = 3.5   # Sous 3.5, le texte est jugé trop répétitif
    
    CONTEXT_WINDOW = 10
    MODEL_FAST = "claude-3-haiku-20240307"
