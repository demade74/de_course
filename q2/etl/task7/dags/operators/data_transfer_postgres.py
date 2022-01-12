import csv
import psycopg2
from operators.data_transfer import DataTransfer


class DataTransferPostgres(DataTransfer):
    def __init__(self, source_pg_conn_str, pg_meta_conn_str, query, *args, **kwargs):
        super().__init__(
            source_pg_conn_str=source_pg_conn_str,
            pg_meta_conn_str=pg_meta_conn_str,
            query=query,
            *args,
            **kwargs
        )
        self.source_pg_conn_str = source_pg_conn_str
        self.pg_meta_conn_str = pg_meta_conn_str
        self.query = query

    def provide_data(self, csv_file, context):
        with psycopg2.connect(self.source_pg_conn_str) as pg_conn, pg_conn.cursor() as cursor:
            self.log.info("Executing query: {}".format(self.query))
            cursor.execute(self.query)
            csv_writer = csv.writer(
                csv_file,
                delimiter="\t",
                quoting=csv.QUOTE_NONE,
                lineterminator="\n",
                escapechar='\\'
            )

            while True:
                rows = cursor.fetchmany(size=1000)
                if rows:
                    for row in rows:
                        _row = list(row)
                        _row.append(context["task_instance"].job_id)
                        csv_writer.writerow(_row)
                else:
                    break
