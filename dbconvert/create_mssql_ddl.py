# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 12:40:04 2017

@author: 1
"""

import itertools

simpleTypes = dict(
        BOOLEAN = "bit",
        BYTE = "tinyint",
        SMALLINT = "smallint",
        WORD = "smallint",
        LARGEINT = "bigint",
        DATE = "date",
        TIME = "time",
        )
precisionAndScaleTypes = dict(
        FLOAT = "numeric",
        )
lengthTypes = dict(
        BLOB = "varbinary",
        STRING = "varchar",
        CODE = "varchar",
        MEMO = "nvarchar",   
        )

def getType(domain):
    if domain.type in simpleTypes:
        return simpleTypes[domain.type]
    if domain.type in lengthTypes:
        if domain.length is not None:
            length = domain.length
        elif domain.char_length is not None:
            length = domain.char_length
        else:
            length = "MAX"
#            raise ValueError("Domain with type {} haven't length or char_length".format(domain.type))
        return "{t}({n})".format(
                t = lengthTypes[domain.type],
                n = length)
    if domain.type in precisionAndScaleTypes:
        if domain.precision is not None:
            params = domain.precision
            if domain.scale is not None:
                params += ", " + domain.scale
        return "{t}{p}".format(
                t = precisionAndScaleTypes[domain.type],
                p = "(" + params + ")" if params is not None else "")
        
        
def getPrimaryKey(schemaName, tableName, constraint):
    return """ALTER TABLE [{schema_name}].[{table_name}]
    ADD {name} PRIMARY KEY ([{items}])""".format(
            schema_name = schemaName,
            table_name = tableName,
            name = "\"" + constraint.name + "\"" if constraint.name is not None else "",
            items = constraint.items
            )

def getForeignKey(schemaName, tableName, constraint):
    return """ALTER TABLE [{schema_name}].[{table_name}]
    ADD {name} FOREIGN KEY ([{items}])
    REFERENCES [{schema_name}].[{reference}]""".format(
            schema_name = schemaName,
            table_name = tableName,
            name = "CONSTRAINT [" + constraint.name + "]" if constraint.name is not None else "",
            items = constraint.items,
            reference = constraint.reference
            )
    
constraints = dict(
        PRIMARY = getPrimaryKey,
        FOREIGN = getForeignKey
        )



def createMSSQLDDL(schema):
    """
    Create DDL for Microsoft SQL Server
    RAM model -> MSSQL DDL
    Args:
        schema: object schema
    Return:
        tuple of three elements (str, str, str):
            0) DDL for creating schema
            1) DDL for creating domains, tables and indeces
            2) DDL for creating primary keys
            3) DDL for creating other constraints DDL for creating other constraints
    """
    domains = []
    tables = []
    indeces = []
    primaryKeys = []
    constraints = []
    for domain in schema.domains:
        domains.append(createDomain(schema.name, domain))
        
    for table in schema.tables:
        table_, indeces_, primaryKeys_, constraints_ = createTable(schema.name, table)
        tables.append(table_)
        indeces.extend(indeces_)
        primaryKeys.extend(primaryKeys_)
        constraints.extend(constraints_)
    
    createDomainStr = ";\n".join(domains) + ";\n"
    createTablesStr = ";\n".join(tables) + ";\n"
    createIndecesStr = ";\n".join(indeces) + ";\n"
    createPrimaryKeysStr = ";\n".join(primaryKeys) + ";\n"
    createConstraintsStr = ";\n".join(constraints) + ";\n"
    
    return (createSchema(schema),
            createDomainStr,
            createTablesStr,
            createIndecesStr,
            createPrimaryKeysStr,
            createConstraintsStr)
    


def createSchema(schema):
    return "CREATE SCHEMA [{name}]".format(name = schema.name)


def createDomain(schemaName, domain):
    return """CREATE TYPE [{schema_name}].[{domain_name}]
    FROM {type_name}""".format(
            schema_name = schemaName,
            domain_name = domain.name,
            type_name = getType(domain)
            )
#    return """
#    DROP TYPE [{schema_name}].[{domain_name}]""".format(
#            schema_name = schemaName,
#            domain_name = domain.name
#            )


def createTable(schemaName, table):
    """
    Create DDL for table
    Args:
        schemaName: str
        domain: object Domain
    Return:
        tuple of four elements (str, list<str>, list<str>, list<str>):
            0) DDL for creating table
            1) list of DDL for creating table indces
            2) list of DDL for creating table primary keys
            3) list of DDL for creating table other constraints
    """
    fields = ",\n".join(map(lambda f: createField(schemaName, f), table.fields))
    tableCreateStr =  """CREATE TABLE [{schema_name}].[{table_name}](
    {fields}
    )
    """.format(
            schema_name = schemaName,
            table_name = table.name,
            fields = fields
            )
#    tableCreateStr =  """
#    DROP TABLE [{schema_name}].[{table_name}]""".format(
#            schema_name = schemaName,
#            table_name = table.name
#            )
    indeces = map(lambda i: createIndex(schemaName, table.name, i), table.indexes)
    primaryKeys = map(lambda pk: createConstraint(schemaName, table.name, pk),
                      filter(lambda c: c.kind == "PRIMARY", table.constraints))
    constraints = map(lambda c : createConstraint(schemaName, table.name, c),
                      filter(lambda c: c.kind != "PRIMARY", table.constraints))
    return tableCreateStr, list(indeces), list(primaryKeys), list(constraints)
    

def createField(schemaName, field):
    """
    Create DDL for field
    Args:
        schemaName: str
        field: object Field
    Return: str
    """
    return "[{name}] [{schema_name}].[{type_}]".format(
            name = field.name,
            schema_name = schemaName,
            type_ = field.domain
            )


def createIndex(schemaName, tableName, index):
    """
    Create DDL for index
    Args:
        schemaName: str
        tableName: str
        field: object Index
    Return: str
    """
    return """CREATE {unique} INDEX {index_name} ON [{schema_name}].[{tableName}] ([{field}])""".format(
            unique = "UNIQUE" if index.uniqueness else "",
            schema_name = schemaName,
            index_name = "[" + index.name + "]" if index.name is not None else "",
            tableName = tableName,
            field = index.fields[0]
            )
    
    
    
def createConstraint(schemaName, tableName, constraint):
    """
    Create DDL for constraint
    Args:
        schemaName: str
        tableName: str
        constraint: object Constraint
    Return: str
    """
    return constraints[constraint.kind](schemaName, tableName, constraint)