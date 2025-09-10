# Stock Data Pipeline with Apache Airflow & PostgreSQL

A complete data pipeline that **fetches daily stock prices** from the Alpha Vantage API, stores them in a **PostgreSQL database**, and orchestrates the process with **Apache Airflow**.

---

## Features
- Fetch daily stock prices for a given ticker (default: `IBM`)
- Store data in PostgreSQL with upsert logic to avoid duplicates
- Automated scheduling using Apache Airflow
- Environment configuration via `.env` file
- Dockerized for easy setup and deployment

---

## Project Structure
```
stock_pipeline/
├── docker-compose.yml       # Services: Airflow, Postgres
├── .env                     # API keys and DB configuration
├── init.sql                 # Database table initialization
├── scripts/
│   └── fetch_data.py         # Fetches and inserts stock data
└── dags/
    └── stock_dag.py          # Airflow DAG to run the pipeline
```

---

## Prerequisites
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)
- Alpha Vantage API key (Get one for free: [Alpha Vantage](https://www.alphavantage.co/support/#api-key))

---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Zaid-76/stock-market-etl-pipeline.git
cd stock-market-etl-pipeline
```

### 2. Configure Environment Variables
Edit `.env` and update:
```env
API_KEY=YOUR_ALPHA_VANTAGE_KEY
DB_USER=airflow
DB_PASSWORD=airflow
DB_NAME=stockdb
DB_HOST=postgres
DB_PORT=5432
```

### 3. Start the Services
```bash
docker-compose up -d
```
This starts:
- **PostgreSQL** on port `5432`
- **Airflow Web UI** on port `8080`

---

## Running the Pipeline

### Option 1: Automatic (via Airflow Scheduler)
1. Go to **http://localhost:8080**
2. Log in with:
   ```
   Username: admin
   Password: admin
   ```
3. Enable and trigger the `stock_data_pipeline` DAG.

### Option 2: Manual Run
Run the fetch script directly inside the Airflow container:
```bash
docker exec -it stock_pipeline-airflow-1 python /opt/airflow/scripts/fetch_data.py
```

---

## Database Schema
Created by `init.sql`:
```sql
CREATE TABLE IF NOT EXISTS stock_data (
    symbol TEXT NOT NULL,
    date   DATE NOT NULL,
    open   NUMERIC,
    close  NUMERIC,
    PRIMARY KEY (symbol, date)
);
```

---

## Troubleshooting

- **Invalid API Key**  
  Make sure your `.env` file has a valid `API_KEY`.

- **ON CONFLICT error**  
  Ensure `fetch_data.py` uses `ON CONFLICT (symbol, date)`.

- **Container Not Starting**  
  Run:
  ```bash
  docker-compose down -v
  docker-compose up --build
  ```

- **Psycopg2 Connection Error**  
  Use `postgresql://` instead of `postgresql+psycopg2://` in `fetch_data.py` when calling `psycopg2.connect()`.

---
