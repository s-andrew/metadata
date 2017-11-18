# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 12:40:04 2017

@author: 1
"""


#types = dict(
#        BLOB = "image",         # Двоичные данные переменной длины, от 0 до 2^31 - 1 байт
#        BOOLEAN = "bit",        # Целочисленный тип, который принимает значения 0, 1 и NULL
#        BYTE = "tinyint",       # От 0 до 255, 1 байт
#        CODE = "[CODE]",
#        DATE = "Date",
#        FLOAT = "float",        # от -1.79E + 308 до -2.23E - 308, 0 и  от 2.23E - 308 до 1.79E + 308       4 или 8 байт
##        FLOAT = "real",         # от -3.40E + 38 до -1.18E - 38, 0 и от 1.18E - 38 до 3.40E + 38            4 байта
##        FLOAT = "decimal",      # decimal(p, s) p - количество десятичных разпядов(всех, и справа и слева), s - количество десятичных разрядов справа от запятой
#        LARGEINT = "bigint",    # От -2^63 до 2^63 - 1, 8 байт
#        MEMO = "ntext",         # Данные  переменной дляны в кодировке Юникод с максимальной длинной строки 2^30 - 1 байт
##        MEMO = "text",          # Данные переменной длины не в Юникоде в кодовой странице сервера и с максимальной длинной строки 2^31 - 1 байт.
#        SMALLINT = "smallint",  # От -2^15 до 2^15 - 1, 2 байта
#        STRING = "varchar",
#        TIME = "time",
#        WORD = "[WORD]"
#        )



def createMSSQLDDL(schema):
    result = ""
    result += createSchema(schema)
    
    for domain in schema.domains:
        result += createDomain(domain)
    
    for table in schema.tables:
        createTable(table)

    return result


def createSchema(schema):
    return "CREATE SCHEMA {name}".format(name = schema.name)


def createDomain(domain):
    precisionAndScale = ""
    if domain.precision is not None:
        precisionAndScale += str(domain.precision)
        if domain.scale is not None:
            precisionAndScale += ", " + str(domain.scale)
        precisionAndScale = "(" + precisionAndScale + ")"
    return """
    CREATE TYPE {domain_name}
    FROM [{type_}]
    {precision_and_scale}
    """.format(
            domain_name = domain.name,
            type_ = domain.type,
            precision_and_scale = precisionAndScale
            )


def createTable(table):
    fields = ""
    for field in table.fields:
        fields += createField(field)
    return """
    CREATE TABLE {table_name}(
    {fields}
    )
    """.format(
            table_name = table.name,
            fields = fields
            )
    

def createField(field):
    pass
    return "{name} {type_}".format(
                name = field.name,
                type_ = field.domain
            )


def createIndex(index):
    pass