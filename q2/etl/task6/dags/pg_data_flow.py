from airflow import DAG
from operators.data_transfer_postgres import DataTransferPostgres
from datetime import datetime


DEFAULT_ARGS = {
    "owner": "airflow",
    "start_date": datetime(2021, 7, 29),
    "retries": 1,
    "email_on_failure": False,
    "email_on_retry": False,
    "depends_on_past": True,
}

with DAG(
    dag_id="pg-data-flow",
    default_args=DEFAULT_ARGS,
    schedule_interval="@daily",
    max_active_runs=1,
    tags=['data-flow'],
) as dag:
    source_pg_conn_str = "host='source_db' port=5432 dbname='source' user='root' password='postgres'"
    pg_conn_str = "host='target_db' port=5432 dbname='target' user='root' password='postgres'"
    source_tables = [
        'customer',
        'lineitem',
        'nation',
        'orders',
        'part',
        'partsupp',
        'region',
        'supplier',
    ]

    tasks = {
        table: DataTransferPostgres(
            task_id=table,
            config={'table': 'public.{table}'.format(table=table)},
            query='select * from {table}'.format(table=table),
            source_pg_conn_str=source_pg_conn_str,
            pg_conn_str=pg_conn_str,
        )
        for table in source_tables
    }

    tasks_list = list(tasks.values())
    for idx, task in enumerate(tasks_list):
        if idx == len(tasks.values()) - 1:
            break
        tasks_list[idx] >> tasks_list[idx + 1]
