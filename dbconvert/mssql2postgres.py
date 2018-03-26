# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 19:09:03 2018

@author: 1
"""
import json
from dbconvert.create_postgresql_ddl import createPostgresqlDDL
from dbconvert.read_mssql_metadata import createSchemaFromMSSQL


def mssql2postgres(schema_name, mssql_connect, postgres_connect):
    
    schema = createSchemaFromMSSQL(schema_name, mssql_connect)
    postgresDDL = createPostgresqlDDL(schema)
    
    pg_cursor = postgres_connect.cursor()
    ms_cursor = mssql_connect.cursor()

    pg_cursor.execute(postgresDDL)

    for table in schema.tables:
        fields = ",".join(map(lambda field: '"' + field.name + '"', table.fields))
        ms_cursor.execute('''
        SELECT {fields}
          FROM "{schema_name}"."{table_name}"
        '''.format(fields = fields,
                   schema_name = schema.name,
                   table_name = table.name))

        data = tuple(ms_cursor.fetchall())

        pg_cursor.execute('''
        ALTER TABLE "{schema_name}"."{table_name}"
        DISABLE TRIGGER ALL
        '''.format(schema_name = schema.name,
                   table_name = table.name))

        pg_cursor.executemany('''
        INSERT INTO "{schema_name}"."{table_name}"({fields})
             VALUES ({statement_params})
        '''.format(fields = fields,
                   schema_name = schema.name,
                   table_name = table.name,
                   statement_params = ", ".join(["%s"] * len(table.fields))
                   ), data)

        pg_cursor.execute('''
        ALTER TABLE "{schema_name}"."{table_name}"
        ENABLE TRIGGER ALL
        '''.format(schema_name = schema.name,
                   table_name = table.name))

    # return postgresDDL
            
            
        