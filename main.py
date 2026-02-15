from lea_v1.core.brain import Brain
from lea_v1.config import Config
import time

def main():
    print(f"🤖 INITIALIZING {Config.AGENT_NAME}...")
    lea = Brain()
    
    # On lance une boucle de discussion infinie
    print("💬 LEA is listening. (Type 'quit' to stop, or just press Enter to let her think)")
    
    while True:
        try:
            user_input = input("\nYOU > ")
            if user_input.lower() in ['quit', 'exit']:
                break
            
            # Si l'utilisateur ne dit rien, on force LEA à continuer sa pensée (récursion)
            if not user_input:
                user_input = "Continue your thought stream."
            
            print("⏳ LEA is thinking...")
            response, length = lea.think(user_input)
            
            print(f"\nLEA ({length} chars) > {response}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\n🛑 SHUTTING DOWN.")
            break

if __name__ == "__main__":
    main()
