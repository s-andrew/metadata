# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 10:20:50 2017

@author: 1
"""
import itertools

simpleTypes = dict(
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



def getPrimaryKey(schemaName, tableName, constraint):
    return """ALTER TABLE \"{schema_name}\".\"{table_name}\"
    ADD {name} PRIMARY KEY (\"{items}\")""".format(
            schema_name = schemaName,
            table_name = tableName,
            name = "\"" + constraint.name + "\"" if constraint.name is not None else "",
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
    
constraints = dict(
        PRIMARY = getPrimaryKey,
        FOREIGN = getForeignKey
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
            raise ValueError("Domain with type {} haven't length or char_length".format(domain.type))
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
    



def createPostgresqlDDL(schema):
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

#    createSchemaDomainTablesIndecesStr = list(itertools.chain([createSchema(schema)],
#                                                                     domains,
#                                                                     tables,
#                                                                     indeces))
#    createPrimaryKeysStr = primaryKeys
#    createConstraintsStr = constraints
    
    createSchemaDomainTablesIndecesStr = ";\n".join(itertools.chain([createSchema(schema)],
                                                                     domains,
                                                                     tables,
                                                                     indeces)) + ";\n"
    createPrimaryKeysStr = ";\n".join(primaryKeys) + ";\n"
    createConstraintsStr = ";\n".join(constraints) + ";\n"
    
    return (createSchemaDomainTablesIndecesStr,
            createPrimaryKeysStr,
            createConstraintsStr)
    

def createSchema(schema):
    return "CREATE SCHEMA \"{name}\"".format(name = schema.name)


def createDomain(schemaName, domain):
    return """CREATE DOMAIN \"{schema_name}\".\"{domain_name}\" AS {type_}""".format(
            schema_name = schemaName,
            domain_name = domain.name,
            type_ = getType(domain)
            )


def createTable(schemaName, table):
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
    return "\"{name}\" \"{schema_name}\".\"{type_}\"".format(
            name = field.name,
            schema_name = schemaName,
            type_ = field.domain
            )


def createIndex(schemaName, tableName, index):
    return """CREATE {unique} INDEX{name} ON \"{schema_name}\".\"{tableName}\" (\"{field}\")""".format(\
            unique = "UNIQUE" if index.uniqueness else "",
            schema_name = schemaName,
            name = "\"" + index.name + "\"" if index.name is not None else "",
            tableName = tableName,
            field = index.fields[0]
            )
    

def createConstraint(schemaName, tableName, constraint):
    return constraints[constraint.kind](schemaName, tableName, constraint)
