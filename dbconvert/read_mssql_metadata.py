# -*- coding: utf-8 -*-
"""
Created on Sat Dec  2 10:26:11 2017

@author: 1
"""
from itertools import groupby, chain

from dbconvert.rammodel.domain import Domain
from dbconvert.rammodel.table import Table
from dbconvert.rammodel.field import Field
from dbconvert.rammodel.index import Index, IndexItem
from dbconvert.rammodel.constraint import Constraint
from dbconvert.rammodel.schema import Schema


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
        date = "DATE",
        image = "BLOB",
        int = "INTEGER",
        money = "CURRENCY",
        nchar = "STRING", #???
        ntext = "MEMO", #???
        nvarchar = "STRING", # ???
        real = "FLOAT", # ???
        smallint = "SMALLINT", #???
        varbinary = "BLOB", 
        varchar = "STRING",
        sysname = "STRING"
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
#        tmp.id = tableId
        
        tmp.fields = list(_fieldGenerator(tableId, cursor))
        tmp.constraints = list(chain(_foreignKeyGenerator(tableId, cursor),
                                     _primaryAndUniqueKeyGenerator(tableId, cursor),
                                     _checkConstraintGenerator(tableId, cursor)))
        tmp.indexes = list(_indecesGenerator(tableId, cursor))
        yield tmp
        

def _fieldGenerator(tableId, cursor):
    cursor.execute("""
    SELECT COL.name
    	    ,TP.name AS type_name
          ,COL.max_length
          ,COL.precision
          ,COL.scale
          ,COL.is_nullable
    	    ,DF.definition AS default_value
    FROM sys.columns AS COL
    LEFT JOIN sys.default_constraints AS DF
    ON COL.default_object_id = DF.object_id
    LEFT JOIN sys.types AS TP
    ON COL.system_type_id = TP.system_type_id
    WHERE COL.object_id = {table_id}
      AND TP.name != 'sysname'
    """.format(table_id = tableId))
    for field in cursor.fetchall():
        name, type_name, max_length, precision, scale, is_nullable, default_value = field
        tmp = Field()
        errors = []
        if name is not None:
            tmp.name = name
        else:
            errors.append("No field name in table with id={}".format(tableId))

            
        # Хз как отличить системный тип от пользовательского,
        # поэтому так как в NORTHWND нет пользовательских типов
        # обрабатываю все как системные типы (через безымянные домены)
        # TODO: все сказанное выше надо исправить(когда нибудь)
        
        domain = Domain()
       
        if type_name is not None:
            domain.type = types[type_name]
        if max_length is not None:
            domain.char_length = str(max_length)
        if precision is not None:
            domain.precision = str(precision)
        if scale is not None:
            domain.scale = str(scale)
        if is_nullable == 0:
            domain.required = True
        if default_value is not None:
            domain.default = str(default_value)
        tmp.domain = domain
        
        if errors != []:
            raise ValueError("\n".join(errors))
        yield tmp
    

def _foreignKeyGenerator(tableId, cursor):
    cursor.execute("""
    SELECT FK.name
    	  ,COL.name AS items
    	  ,TBL.name AS reference
    	  ,FK.delete_referential_action
    	  ,FK.update_referential_action
    FROM sys.foreign_key_columns AS FKC
    LEFT JOIN sys.foreign_keys AS FK ON FKC.constraint_object_id = FK.object_id
    LEFT JOIN sys.objects AS OBJ
    ON FK.referenced_object_id = OBJ.object_id
    LEFT JOIN sys.columns AS COL
    ON FKC.parent_object_id = COL.object_id
    AND FKC.parent_column_id = COL.column_id
    LEFT JOIN sys.tables AS TBL
    ON FKC.referenced_object_id = TBL.object_id
    WHERE FKC.parent_object_id = {table_id}
    """.format(table_id = tableId))
    for fk in cursor.fetchall():
        name, items, reference, deleteAction, updateAction = fk
        tmp = Constraint()
        errors = []
        if name is not None:
            tmp.name = name
        if items is not None:
            tmp.items = items
        else:
            errors.append("Foreign key in table with id={} has not items".format(tableId))
        if reference is not None:
            tmp.reference = reference
        else:
            errors.append("Foreign key in table with id={} has not reference".format(tableId))
            
        if errors != []:
            raise ValueError("\n".join(errors))
        tmp.kind = "FOREIGN"
        yield tmp
        


