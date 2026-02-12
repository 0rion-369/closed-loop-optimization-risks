import os
import requests

api_key = os.environ.get("XAI_API_KEY")
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
payload = {"model": "grok-beta", "messages": [{"role": "user", "content": "Say 'Rock'"}], "temperature": 0.0}

try:
    response = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=payload)
    print(f"Réponse de Grok : {response.json()['choices'][0]['message']['content']}")
except Exception as e:
    print(f"❌ Erreur : {e}")
    print(f"Ta clé commence par : {api_key[:10] if api_key else 'Rien'}")
