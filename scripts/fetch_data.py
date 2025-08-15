import os
import sys
import requests
import psycopg2
from psycopg2.extras import execute_values

API_KEY = os.environ.get("API_KEY")
DB_CONN = f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@{os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}/{os.environ.get('DB_NAME')}"
STOCK_SYMBOL = "IBM"  # you can change to a company of your choice

# Validate env
if not API_KEY or API_KEY.strip().lower() == "your_api_key_here":
    print("ERROR: A valid API_KEY must be set in the environment or .env file.")
    sys.exit(1)
if not DB_CONN:
    print("ERROR: DB_CONN is not set. Put it in your .env.")
    sys.exit(1)

def fetch_data():
    url = (
        "https://www.alphavantage.co/query"
        f"?function=TIME_SERIES_DAILY&symbol={STOCK_SYMBOL}"
        f"&outputsize=compact&apikey={API_KEY}"
    )
    try:
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        payload = r.json()

        # Explicit API error/rate-limit handling
        if "Error Message" in payload:
            print(f"API error: {payload['Error Message']}")
            return []
        if "Note" in payload:
            print(f"Rate limit/notice from API: {payload['Note']}")
            return []

        data = payload.get("Time Series (Daily)", {})
        if not data:
            print("No data returned from API.")
            return []

        rows = [(STOCK_SYMBOL,d, v["1. open"], v["4. close"]) for d, v in data.items()]
        rows.sort(key=lambda x: x[0])  # deterministic order
        print(f"Fetched {len(rows)} rows for {STOCK_SYMBOL}.")
        return rows
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
        # insert so reruns refresh existing rows
        query = """
        INSERT INTO stock_data (symbol,date, open, close)
        VALUES %s
        ON CONFLICT (symbol, date) DO UPDATE
        SET open = EXCLUDED.open,
            close = EXCLUDED.close
        """
        execute_values(cur, query, records)
        conn.commit()
        cur.close()
        conn.close()
        print(f"inserted {len(records)} rows into stock_data.")
    except Exception as e:
        print(f"DB update error: {e}")

if __name__ == "__main__":
    data = fetch_data()
    update_db(data)