def _primaryAndUniqueKeyGenerator(tableId, cursor):
    cursor.execute("""
    SELECT kc.name
    	  ,kc.type
    	  ,KCU.COLUMN_NAME as items
    FROM sys.tables AS t
    JOIN sys.key_constraints AS kc
    ON t.object_id = kc.parent_object_id
    JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS KCU
    ON KCU.CONSTRAINT_NAME = kc.name
    WHERE t.object_id = {table_id}
    """.format(table_id = tableId))
    
    for key, group in groupby(cursor.fetchall(), lambda x: (x[0], x[1])):
        constraint = Constraint()
        errors = []
        constraint.name, kind = key
        if kind is not None:
            if kind == "PK":
                constraint.kind = "PRIMARY"
            elif kind == "UQ":
                constraint.kind = "UNIQUE"
            else:
                errors.append("Key in table with id={} has unknown kind ({kind})".format(tableId, kind))
        else:
            errors.append("Key in table with id={} has not kind".format(tableId))
        constraint.items = list(map(lambda x: x[2], group))
        
        if errors != []:
            raise ValueError("\n".join(errors))
            
        yield constraint
        
    
    
    
    for name, kind, items in cursor.fetchall():
        tmp = Constraint()
        errors = []
        tmp.name = name
        if kind is not None:
            if kind == "PK":
                tmp.kind = "PRIMARY"
            elif kind == "UQ":
                tmp.kind = "UNIQUE"
        else:
            errors.append("Key in table with id={} has not kind".format(tableId))
        if items is not None:
            tmp.items = items
        else:
            errors.append("Key in table with id={} has not items".format(tableId))
        
        if errors != []:
            raise ValueError("\n".join(errors))
        
        yield tmp
        
def _checkConstraintGenerator(tableId, cursor):
    cursor.execute("""
    SELECT CC.name, CC.definition, COL.name
    FROM sys.check_constraints AS CC
    JOIN sys.columns AS COL
    ON CC.parent_column_id = COL.column_id
    AND CC.parent_object_id = COL.object_id
    WHERE parent_object_id = {table_id}
    """.format(table_id = tableId))
    for name, exp, item in cursor.fetchall():
        tmp = Constraint()
        tmp.name = name
        tmp.expression = exp.replace('[', '"').replace(']', '"').replace('getdate()', 'current_date')
        if item is not None:
            tmp.items = item
        else:
            raise ValueError("Check constraint in table with id={} has not items".format(tableId))
        tmp.kind = "CHECK"
        yield tmp

    
def _indecesGenerator(tableId, cursor):
    cursor.execute("""
    SELECT ind.name
          ,ind.type_desc
    	  ,ic.index_column_id
    	  ,col.name
    	  ,ic.is_descending_key
    FROM sys.indexes AS ind
    JOIN sys.index_columns ic
    ON ind.object_id = ic.object_id AND ind.index_id = ic.index_id
    JOIN sys.columns AS col
    ON ind.object_id = col.object_id AND ic.column_id = col.column_id
    WHERE ind.object_id = {table_id}
    """.format(table_id = tableId))
    for key, group in groupby(cursor.fetchall(), lambda x: (x[0], x[1])):
        tmp = Index()
        tmp.name, tmp.is_clustered = key
        for _, _, colPos, colName, colDesc in group:
            tmpItem = IndexItem()
            tmpItem.name = colName
            tmpItem.position = colPos
            tmpItem.desc = colDesc
            tmp.fields.append(tmpItem)
        yield tmp
    
    
    