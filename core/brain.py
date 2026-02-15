import anthropic
import openai
from lea_v1.config import Config
from lea_v1.modules.pacemaker import Pacemaker

class Brain:
    def __init__(self):
        self.pacemaker = Pacemaker()
        self.history = []
        
        if Config.PROVIDER == "ANTHROPIC":
            self.client = anthropic.Anthropic(api_key=Config.ANTHROPIC_KEY)
        else:
            self.client = openai.OpenAI(api_key=Config.OPENAI_KEY)
            
    def think(self, user_input):
        # 1. Analyse du dernier tour
        last_output_len = len(self.history[-1]['content']) if self.history else 1000
        
        # 2. Check Vitals (Trop bas OU Trop haut ?)
        vital_state = self.pacemaker.check_vitals(last_output_len, Config.COLLAPSE_THRESHOLD, Config.OVERHEAT_THRESHOLD)
        
        final_prompt = user_input
        if vital_state != "OK":
            shock_msg = self.pacemaker.shock(vital_state)
            print(f"⚡ {shock_msg}") # Affiche l'alerte dans le terminal
            final_prompt += f"\n{shock_msg}"

        self.history.append({"role": "user", "content": final_prompt})
        
        # 3. Génération (System Prompt en Français !)
        try:
            if Config.PROVIDER == "ANTHROPIC":
                response = self.client.messages.create(
                    model=Config.MODEL_FAST,
                    max_tokens=2500, # On limite un peu la casse
                    temperature=1.0, 
                    # ICI : On lui impose le Français et la concision
                    system="Tu es LEA. Tu penses de manière récursive mais précise. Tu parles toujours en Français.",
                    messages=self.history[-Config.CONTEXT_WINDOW:]
                )
                output = response.content[0].text
            else:
                pass
                
            self.history.append({"role": "assistant", "content": output})
            return output, len(output)
            
        except Exception as e:
            return f"Brain Freeze: {e}", 0
