import sys
import sqlite3

import psycopg2

from dbconvert.sqlite2ram import sqlite2ram
from dbconvert.create_postgresql_ddl import createPostgresqlDDL



if len(sys.argv) < 7:
    print("Bad argument\n\nArgument example:\npython dbd2pgsql.py <db_file_name> <schewma_name> <pg_dbname> <user> <host> <password>\n")
    sys.exit(1)
db_file_name = sys.argv[1]
schema_name = sys.argv[2]
connection_params = dict(
        dbname = sys.argv[3],
        user = sys.argv[4],
        host = sys.argv[5],
        pwd = sys.argv[6]        
        )
#db_file_name = "tasks.db"
#schema_name = "TASKS"
#connection_params = dict(
#       dbname = "Test",
#       user = "postgres",
#       host = "localhost",
#       pwd = ""
#       )



sqlite_connect = sqlite3.connect(db_file_name)
schema =  sqlite2ram(schema_name, sqlite_connect)
postgresqlDDL = createPostgresqlDDL(schema)
pg_connect = psycopg2.connect("dbname='{dbname}' user='{user}' host='{host}' password='{pwd}'".format_map(connection_params))
cursor = pg_connect.cursor()
cursor.execute(postgresqlDDL)
pg_connect.commit()
