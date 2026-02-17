from fastapi import FastAPI, Header, HTTPException
import os

app = FastAPI()

API_KEY = os.getenv("API_KEY", "superhemmelig")

def require_api_key(x_api_key: str | None):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/")
def read_root(x_api_key: str | None = Header(default=None, alias="X-API-KEY")):
    require_api_key(x_api_key)
    return {"message": "Fire risk API is running (secured)"}
