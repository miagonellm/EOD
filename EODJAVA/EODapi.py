import requests
import json

url = "https://api.x.ai/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer xai-epKWi7IPAiAY1EYFTZtrPXP1TZncGyIfswAKgtjFzRxgc54ooSzgzZZYgWKnwM2TLXCajfr0QRFeKEGU"
}
data = {
    "messages": [
        {"role": "system", "content": "test"},
        {"role": "user", "content": "hello"}
    ],
    "model": "grok-3-mini",
    "stream": False,
    "temperature": 0
}

response = requests.post(url, headers=headers, json=data)
print(response.text)
