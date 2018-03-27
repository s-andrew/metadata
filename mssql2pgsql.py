import sys
import logging

import psycopg2
import pyodbc

import dbconvert.mssql2postgres as ms2pg

#if len(sys.argv) < 11:
#    print("Bad argument\n\nArgument example:\npython mssql2pgsql.py <pg_db_name> <pg_username> <pg_host> <pg_password> <ms_driver> <ms_host> <ms_username> <ms_password> <ms_db_name> <ms_schema_name>\n")
#    sys.exit(1)
#pg_connect_params = dict(
#dbname = sys.argv[1],
#user = sys.argv[2],
#host = sys.argv[3],
#pwd = sys.argv[4]     
#)
#ms_connect_params = dict(
#driver   = sys.argv[5],
#server   = sys.argv[6],
#username = sys.argv[7],
#password = sys.argv[8],
#database = sys.argv[9]
#)
#schema_name = sys.argv[10]
 
    
pg_connect_params = dict(
dbname = "Test",
user = "postgres",
host = "localhost",
pwd = "3korif8245ef"     
)
ms_connect_params = dict(
driver   = "ODBC Driver 11 for SQL Server",
#driver   = "SQL Server",
server   = "localhost",
username = "sa",
password = "3korif8245ef",
database = "NORTHWND"
)
schema_name = "dbo"



logging.basicConfig(filename="mssql2pgsql.log", level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

logging.info("Start")
pg_connect = psycopg2.connect("dbname='{dbname}' user='{user}' host='{host}' password='{pwd}'".format_map(pg_connect_params))
logging.info("Connect to postgres")
ms_conenct = pyodbc.connect("DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}".format_map(ms_connect_params))
logging.info("Connect to SQL server")



cursor = pg_connect.cursor()
cursor.execute('DROP SCHEMA IF EXISTS "{}" CASCADE'.format(schema_name))
ddl = ms2pg.mssql2postgres(schema_name, ms_conenct, pg_connect, 50)










































