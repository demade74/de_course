import logging
import os
import psycopg2
from airflow.models import BaseOperator


class DataTransfer(BaseOperator):
    def __init__(self, config, pg_conn_str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.pg_conn_str = pg_conn_str

    def provide_data(self, fifo, context):
        pass

    def execute(self, context):
        copy_statement = """
        COPY {target_schema}.{target_table} ({columns}) FROM STDIN with
        DELIMITER '\t'
        CSV
        ESCAPE '\\'
        NULL '';
        """
        schema_name = "{table}".format(**self.config).split(".")
        self.config.update(
            target_schema=schema_name[0],
            target_table=schema_name[1],
        )
        with psycopg2.connect(self.pg_conn_str) as conn, conn.cursor() as cursor:
            cursor.execute(
                """
            select column_name
              from information_schema.columns
             where table_schema = '{target_schema}'
               and table_name = '{target_table}';
            """.format(**self.config)
            )
            result = cursor.fetchall()
            self.log.info(result)
            columns = ", ".join('"{}"'.format(row[0]) for row in result)
            self.config.update(columns=columns)

            with open('transfer.csv', 'w', encoding='utf-8') as csv_file:
                self.provide_data(csv_file, context)

            self.log.info("writing done")
            self.log.info(self.config)
            self.log.info(columns)
            self.log.info(copy_statement.format(**self.config))

            with open('transfer.csv', 'r', encoding='utf-8') as f:
                cursor.copy_expert(copy_statement.format(**self.config), f)
