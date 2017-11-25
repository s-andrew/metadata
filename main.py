import xml.dom.minidom as md
import sqlite3

import psycopg2

from dbconvert import (xml2ram,
                       ram2xml,
                       ram2sqlite,
                       createMSSQLDDL,
                       createPostgresqlDDL)

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


#==============================================================================
#  Создание соединения с базой при помощи sqlite3
#==============================================================================
#connect = sqlite3.connect("test_db.db")
connect = sqlite3.connect(":memory:")


#==============================================================================
#  Заполнение базы данными из объекта Schema
#==============================================================================
ram2sqlite(schema, connect)


#==============================================================================
#  Закрытие соединения с базой
#==============================================================================
connect.close()
del connect


#==============================================================================
#  Создания DDL для PostgreSQL
#==============================================================================
postgresqlDDL = createPostgresqlDDL(schema)

connect = psycopg2.connect("dbname='{dbname}' user='{user}' host='{host}' password='{pwd}'".format(
            dbname = "Test",
            user = "postgres",
            host = "localhost",
            pwd = "3korif8245ef"
        ))

cursor = connect.cursor()
#cursor.execute(postgresqlDDL[0])
#connect.commit()
#cursor.execute(postgresqlDDL[1])            
#connect.commit()
#connect.close()

for query in postgresqlDDL[0]:
    cursor.execute(query)
    connect.commit()
for query in postgresqlDDL[1]:
    cursor.execute(query)
    connect.commit()
connect.close()
    
