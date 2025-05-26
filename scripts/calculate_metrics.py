# scripts/calculate_metrics.py

import psycopg2
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=os.getenv("PG_HOST"),
    port=os.getenv("PG_PORT"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    database=os.getenv("PG_DATABASE")
)

# Fetch data
query = "SELECT * FROM properties"
df = pd.read_sql(query, conn)

# ---- Metric 1: Price per Sqft ----
df["price_per_sqft"] = df["price"] / df["area"]
df["price_per_sqft"] = df["price_per_sqft"].round(2)

# ---- Metric 2: Average Price by ZIP ----
zip_stats = df.groupby("zipcode").agg(
    total_listings=("zpid", "count"),
    avg_price=("price", "mean"),
    avg_price_per_sqft=("price_per_sqft", "mean")
).round(2).reset_index()

# ---- Metric 3: Simulated ROI ----
# Assume: rent = 0.8% of price monthly, expenses = 30% of rent
df["monthly_rent"] = df["price"] * 0.008
df["monthly_expense"] = df["monthly_rent"] * 0.3
df["monthly_net_income"] = df["monthly_rent"] - df["monthly_expense"]
df["annual_net_income"] = df["monthly_net_income"] * 12
df["simulated_roi_%"] = (df["annual_net_income"] / df["price"]) * 100
df["simulated_roi_%"] = df["simulated_roi_%"].round(2)

# ---- Export Results ----
os.makedirs("outputs", exist_ok=True)
df.to_csv("outputs/enriched_properties.csv", index=False)
zip_stats.to_csv("outputs/zip_summary.csv", index=False)

print("✅ Metrics calculated and saved to outputs/")
