import psycopg2
import pyodbc

from dbconvert.mssql2postgres import mssql2postgres



pg_connect = psycopg2.connect("dbname='{dbname}' user='{user}' host='{host}' password='{pwd}'".format(
            dbname = "Test",
            user = "postgres",
            host = "localhost",
            pwd = "3korif8245ef"
        ))

ms_conenct = pyodbc.connect("DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}".format(
        driver   = "ODBC Driver 11 for SQL Server",
        #driver   = "SQL Server",
        server   = "localhost",
        username = "sa",
        password = "3korif8245ef",
        database = "NORTHWND"
        ))

schemaName = "dbo"
cursor = pg_connect.cursor()
cursor.execute('DROP SCHEMA IF EXISTS "{}" CASCADE'.format(schemaName))
ddl = mssql2postgres(schemaName, ms_conenct, pg_connect)