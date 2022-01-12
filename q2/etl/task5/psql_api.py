import psycopg2


class DBUtils:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = psycopg2.connect(self.connection_string)
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def execute_query(self, query):
        self.cursor.execute(query)

    def fetch(self, all_=False):
        if all_:
            return self.cursor.fetchall()
        return self.cursor.fetchone()

    def dump_table(self, table_name):
        query = f"COPY {table_name } TO STDOUT WITH DELIMITER ',' CSV HEADER;"
        with open(f'{table_name}.csv', 'w') as f:
            self.cursor.copy_expert(query, f)

    def copy_table_to_db(self, table_name):
        query = f"COPY {table_name} FROM STDIN WITH DELIMITER ',' CSV HEADER;"
        with open(f'{table_name}.csv', 'r') as f:
            self.cursor.copy_expert(query, f)
        self.connection.commit()

