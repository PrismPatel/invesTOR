# scripts/load_api_to_postgres.py

import requests
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# API setup
API_URL = "https://axesso-zillow-data-service.p.rapidapi.com/search"
headers = {
    "x-rapidapi-host": "axesso-zillow-data-service.p.rapidapi.com",
    "x-rapidapi-key": os.getenv("RAPIDAPI_KEY"),
}
params = {
    "location": "10001",
    "sortSelection": "priorityscore",
    "status": "forSale",
    "listing_type": "by_agent",
    "doz": "any"
}

# PostgreSQL setup
conn = psycopg2.connect(
    host=os.getenv("PG_HOST"),
    port=os.getenv("PG_PORT"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    database=os.getenv("PG_DATABASE")
)
cur = conn.cursor()

# Fetch data
response = requests.get(API_URL, headers=headers, params=params)
data = response.json()

# Insert into DB
for prop in data.get("listResults", []):
    try:
        cur.execute("""
            INSERT INTO properties (
                zpid, address, zipcode, price, bedrooms, bathrooms,
                area, home_type, status, latitude, longitude,
                days_on_market, broker_name
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (zpid) DO NOTHING
        """, (
            prop.get("zpid"),
            prop.get("address"),
            prop.get("zipcode"),
            prop.get("price"),
            prop.get("bedrooms"),
            prop.get("bathrooms"),
            prop.get("livingArea"),
            prop.get("homeType"),
            prop.get("statusType"),
            prop.get("latitude"),
            prop.get("longitude"),
            prop.get("daysOnZillow"),
            prop.get("brokerName")
        ))
    except Exception as e:
        print("Error inserting:", prop.get("zpid"), e)

conn.commit()
cur.close()
conn.close()

print("✅ Data successfully loaded into PostgreSQL.")
