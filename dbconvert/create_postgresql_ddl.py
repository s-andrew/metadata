# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 10:20:50 2017

@author: 1
"""
import itertools

simpleTypes = dict(
        INTEGER = "int",
        BLOB = "bytea",
        BOOLEAN = "boolean",
        BYTE = "smallint",
        LARGEINT = "bigint",
        SMALLINT = "smallint",
        WORD = "smallint" ,
        DATE = "date",
        TIME = "time",
        MEMO = "text",
        )

precisionAndScaleTypes = dict(
        FLOAT = "numeric",
        )

lengthTypes = dict(
        STRING = "varchar",
        CODE = "varchar",
        )


def getType(domain):
    res = None
    if domain.type in simpleTypes:
        return simpleTypes[domain.type]
    if domain.type in lengthTypes:
        if domain.length is not None:
            length = domain.length
        elif domain.char_length is not None:
            length = domain.char_length
        else:
            raise ValueError("Domain with type {} haven't length or char_length".format(domain.type))
        return "{t}({n})".format(
                t = lengthTypes[domain.type],
                n = length)
    if domain.type in precisionAndScaleTypes:
        if domain.precision is not None:
            params = domain.precision
            if domain.scale is not None:
                params += ", " + domain.scale
        res = "{t}{p}".format(
                t = precisionAndScaleTypes[domain.type],
                p = "(" + params + ")" if params is not None else "")
    return res if res is not None else "text"
    

def getPrimaryKey(schemaName, tableName, constraint):
    return """ALTER TABLE \"{schema_name}\".\"{table_name}\"
    ADD PRIMARY KEY (\"{items}\")""".format(
            schema_name = schemaName,
            table_name = tableName,
#            name = "CONSTRAINT \"" + constraint.name + "\"" if constraint.name is not None else "",
            items = constraint.items
            )

def getForeignKey(schemaName, tableName, constraint):
    return """ALTER TABLE \"{schema_name}\".\"{table_name}\"
    ADD {name} FOREIGN KEY (\"{items}\")
    REFERENCES \"{schema_name}\".\"{reference}\"""".format(
            schema_name = schemaName,
            table_name = tableName,
            name = "CONSTRAINT \"" + constraint.name + "\"" if constraint.name is not None else "",
            items = constraint.items,
            reference = constraint.reference
            )
    
def getCheckConstraint(schemaName, tableName, constraint):
    return """ALTER TABLE \"{schema_name}\".\"{table_name}\"
    ADD {name} CHECK ({expression})""".format(
            schema_name = schemaName,
            table_name = tableName,
            name = "CONSTRAINT \"" + constraint.name + "\"" if constraint.name is not None else "",
            items = constraint.items,
            expression = constraint.reference
            )
    
def getUniqueConstraint(schemaName, tableName, constraint):
    return """ALTER TABLE \"{schema_name}\".\"{table_name}\"
    ADD {name} UNIQUE (\"{items}\")""".format(
            schema_name = schemaName,
            table_name = tableName,
            name = "CONSTRAINT \"" + constraint.name + "\"" if constraint.name is not None else "",
            items = constraint.items
            )
    
constraints = dict(
        PRIMARY = getPrimaryKey,
        FOREIGN = getForeignKey,
        CHECK = getCheckConstraint,
        UNIQUE = getUniqueConstraint
        )



def createPostgresqlDDL(schema):
    """
    Create DDL for PostgreSQL
    RAM model -> PostgreSQL DDL
    Args:
        schema: object schema
    Return:
        str with DDL of schema
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
    
    createSchemaDomainTablesIndecesStr = ";\n".join(itertools.chain(domains,
                                                                     tables,
                                                                     indeces)) + ";\n"
    createPrimaryKeysStr = ";\n".join(primaryKeys) + ";\n"
    createConstraintsStr = ";\n".join(constraints) + ";\n"
    
    return """\
BEGIN TRANSACTION;
SET CONSTRAINTS ALL DEFERRED;
""" +\
createSchema(schema) +\
createSchemaDomainTablesIndecesStr +\
createPrimaryKeysStr +\
createConstraintsStr +\
"COMMIT;"
    

def createSchema(schema):
    """
    Create DDL for schema
    Args:
        schema: object Schema
    Return: str
    """
    return "CREATE SCHEMA \"{name}\";\n".format(name = schema.name)


def createDomain(schemaName, domain):
    """
    Create DDL for domain
    Args:
        schemaName: str
        domain: object Domain
    Return: str
    """
    return """CREATE DOMAIN \"{schema_name}\".\"{domain_name}\" AS {type_name}""".format(
            schema_name = schemaName,
            domain_name = domain.name,
            type_name = getType(domain)
            )


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
    tableCreateStr = """CREATE TABLE \"{schema_name}\".\"{table_name}\"(\n{fields})""".format(
            schema_name = schemaName,
            table_name = table.name,
            fields = fields
            )
    indeces = map(lambda i: createIndex(schemaName, table.name, i), table.indexes)
    primaryKeys = map(lambda c: createConstraint(schemaName, table.name, c),
                      filter(lambda c: c.kind == "PRIMARY", table.constraints))
    constraints = map(lambda c: createConstraint(schemaName, table.name, c),
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
#    print(field.domain)
#    print(field.name, field.domain if isinstance(field.domain, str) else field.domain.type)
    return "\"{name}\" \"{schema_name}\".\"{type_}\"".format(
            name = field.name,
            schema_name = schemaName,
            type_ = field.domain if isinstance(field.domain, str) else getType(field.domain)
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
    return """CREATE {unique} INDEX{name} ON \"{schema_name}\".\"{tableName}\" (\"{field}\")""".format(
            unique = "UNIQUE" if index.uniqueness else "",
            schema_name = schemaName,
            name = "\"" + index.name + "\"" if index.name is not None else "",
            tableName = tableName,
            field = ", ".join(item.name for item in index.fields)
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
