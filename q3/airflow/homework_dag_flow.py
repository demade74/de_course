import os
from urllib.request import urlretrieve
from datetime import datetime
from airflow.operators.bash import BashOperator
from airflow.providers.telegram.operators.telegram import TelegramOperator
from airflow.utils.task_group import TaskGroup
from airflow.providers.apache.hive.operators.hive import HiveOperator

from airflow.decorators import dag, task


default_args = {
    "owner": "airflow",
    "retries": 0,
    "email_on_failure": False,
    "email_on_retry": False,
    "depends_on_past": False,
}


@dag(schedule_interval=None, start_date=datetime(2021, 10, 10), default_args=default_args)
def titanic_flow():
    @task
    def download_titanic_dataset(**kwargs):
        url = 'https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv'
        filepath, headers = urlretrieve(
            url=url,
            filename=os.path.join(os.path.expanduser('~'), f"titanic-{kwargs['ts_nodash']}.csv")
        )
        os.system(f'hdfs dfs -mkdir -p /datasets/titanic && hdfs dfs -put -f {filepath} /datasets/titanic && rm {filepath}')

        return f'/datasets/titanic/{os.path.basename(filepath)}'

    with TaskGroup("prepare_table") as prepare_table:
        drop_hive_table = HiveOperator(
            task_id='drop_hive_table',
            hql='DROP TABLE titanic;',
        )
        create_hive_table = HiveOperator(
            task_id='create_hive_table',
            hql='''CREATE EXTERNAL TABLE IF NOT EXISTS titanic ( Survived INT, Pclass INT,
            Name STRING, Sex STRING, Age INT, Sibsp INT, Parch INT, Fare DOUBLE)
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
            LOCATION '/datasets/titanic/'
            TBLPROPERTIES('skip.header.line.count'='1');''',
        )
        drop_hive_table >> create_hive_table

    show_avg_fare = BashOperator(
        task_id='show_avg_fare',
        bash_command="beeline -u jdbc:hive2://localhost:10000 -e 'SELECT Pclass, avg(Fare) FROM titanic GROUP BY Pclass;' > /home/hduser/avg_fare",
    )

    send_result_telegram = TelegramOperator(
        task_id='send_success_message_telegram',
        chat_id='597309171',
        text='''Pipeline {{ execution_date.int_timestamp }} is done. Execution date {{ ds }}. Next execution for {{ tomorrow_ds }}''',
    )

    download_titanic_dataset = download_titanic_dataset()
    download_titanic_dataset >> prepare_table >> show_avg_fare >> send_result_telegram


titanic_dag = titanic_flow()



