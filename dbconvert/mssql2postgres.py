# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 19:09:03 2018

@author: 1
"""
import logging
import traceback
from itertools import chain

from dbconvert.create_postgresql_ddl import createPostgresqlDDL
from dbconvert.read_mssql_metadata import createSchemaFromMSSQL


# module_logger = logging.getLogger("dbconvert.mssql2postgres")

MSSQL_UNSORTABLE_TYPES = ["BLOB", "MEMO"]

def mssql2postgres(schema_name, mssql_connect, postgres_connect, chunk_size):
    logger = logging.getLogger("dbconvert.mssql2postgres.mssql2postgres")

    schema = createSchemaFromMSSQL(schema_name, mssql_connect)

    postgresDDL = createPostgresqlDDL(schema)

    pg_cursor = postgres_connect.cursor()
    ms_cursor = mssql_connect.cursor()

    pg_cursor.execute(postgresDDL)
    logger.info("Start migration from SQL Server to PostgreSQL")

    row_count = 0

    for table in schema.tables:
        logger.debug("Processing table %s" % table.name)
        table_row_count = 0
        fields = ",".join(map(lambda field: '"' + field.name + '"', table.fields))
        sort_fields = ", ".join(
            map(
                lambda field: '"' + field.name + '"',
                filter(
                    lambda field: field.domain.type not in MSSQL_UNSORTABLE_TYPES,
                    table.fields
                )
            )
        )
        offset = 0
        pg_cursor.execute('''
                ALTER TABLE "{schema_name}"."{table_name}"
                DISABLE TRIGGER ALL
                '''.format(schema_name=schema.name,
                           table_name=table.name))

        while True:
            ms_cursor.execute('''
            SELECT {fields}
              FROM "{schema_name}"."{table_name}"
              ORDER BY {sort_fields}
              OFFSET {offset} ROWS
              FETCH NEXT {size} ROWS ONLY;
            '''.format(fields=fields,
                       schema_name=schema.name,
                       table_name=table.name,
                       sort_fields = sort_fields,
                       offset=offset,
                       size=chunk_size))
            data = ms_cursor.fetchall()
            if not data:
                break
            # pg_cursor.executemany('''
            # INSERT INTO "{schema_name}"."{table_name}"({fields})
            #      VALUES ({statement_params})
            # '''.format(fields=fields,
            #            schema_name=schema.name,
            #            table_name=table.name,
            #            statement_params=", ".join(["%s"] * len(table.fields))
            #            ), tuple(data))
            transaction = "BEGIN TRANSACTION;"
            for row in data:
                transaction += '''
                INSERT INTO "{schema_name}"."{table_name}"({fields})
                     VALUES ({statement_params});
                '''.format(fields=fields,
                           schema_name=schema.name,
                           table_name=table.name,
                           statement_params=", ".join(["%s"] * len(table.fields))
                )
            transaction += "COMMIT;"

            l = list(map(lambda x: None if x is None or type(x) == bytes else str(x), chain(*data)))
            logger.debug("Transaction start")
            try:
                pg_cursor.execute(transaction, l)
                logger.debug("Transaction success, size = %d" % len(data))
            except Exception:
                logger.critical('Bad transaction:\n{}\ndata:\n{}'.format(transaction, data))
                raise
            table_row_count += len(data)
            offset += chunk_size

        pg_cursor.execute('''
        ALTER TABLE "{schema_name}"."{table_name}"
        ENABLE TRIGGER ALL
        '''.format(schema_name=schema.name,
                   table_name=table.name))
        logger.info("Table %s success, row count: %d" % (table.name, table_row_count))
        row_count += table_row_count

    logger.info("Migration complete, row count %d" % row_count)

    return postgresDDL, schema


