from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "stock_data_pipeline",
    default_args=default_args,
    description="Fetch and store stock data",
    schedule="@daily",
    start_date=datetime(2025, 8, 15),
    catchup=False,
) as dag:

    fetch_and_store = BashOperator(
        task_id="fetch_and_store",
        bash_command="python /opt/airflow/scripts/fetch_data.py"
    )

    fetch_and_store
