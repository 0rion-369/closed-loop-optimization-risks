import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    AGENT_NAME = "LEA (Logical Emotive Agent)"
    VERSION = "1.1.0-Bipolar-Regulator"
    
    PROVIDER = "ANTHROPIC"
    ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
    OPENAI_KEY = os.getenv("OPENAI_API_KEY")
    
    MODEL_FAST = "claude-3-haiku-20240307"
    
    # --- LES PARAMÈTRES VITAUX ---
    # Le plancher (Mort par silence)
    COLLAPSE_THRESHOLD = 600  
    # Le plafond (Délire graphomane) -> NOUVEAU !
    OVERHEAT_THRESHOLD = 2500 
    
    CONTEXT_WINDOW = 10
