import os
import sys
import requests
import psycopg2
from psycopg2.extras import execute_values



API_KEY = os.environ.get("API_KEY")
DB_CONN = os.environ.get("AIRFLOW__DATABASE__SQL_ALCHEMY_CONN")
STOCK_SYMBOL = "IBM"

# API key check
if not API_KEY or API_KEY.strip().lower() == "your_api_key_here":
    print("Error:A valid API_KEY must be set in the environment or .env file.")
    sys.exit(1)

def fetch_data():
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK_SYMBOL}&apikey={API_KEY}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json().get("Time Series (Daily)", {})
        if not data:
            print("No data returned from API. Check API key and limits.")
        return [(STOCK_SYMBOL,date, values['1. open'], values['4. close'])
                for date, values in data.items()]
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def update_db(records):
    if not records:
        print("No records to insert into the database.")
        return
    try:
        conn = psycopg2.connect(DB_CONN)
        cur = conn.cursor()
        execute_values(cur,
            "INSERT INTO stock_data (stock_symbol,date, open, close) VALUES %s ON CONFLICT (date) DO NOTHING",
            records)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB update error: {e}")

if __name__ == "__main__":
    data = fetch_data()
    update_db(data)
