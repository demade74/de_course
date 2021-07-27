from psql_api import DBUtils

connection_string_source = "host='localhost' port=5433 dbname='source' user='root' password='postgres'"
connection_string_target = "host='localhost' port=5434 dbname='target' user='root' password='postgres'"
db_source = DBUtils(connection_string_source)
db_target = DBUtils(connection_string_target)
# select tables of source database
db_source.execute_query("select * from pg_catalog.pg_tables where schemaname='public'")
source_tables = db_source.fetch(all_=True)
# dump tables to csv and copy to target db
for row in source_tables:
    table_name = row[1]
    db_source.dump_table(table_name)
    print(f'table {table_name} was dumped successfully')
    db_target.copy_table_to_db(table_name)
    print(f'table {table_name} was copied successfully')

db_source.close()
db_target.close()
