from airflow import DAG
#from airflow.sensors.external_task import ExternalTaskSensor
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from operators.utils import DataFlowCollectStatisticOperator
from datetime import datetime

DEFAULT_ARGS = {
    "owner": "airflow",
    "start_date": datetime(2021, 8, 4),
    "retries": 1,
    "email_on_failure": False,
    "email_on_retry": False,
    "depends_on_past": False,
}

with DAG(
    dag_id="collect_statistic",
    default_args=DEFAULT_ARGS,
    schedule_interval="@daily",
    max_active_runs=1,
    tags=['collect_stats'],
) as dag:
    source_pg_conn_str = "host='source_db' port=5432 dbname='source' user='root' password='postgres'"
    pg_conn_str = "host='target_db' port=5432 dbname='target' user='root' password='postgres'"
    target_tables = [
        'customer',
        'lineitem',
        'nation',
        'orders',
        'part',
        'partsupp',
        'region',
        'supplier',
    ]
    tasks_list = list()

    for table in target_tables:
        tasks_list.append(
            ExternalTaskSensor(
                task_id=f'waiting_for_loading_{table}',
                external_dag_id='pg-data-flow-with-log',
                external_task_id=table,
                allowed_states=['success']
            )
        )
        tasks_list.append(
            DataFlowCollectStatisticOperator(
                task_id=f'collect_stats_{table}',
                config={'table': 'public.{table}'.format(table=table)},
                # query='select * from {table}'.format(table=table),
                pg_target_conn_str=pg_conn_str,
                pg_meta_conn_str=pg_conn_str
            )
        )

    for idx, task in enumerate(tasks_list):
        if idx == len(tasks_list) - 1:
            break
        tasks_list[idx] >> tasks_list[idx + 1]
