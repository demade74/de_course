import psycopg2

pg_conn_str = "host='localhost' port=5434 dbname='target' user='root' password='postgres'"

log_table_query = """
create table log (
       source_launch_id    int
     , target_schema       text
     , target_table        text  
     , target_launch_id    int
     , processed_dttm      timestamp default now()
     , row_count           int
     , duration            interval
     , load_date           date
     , effective_dttm      timestamp default now()
)
"""

statistic_table_query = """
create table statistic (
       launch_id      int
     , table_name     text
     , column_name    text
     , cnt_nulls      int
     , cnt_all        int
     , load_date      date
     , effective_dttm      timestamp default now()
)
"""

with psycopg2.connect(pg_conn_str) as conn, conn.cursor() as cursor:
    for query in [log_table_query, statistic_table_query]:
        cursor.execute(query)
        print(f'query executed')
