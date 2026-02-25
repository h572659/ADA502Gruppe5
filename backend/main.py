from fastapi import FastAPI, Header, HTTPException
import os
from met_service import fetch_weather
from frcm_service import calculate_fire_risk



app = FastAPI()


API_KEY = os.getenv("API_KEY", "superhemmelig")

def require_api_key(x_api_key: str | None):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/")
def read_root(x_api_key: str | None = Header(default=None, alias="X-API-KEY")):
    require_api_key(x_api_key)
    return {"message": "Fire risk API is running (secured)"}

@app.get("/met")
def met(
    lat: float,
    lon: float,
    x_api_key: str | None = Header(default=None, alias="X-API-KEY")
):
    require_api_key(x_api_key)
    return fetch_weather(lat, lon)

@app.get("/risk")
def risk(
    lat: float,
    lon: float,
    x_api_key: str | None = Header(default=None, alias="X-API-KEY")
):
    require_api_key(x_api_key)
    met_json = fetch_weather(lat, lon)
    result = calculate_fire_risk(met_json)
    return {"lat": lat, "lon": lon, "frcm_result": result}
