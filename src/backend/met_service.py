import requests

def fetch_weather(lat: float, lon: float):
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}"
    headers = {"User-Agent": "ADA502Gruppe5/1.0 (student project)"}
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    return r
