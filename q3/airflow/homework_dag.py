import os
import pandas as pd
from datetime import datetime
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "airflow",
    "start_date": datetime(2021, 10, 10),
    "retries": 0,
    "email_on_failure": False,
    "email_on_retry": False,
    "depends_on_past": False,
}

hadoop_home = '/home/hduser/hadoop/bin/'
hive_home = '/home/hduser/hive/bin/'
hive_db_name = 'test'


def get_path(file_name):
    return os.path.join(os.path.expanduser('~'), file_name)


def download_titanic_dataset():
    url = 'https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv'
    df = pd.read_csv(url)
    df.to_csv(get_path('titanic.csv'), encoding='utf-8')


def prepare_hive_table_script():
    with open(get_path('titanic.csv')) as f:
        header_columns = 'ID,' + f.readline().lstrip(',')  # read header
    header_columns = header_columns.lower().replace('/', '_').replace(' ', '_')  # remove slashes and spaces from header
    header_columns = header_columns.strip().split(',')  # split column names into list
    header_columns = [col_name + ' string,' for col_name in header_columns]  # column names with types to list
    header_columns[-1] = header_columns[-1].rstrip(',')  # remove last comma

    #  create table script
    script = "create table if not exists {db}.titanic (".format(db=hive_db_name)
    script += ''.join(header_columns)
    script += ") row format delimited fields terminated by ',' stored as textfile "
    script += 'tblproperties (\\"skip.header.line.count\\"=\\"1\\");'

    return script


def pivot_dataset():
    titanic_df = pd.read_csv(get_path('titanic.csv'))
    df = titanic_df.pivot_table(index=['Pclass'],
                                values='Fare',
                                aggfunc='mean').reset_index()
    df.to_csv(get_path('titanic_pivot.csv'))


with DAG(
    dag_id='titanic',
    default_args=default_args,
    schedule_interval=None,
) as dag:
    upload_command = "{hadoop_home}hdfs dfs -put -f {file_path} {hdfs_destination_path}".format(
        hadoop_home=hadoop_home,
        file_path=get_path('titanic.csv'),
        hdfs_destination_path="/datasets/titanic",
    )

    create_titanic_dataset = PythonOperator(
        task_id='download_titanic_dataset',
        python_callable=download_titanic_dataset,
    )

    create_dir = BashOperator(
        task_id='create_dataset_dir',
        bash_command="/home/hduser/hadoop/bin/hdfs dfs -mkdir -p /datasets/titanic"
    )

    upload_dataset_to_hdfs = BashOperator(
        task_id='upload_dataset_to_hdfs',
        bash_command=upload_command,
    )

    hive_init_db_and_upload_data_to_table = BashOperator(
        task_id='hive_init_db_and_upload_data_to_table',
        bash_command=(
            "rm -rf /home/hduser/metastore_db/ ; "
            "{hive_home}schematool -initSchema -dbType derby ; "
            "{hive_home}hive -e 'create database if not exists {db};' ; "
            "{hive_home}hive -e \"{table_script}\" ; "
            "{hive_home}hive -e \"load data inpath '/datasets/titanic/titanic.csv' into table {hive_db}.{hive_table};\" ; "
            "echo \"all actions done!\" ; "
            "{hive_home}hive -e 'select * from {hive_db}.{hive_table};' > /home/hduser/result"
        ).format(
            hive_home=hive_home,
            db=hive_db_name,
            table_script=prepare_hive_table_script(),
            local_file_path=get_path('titanic.csv'),
            hive_db=hive_db_name,
            hive_table='titanic'
        ),
    )

    pivot_titanic_dataset = PythonOperator(
        task_id='pivot_titanic_dataset',
        python_callable=pivot_dataset,
    )

    finish_work_message = BashOperator(
        task_id='finish_work_message',
        bash_command='echo "Pipeline finished! Execution date is {{ ds }}"',
    )

    create_dir >> \
    create_titanic_dataset >> \
    upload_dataset_to_hdfs >> \
    hive_init_db_and_upload_data_to_table >> \
    pivot_titanic_dataset >> \
    finish_work_message
