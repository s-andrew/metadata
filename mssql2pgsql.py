import sys
import logging
import time

import psycopg2
import pyodbc

import dbconvert.mssql2postgres as ms2pg
import dbconvert.ram2xml as rx

if len(sys.argv) < 12:
   print("Bad argument\n\nArgument example:\npython mssql2pgsql.py <pg_db_name> <pg_username> <pg_host> <pg_password> <ms_driver> <ms_host> <ms_username> <ms_password> <ms_db_name> <ms_schema_name> <chunk_size>\n")
   sys.exit(1)
pg_connect_params = dict(
dbname = sys.argv[1],
user = sys.argv[2],
host = sys.argv[3],
pwd = sys.argv[4]
)
ms_connect_params = dict(
driver   = sys.argv[5],
server   = sys.argv[6],
username = sys.argv[7],
password = sys.argv[8],
database = sys.argv[9]
)
schema_name = sys.argv[10]
chunk_size = sys.argv[11]
 
    
# pg_connect_params = dict(
# dbname = "Test",
# user = "postgres",
# host = "localhost",
# pwd = ""
# )
# ms_connect_params = dict(
# driver   = "ODBC Driver 11 for SQL Server",
# #driver   = "SQL Server",
# server   = "localhost",
# username = "sa",
# password = "",
# database = "NORTHWND"
# )
# schema_name = "dbo"
# chunk_size = 50



logging.basicConfig(filename="mssql2pgsql.log", level=logging.DEBUG, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

logging.info("Start")
start_time = time.time()
pg_connect = psycopg2.connect("dbname='{dbname}' user='{user}' host='{host}' password='{pwd}'".format_map(pg_connect_params))
logging.info("Connect to postgres")
ms_conenct = pyodbc.connect("DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}".format_map(ms_connect_params))
logging.info("Connect to SQL server")



cursor = pg_connect.cursor()
cursor.execute('DROP SCHEMA IF EXISTS "{}" CASCADE'.format(schema_name))
# ddl, schema = \
ms2pg.mssql2postgres(schema_name, ms_conenct, pg_connect, chunk_size)

# with open("ddl.txt", "w") as ddl_file:
#     ddl_file.write(ddl)
#
# with open("schema.xml", "w") as xml_file:
#     xml = rx.ram2xml(schema)
#     xml_file.write(xml.toprettyxml(encoding="utf-8").decode("utf-8"))

runtime = time.time() - start_time
if runtime < 60:
    time_format = "%S s."
elif runtime < 3600:
    time_format = "%M m., %S s."
else:
    time_format = "%H h., %M m., %S s."
time_str = time.strftime(time_format, time.gmtime(runtime))
logging.info("Complete, runtime = %s" % time_str)











































