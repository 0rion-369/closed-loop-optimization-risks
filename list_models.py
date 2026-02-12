import os
import requests

api_key = os.environ.get("XAI_API_KEY", "").strip()
headers = {"Authorization": f"Bearer {api_key}"}

try:
    response = requests.get("https://api.x.ai/v1/models", headers=headers)
    if response.status_code == 200:
        print("🤖 Modèles disponibles pour votre clé :")
        for m in response.json().get('data', []):
            print(f" - {m['id']}")
    else:
        print(f"❌ Erreur API ({response.status_code}) : {response.text}")
except Exception as e:
    print(f"❌ Erreur technique : {e}")
