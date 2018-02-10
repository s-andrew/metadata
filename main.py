import xml.dom.minidom as md
import sqlite3

from dbconvert import (xml2ram,
                       ram2xml,
                       ram2sqlite,
                       sqlite2ram,
                       createPostgresqlDDL,
                       createSchemaFromMSSQL)
from dbconvert.rammodel import Domain

#TODO: ARGPARSE

#==============================================================================
#  Чтение XML при помощи minidom
#==============================================================================
xml = md.parse("tasks.xml")
#xml = md.parse("PRJAdm.xml")


#==============================================================================
#  Создание объекта Schema из XML
#==============================================================================
schema = xml2ram(xml)        
    

#==============================================================================
#  Создание XML из объекта Schema
#==============================================================================
resXML = ram2xml(schema)
#with open("result.xml", "w") as file:
#    file.write(resXML.toprettyxml(encoding="utf-8").decode("utf-8"))


#==============================================================================
#  Создание соединения с базой при помощи sqlite3
#  Заполнение базы данными из объекта Schema
#  Закрытие соединения с базой
#==============================================================================
#connect = sqlite3.connect("test_db1.db")
connect = sqlite3.connect(":memory:")
ram2sqlite(schema, connect)
connect.commit()

d = sqlite2ram(schema.name, connect)

connect.close()
del connect


#==============================================================================
#  Создания DDL для PostgreSQL
#==============================================================================
schema.name = "mssql"
postgresqlDDL = createPostgresqlDDL(schema)

import psycopg2
connect = psycopg2.connect("dbname='{dbname}' user='{user}' host='{host}' password='{pwd}'".format(
            dbname = "Test",
            user = "postgres",
            host = "localhost",
            pwd = "3korif8245ef"
        ))
#
#cursor = connect.cursor()
#cursor.execute(postgresqlDDL)
#connect.close()
#del connect

#==============================================================================
#  Создание DDL для Microsoft SQL Server
#==============================================================================
#mssqlDDL = createMSSQLDDL(schema)

import pyodbc
connect = pyodbc.connect("DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}".format(
        driver   = "ODBC Driver 11 for SQL Server",
        #driver   = "SQL Server",
        server   = "localhost",
        username = "sa",
        password = "3korif8245ef",
        database = "NORTHWND"
        ))

schemaName = "dbo"
#
#cursor = connect.cursor()
#cursor.execute("""
#    SELECT TBL.name, TBL.object_id
#    FROM sys.tables AS TBL
#    LEFT JOIN sys.schemas AS SCH ON TBL.schema_id = SCH.schema_id
#    WHERE SCH.name = '{schema_name}'
#    """.format(schema_name = schemaName))



schema = createSchemaFromMSSQL(schemaName, connect)
resXML = ram2xml(schema)
#s = resXML.toprettyxml()



with open("result.xml", "w") as file:
    file.write(resXML.toprettyxml())
        

connect.close()
del connect