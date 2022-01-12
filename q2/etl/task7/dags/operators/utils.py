import psycopg2
import logging
from airflow.models import BaseOperator


class DataFlowBaseOperator(BaseOperator):
    def __init__(self, pg_meta_conn_str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pg_meta_conn_str = pg_meta_conn_str

    def write_etl_log(self, config):
        with psycopg2.connect(self.pg_meta_conn_str) as conn, conn.cursor() as cursor:
            query = """
            insert into log (
                   source_launch_id
                 , target_schema
                 , target_table
                 , target_launch_id
                 , row_count
                 , duration
                 , load_date
            )
            select '{launch_id}'
                ,  '{target_schema}'
                ,  '{target_table}'
                ,  '{job_id}'
                ,  '{row_count}'
                ,  '{duration}'
                ,  '{dt}'
            """
            self.log.info("query.format(**config)" + query.format(**config))
            cursor.execute(query.format(**config))
            logging.info('Log update: {target_table} : {job_id}'.format(**config))
            conn.commit()

    def write_etl_statistic(self, config):
        with psycopg2.connect(self.pg_meta_conn_str) as conn, conn.cursor() as cursor:
            query = '''
            insert into statistic (
                   table_name
                 , column_name
                 , cnt_nulls
                 , cnt_all
                 , launch_id
                 , load_date
            )          
            select '{table}' as table_name
                 , '{column}' as column_name
                 , '{cnt_nulls}' as cnt_nulls
                 , '{cnt_all}' as cnt_all
                 , '{launch_id}' as launch_id
                 , '{load_date}' as load_date
            '''
            cursor.execute(query.format(**config))
            conn.commit()

    def get_load_dates(self, config):
        with psycopg2.connect(self.pg_meta_conn_str) as conn, conn.cursor() as cursor:
            query = '''
            select array_agg(distinct load_date order by load_date)
                from log
                where target_table = '{target_table}'
                and target_schema = '{target_schema}'
                and source_launch_id = -1
            '''
            cursor.execute(query.format(**config))
            dates = cursor.fetchone()[0]
        if dates:
            return dates
        else:
            return []


class DataFlowCollectStatisticOperator(DataFlowBaseOperator):
    def __init__(self, config, pg_target_conn_str, pg_meta_conn_str, *args, **kwargs):
        super().__init__(pg_meta_conn_str, *args, **kwargs)
        self.pg_target_conn_str = pg_target_conn_str
        self.config = config

    def execute(self, context):

        self.log.info("DataFlowCollectStatisticOperator context:" + str(context))
        schema_name = "{table}".format(**self.config).split(".")
        self.config.update(
            schema=schema_name[0],
            table=schema_name[1],
        )

        query_table_columns = """
        select column_name
        from information_schema.columns
        where table_schema = '{schema}'
        and table_name = '{table}'
        and column_name not in ('launch_id', 'effective_dttm');
        """.format(**self.config)

        query_cnt_counts = """
        select count(*) from {table} where {column} is null
        union all
        select count(*) from {table} where {column} is not null
        """

        with psycopg2.connect(self.pg_target_conn_str) as conn, conn.cursor() as cursor:
            cursor.execute(query_table_columns)
            columns = cursor.fetchall()
            for column in columns:
                col = column[0]
                cursor.execute(query_cnt_counts.format(table=self.config.get('table'), column=col))
                cnt_result = cursor.fetchall()
                self.log.info('cnt_result = ' + str(cnt_result))
                self.config.update(
                    column=col,
                    cnt_nulls=cnt_result[0][0],
                    cnt_all=cnt_result[1][0],
                    load_date=context["task_instance"].execution_date,
                    launch_id=context["task_instance"].job_id,
                )
                self.write_etl_statistic(self.config)
