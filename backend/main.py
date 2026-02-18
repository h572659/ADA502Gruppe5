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
    met_response = fetch_weather(lat, lon)
    return met_response.json()


@app.get("/risk")
def risk(
    lat: float,
    lon: float,
    x_api_key: str | None = Header(default=None, alias="X-API-KEY")
):
    require_api_key(x_api_key)
    met_response = fetch_weather(lat, lon)
    met_json = met_response.json()
    result = calculate_fire_risk(met_json)
    return {"lat": lat, "lon": lon, "frcm_result": result}


