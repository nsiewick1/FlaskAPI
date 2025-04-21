import requests


API_URL = "http://34.85.238.67:5000/api/time"
TOKEN = "supersecrettoken123"
CAPITAL = "Berlin"

headers = {
    "Authorization": f"Bearer {TOKEN}"
}

params = {
    "capital": CAPITAL
}

response = requests.get(API_URL, headers=headers, params=params)

if response.status_code == 200:
    print("Success:", response.json())
else:
    print("Failed:", response.status_code, response.text)
