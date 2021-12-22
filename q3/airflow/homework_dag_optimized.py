from datetime import datetime
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.telegram.operators.telegram import TelegramOperator
from airflow.utils.task_group import TaskGroup
from airflow.providers.apache.hive.operators.hive import HiveOperator
#from airflow.providers.apache.hdfs.hooks.webhdfs import WebHDFSHook


default_args = {
    "owner": "airflow",
    "start_date": datetime(2021, 10, 10),
    "retries": 0,
    "email_on_failure": False,
    "email_on_retry": False,
    "depends_on_past": False,
}


# def upload_file_to_hdfs(source, destination, overwrite):
#     with WebHDFSHook() as hook:
#         hook.load_file(source, destination, overwrite)


with DAG(
    dag_id='titanic',
    default_args=default_args,
    schedule_interval=None,
) as dag:
    create_titanic_dataset = BashOperator(
        task_id='download_titanic_dataset',
        bash_command='''TITANIC_FILE="titanic-{{ execution_date.int_timestamp }}.csv" && \
        wget -q https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv -O $TITANIC_FILE && \
        hdfs dfs -mkdir -p /datasets/titanic && \
        hdfs dfs -put -f $TITANIC_FILE /datasets/titanic && \
        rm $TITANIC_FILE && \
        echo "/datasets/titanic/$TITANIC_FILE" ''',
    )

    with TaskGroup("prepare_table") as prepare_table:
        drop_hive_table = HiveOperator(
            task_id='drop_hive_table',
            hql='DROP TABLE titanic;',
        )
        create_hive_table = HiveOperator(
            task_id='create_hive_table',
            hql='''CREATE TABLE IF NOT EXISTS titanic ( Survived INT, Pclass INT,
            Name STRING, Sex STRING, Age INT, Sibsp INT, Parch INT, Fare DOUBLE)
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
            TBLPROPERTIES('skip.header.line.count'='1');''',
        )
        drop_hive_table >> create_hive_table

    load_titanic_hive = HiveOperator(
        task_id='load_data_to_hive',
        hql='''LOAD DATA INPATH '{{ task_instance.xcom_pull(task_ids='download_titanic_dataset', key='return_value') }}'
        INTO TABLE titanic;''',
    )

    show_avg_fare = BashOperator(
        task_id='show_avg_fare',
        bash_command="beeline -u jdbc:hive2://localhost:10000 -e 'SELECT Pclass, avg(Fare) FROM titanic GROUP BY Pclass;' > /home/hduser/avg_fare",
    )

    # hdfs_upload_avg_fare = PythonOperator(
    #     task_id='hdfs_upload_avg_fare',
    #     python_callable=upload_file_to_hdfs,
    #     op_args=['/home/hduser/avg_fare', '/datasets/titanic', True]
    # )

    send_result_telegram = TelegramOperator(
        task_id='send_success_message_telegram',
        chat_id='597309171',
        text='''Pipeline {{ execution_date.int_timestamp }} is done''',
    )

    create_titanic_dataset >> prepare_table >> load_titanic_hive >> show_avg_fare >> send_result_telegram
