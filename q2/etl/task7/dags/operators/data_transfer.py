import time
import psycopg2
import datetime
from utils import DataFlowBaseOperator


class DataTransfer(DataFlowBaseOperator):
    def __init__(self, config, pg_conn_str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.pg_conn_str = pg_conn_str

    def provide_data(self, fifo, context):
        pass

    def execute(self, context):
        copy_statement = """
        COPY {target_schema}.{target_table} ({columns}, "launch_id") FROM STDIN with
        DELIMITER '\t'
        CSV
        ESCAPE '\\'
        NULL '';
        """
        schema_name = "{table}".format(**self.config).split(".")
        self.config.update(
            target_schema=schema_name[0],
            target_table=schema_name[1],
            job_id=context['task_instance'].job_id,
            dt=context["task_instance"].execution_date,
        )
        with psycopg2.connect(self.pg_conn_str) as conn, conn.cursor() as cursor:
            start_time = time.time()
            cursor.execute(
                """
            select column_name
              from information_schema.columns
             where table_schema = '{target_schema}'
               and table_name = '{target_table}'
               and column_name not in ('launch_id', 'effective_dttm');
            """.format(**self.config)
            )
            result = cursor.fetchall()
            self.log.info(result)
            columns = ", ".join('"{}"'.format(row[0]) for row in result)
            self.config.update(columns=columns)

            with open('transfer.csv', 'w', encoding='utf-8') as csv_file:
                self.provide_data(csv_file, context)
            self.log.info("writing done")
            with open('transfer.csv', 'r', encoding='utf-8') as f:
                cursor.copy_expert(copy_statement.format(**self.config), f)

            self.config.update(
                launch_id=-1,
                duration=datetime.timedelta(seconds=time.time() - start_time),
                row_count=cursor.rowcount,
            )
            self.write_etl_log(self.config)
