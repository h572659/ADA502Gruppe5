from fastapi import FastAPI, Header, HTTPException, status, Depends
import os
from .met_service import fetch_weather
from .frcm_service import calculate_fire_risk
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from .auth import get_user_info, verify_user_role, verify_admin_role
from .indicator import indication

app = FastAPI()

API_KEY = os.getenv("API_KEY", "superhemmelig")

def require_api_key(x_api_key: str | None):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")


app.mount("/static-docs", StaticFiles(directory="/app/web-docs/site", html=True), name="static-docs")

@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/static-docs")

@app.get("/public/server_status")
def server_status():
    return {
        "Sever status for API, no authentication required": "ok",
        "status": "ok",
        "code": status.HTTP_200_OK,
        "message": "Server is running."
    }

@app.get("/user/met")
def met(
    lat: float,
    lon: float,
    user: bool = Depends(verify_user_role),
):
    return {**fetch_weather(lat, lon).json(), "message": "Weather data collected for users and admins."}

@app.get("/user/risk")
def risk(
    lat: float,
    lon: float,
    user: bool = Depends(verify_user_role),
):
    met_json = fetch_weather(lat, lon).json()
    result = calculate_fire_risk(met_json)
    temperature = result.get("air_temperature")
    if temperature is not None:
        result["indication"] = indication(temperature)
    return {"lat": lat, "lon": lon, "frcm_result": result}

@app.get("/admin/only")
def admin_only(admin: bool = Depends(verify_admin_role)):
    return {"message": "This endpoint is only accessible for admins."}