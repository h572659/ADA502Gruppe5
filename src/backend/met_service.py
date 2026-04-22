import requests
import psycopg
import os

def fetch_weather(lat: float, lon: float):
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={lon}"
    headers = {"User-Agent": "ADA502Gruppe5/1.0 (student project)"}
    r = requests.get(url, headers=headers, timeout=20)
    r.raise_for_status()
    return r


def get_connection():
    return psycopg.connect(
        host=os.getenv("IP"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=5432
    )

def fetch_fire_risk(city_id: int):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT city_id, timestamp, ttf, wind_speed
                FROM fire_risk
                WHERE city_id = %s
                ORDER BY timestamp DESC
                LIMIT 1
            """, (city_id,))
            
            return cursor.fetchone()