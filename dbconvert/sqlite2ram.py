
from dbconvert.rammodel.domain import Domain
from dbconvert.rammodel.table import Table
from dbconvert.rammodel.field import Field
from dbconvert.rammodel.index import Index, IndexItem
from dbconvert.rammodel.constraint import Constraint
from dbconvert.rammodel.schema import Schema

def sqlite2ram(schemaName, connection):
    
    
    selectDomains = """
    SELECT DISTINCT
           dbd$domains.id
          ,dbd$domains.name
          ,dbd$domains.description
          ,dbd$data_types.type_id
          ,dbd$domains.length
          ,dbd$domains.char_length
          ,dbd$domains.precision
          ,dbd$domains.scale
          ,dbd$domains.width
          ,dbd$domains.align
          ,dbd$domains.show_null
          ,dbd$domains.show_lead_nulls
          ,dbd$domains.thousands_separator
          ,dbd$domains.summable
          ,dbd$domains.case_sensitive
    FROM dbd$fields as fd
    JOIN dbd$tables ON dbd$tables.id = fd.table_id
    JOIN dbd$schemas ON dbd$schemas.id = dbd$tables.schema_id
    JOIN dbd$domains ON dbd$domains.id = fd.domain_id
    JOIN dbd$data_types ON dbd$data_types.id = dbd$domains.data_type_id
    WHERE dbd$schemas.name = ?
    """    
    
    selectTables = """
    SELECT tb.id
          ,tb.name
          ,tb.description
          ,tb.can_add
          ,tb.can_edit
          ,tb.can_delete
          --,tb.temporal_mode
          --,tb.means
    FROM dbd$tables as tb
    JOIN dbd$schemas ON dbd$schemas.id = tb.schema_id
    WHERE dbd$schemas.name = ?;
    """
    
    selectFields = """ 
    SELECT fd.id
          ,fd.name
          ,fd.russian_short_name
          ,fd.description
          ,dbd$domains.name
          ,fd.can_input
          ,fd.can_edit
          ,fd.show_in_grid
          ,fd.show_in_details
          ,fd.is_mean
          ,fd.autocalculated
          ,fd.required
    FROM dbd$fields as fd
    JOIN dbd$tables ON dbd$tables.id = fd.table_id
    JOIN dbd$schemas ON dbd$schemas.id = dbd$tables.schema_id
    JOIN dbd$domains ON dbd$domains.id = fd.domain_id
    WHERE dbd$schemas.name = ?
      AND dbd$tables.name = ?;
    """
    
    selectConstraints = """
    SELECT  cs.id
           ,cs.name
           ,cs.constraint_type
           ,cs.reference
           ,cs.has_value_edit
           ,cs.cascading_delete
           ,cs.expression
    FROM dbd$constraints as cs
    JOIN dbd$tables ON dbd$tables.id = cs.table_id
    JOIN dbd$schemas ON dbd$schemas.id = dbd$tables.schema_id
    WHERE dbd$schemas.name = ?
      AND dbd$tables.id = ?
    """
    
    selectConstraintDetails = """
    SELECT dbd$fields.name
    FROM dbd$constraint_details as cd
    JOIN dbd$constraints ON dbd$constraints.id = cd.constraint_id
    JOIN dbd$fields ON dbd$fields.id = cd.field_id
    JOIN dbd$tables ON dbd$tables.id = dbd$constraints.table_id AND dbd$tables.id = dbd$fields.table_id
    JOIN dbd$schemas ON dbd$schemas.id = dbd$tables.schema_id
    WHERE dbd$schemas.name = ?
      AND dbd$tables.id = ?
      AND dbd$constraints.id = ?
    ORDER BY cd.position
    """
    
    selectIndices = """
    SELECT  ind.id
           ,ind.name
           ,ind.local
           ,ind.kind
      FROM dbd$indices AS ind
      JOIN dbd$tables ON ind.table_id = dbd$tables.id
      JOIN dbd$schemas ON dbd$tables.schema_id = dbd$schemas.id
      WHERE dbd$schemas.name = ?
        AND dbd$tables.name = ?
    """
    
    selectIndexDetails = """
    SELECT dbd$fields.name
          ,expression
          ,descend
    FROM dbd$index_details
    JOIN dbd$indices ON dbd$index_details.index_id = dbd$indices.id
    JOIN dbd$fields ON dbd$index_details.field_id = dbd$fields.id
    JOIN dbd$tables ON dbd$fields.table_id = dbd$tables.id
    JOIN dbd$schemas ON dbd$tables.schema_id = dbd$schemas.id
    WHERE dbd$schemas.name = ?
      AND dbd$tables.id = ?
      AND dbd$indices.id = ?
    ORDER BY dbd$index_details.index_id, dbd$index_details.position
    """
    
    cursor = connection.cursor()
    
    schema = Schema()
    schema.name = schemaName
    
    cursor.execute(selectDomains, (schemaName,))
    domainsId, schema.domains = zip(*map(domainMapper, cursor.fetchall()))

    cursor.execute(selectTables, (schemaName,))    
    for tableId, table in map(tableMapper, cursor.fetchall()):
        cursor.execute(selectFields, (schemaName, table.name))
        fieldsId, table.fields = zip(*map(fieldMapper, cursor.fetchall()))
        cursor.execute(selectConstraints, (schemaName, tableId))

        cursor.execute(selectConstraints, (schemaName, tableId))
        for constraintId, constraint in map(constraintMapper, cursor.fetchall()):
            cursor.execute(selectConstraintDetails, (schemaName, tableId, constraintId))
            constraint.items = list(map(lambda x: x[0], cursor.fetchall()))
            table.constraints.append(constraint)

        cursor.execute(selectIndices, (schemaName, table.name))
        for indexId, index in map(indexMapper, cursor.fetchall()):
            cursor.execute(selectIndexDetails, (schemaName, tableId, indexId))
            index.fields = list(map(indexItemMapper, cursor.fetchall()))
            table.indexes.append(index)

        schema.tables.append(table)
    
    
    
    return schema
    

    
    
    
    
    
def domainMapper(fetchrow):
    domain = Domain()
    (id_,
    domain.name,
    domain.descr,
    domain.type,
    domain.length,
    domain.char_length,
    domain.precision,
    domain.scale,
    domain.width,
    domain.align,
    domain.show_null,
    domain.show_lead_nulls,
    domain.thousands_separator,
    domain.summable,
    domain.case_sensitive) = fetchrow
    return id_, domain

def tableMapper(fetchrow):
    table = Table()
    (id_,
    table.name,
    table.descr,
    table.add,
    table.edit,
    table.delete) = fetchrow
    return id_, table

def fieldMapper(fetchrow):
    field = Field()
    (id_,
    field.name,
    field.rname,
    field.descr,
    field.domain,
    field.input,
    field.edit,
    field.show_in_grid,
    field.show_in_details,
    field.is_mean,
    field.autocalculated,
    field.required) = fetchrow
    return id_, field

def constraintMapper(fetchrow):
    constraint = Constraint()
    (id_,
    constraint.name,
    constraint.kind,
    constraint.reference,
    constraint.has_value_edit,
    constraint.cascading_delete,
    constraint.expression) = fetchrow
    return id_, constraint

def indexMapper(fetchrow):
    index = Index()
    id_ = fetchrow[0]
    index.name = fetchrow[1]
    index.is_clustered = True if fetchrow[3] == "clustered" else False
    return id_, index

def indexItemMapper(fetchrow):
    indexItem = IndexItem()
    indexItem.name,
    indexItem.expression,
    indexItem.desc = fetchrow
    return indexItem


