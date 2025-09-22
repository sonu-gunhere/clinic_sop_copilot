import requests, os

API_KEY = os.getenv("SERPER_API_KEY")  # Add key in .env

def search(query: str):
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": API_KEY, "Content-Type": "application/json"}
    payload = {"q": query}
    response = requests.post(url, headers=headers, json=payload)
    return response.json()
