# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 10:26:11 2017

@author: 1
"""

from dbconvert.rammodel import Domain, Table, Field, Index, Constraint, Schema


#simpleTypes = dict(
#        BOOLEAN = "bit",
#        BYTE = "tinyint",
#        SMALLINT = "smallint",
#        WORD = "smallint",
#        LARGEINT = "bigint",
#        DATE = "date",
#        TIME = "time",
#        )
#precisionAndScaleTypes = dict(
#        FLOAT = "numeric",
#        )
#lengthTypes = dict(
#        BLOB = "varbinary",
#        STRING = "varchar",
#        CODE = "varchar",
#        MEMO = "nvarchar",   
#        )

types = dict(
        bit = "BOOLEAN",
        datetime = "DATETIME",
        image = "BLOB",
        int = "INTEGER",
        money = "",
        nchar = "STRING", #???
        ntext = "MEMO", #???
        nvarchar = "STRING", # ???
        real = "FLOAT", # ???
        smallint = "SMALLINT", #???
        varbinary = "BLOB", 
        varchar = "STRING"
        )





def createSchemaFromMSSQL(schemaName, connect):
    cursor = connect.cursor()
    schema = Schema()
    schema.name = schemaName
    schema.tables = list(_tableGenerator(schemaName, cursor))
    
    return schema


def _tableGenerator(schemaName, cursor):
    cursor.execute("""
    SELECT TBL.name, TBL.object_id
    FROM sys.tables AS TBL
    LEFT JOIN sys.schemas AS SCH ON TBL.schema_id = SCH.schema_id
    WHERE SCH.name = '{schema_name}'
    """.format(schema_name = schemaName))
    for tableName, tableId in cursor.fetchall():
        tmp = Table()
        tmp.name = tableName
        tmp.id = tableId
        
        tmp.fields = list(_fieldGenerator(tableId, cursor))
        yield tmp
        

def _fieldGenerator(tableId, cursor):
    cursor.execute("""
        SELECT COL.[name]
        	  ,TP.[name] AS type_name
              ,COL.[max_length]
              ,COL.[precision]
              ,COL.[scale]
              ,COL.[is_nullable]
        	  ,DF.[definition] AS default_value
          FROM [sys].[columns] AS COL
          LEFT JOIN [sys].[default_constraints] AS DF ON COL.default_object_id = DF.object_id
          LEFT JOIN [sys].[types] AS TP ON COL.system_type_id = TP.system_type_id
          WHERE COL.object_id = {table_id}
        """.format(table_id = tableId))
    for field in cursor.fetchall():
        name, type_name, max_length, precision, scale, is_nullable, default_value = field
        tmp = Field()
        errors = []
        if name is not None:
            tmp.name = name
        else:
            errors.append("No field name in table with id={}".format(tableId))
        if type_name is not None:
            tmp.type = type_name# types[type_name]
        else:
            errors.append("No type name in table with id={}".format(tableId))
        if max_length is not None:
            tmp.char_length = str(max_length)
        if precision is not None:
            tmp.precision = str(precision)
        if scale is not None:
            tmp.scale = str(scale)
        if is_nullable == 0:
            tmp.required = True
        if default_value is not None:
            tmp.default = str(default_value)
        
        if errors != []:
            raise ValueError("\n".join(errors))
        yield tmp
    
    