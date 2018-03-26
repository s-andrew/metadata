# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 11:43:51 2017

@author: 1
"""
import functools


from dbconvert import minidom_fixed as md
from dbconvert.rammodel.domain import Domain
from dbconvert.rammodel.table import Table
from dbconvert.rammodel.field import Field
from dbconvert.rammodel.index import Index, IndexItem
from dbconvert.rammodel.constraint import Constraint
from dbconvert.rammodel.schema import Schema

__all__ = ["ram2xml"]






def ram2xml(schema):
    """
    Create xml.dom.minidom.Document from app.schema
    RAM model -> XML
    Args:
        schema: object Schema
    Return:
        xml.dom.minidom.Document
    """
    if schema is None:
        raise ValueError("Schema is missing")

    xml = md.Document()
#    xml.encoding = "utf-8"

    # Create node for the schema
    node = xml.createElement("dbd_schema")
    if schema.fulltext_engine is not None:
        node.setAttribute("fulltext_engine", str(schema.fulltext_engine))
    if schema.version is not None:
        node.setAttribute("version", str(schema.version))
    if schema.name is not None:
        node.setAttribute("name", str(schema.name))
    if schema.descr is not None:
        node.setAttribute("description", str(schema.descr))
    node.appendChild(xml.createElement("custom"))

    domains = xml.createElement("domains")
    createDomain = functools.partial(_createDomainNode, xml)
    for domain in map(createDomain, schema.domains):
        domains.appendChild(domain)
    node.appendChild(domains)

    tables = xml.createElement("tables")
    createTable = functools.partial(_createTableNode, xml)
    for table in map(createTable, schema.tables):
        tables.appendChild(table)
    node.appendChild(tables)

    xml.appendChild(node)
    return xml

        
def _createDomainNode(xml, domain, node=None):
    """
    Create DOM element domain.
    
    If node is not None doesn't create
    a new DOM element domain, but writes
    the properties of the domain to the
    attributes of the node.
    
    Args:
        xml : xml.dom.minidom.Document
        domain: dbconvert.rammodel.Domain
        node: xml.dom.minidom.Element default None
        
    Return: DOM element domain
    """
    # Check node
    if node is None:
        node = xml.createElement("domain")
        
    #Set attributes
    if domain.name is not None:
        node.setAttribute("name", str(domain.name))
    if domain.descr is not None:
        node.setAttribute("description", str(domain.descr))
    if domain.type is not None:
        node.setAttribute("type", str(domain.type))
    if domain.align is not None:
        node.setAttribute("align", str(domain.align))
    if domain.width is not None:
        node.setAttribute("width", str(domain.width))
    if domain.length is not None:
        node.setAttribute("length", str(domain.length))
    if domain.precision is not None:
        node.setAttribute("precision", str(domain.precision))
        
    #Create props
    propsList = []
    if domain.show_null:
        propsList.append("show_null")
    if domain.summable:
        propsList.append("summable")
    if domain.case_sensitive:
        propsList.append("case_sensitive")
    if domain.show_lead_nulls:
        propsList.append("show_lead_nulls")
    if domain.thousands_separator:
        propsList.append("thousands_separator")
    # Set attribute props
    if propsList != []:
        node.setAttribute("props", ", ".join(propsList))
    
    # Set attributes again
    if domain.char_length is not None:
        node.setAttribute("char_length", str(domain.char_length))
    if domain.length is not None:
        node.setAttribute("length", str(domain.length))
    if domain.scale is not None:
        node.setAttribute("scale", str(domain.scale))
    return node


def _createTableNode(xml, table):
    """
    Create DOM element table

    Args:
        xml : xml.dom.minidom.Document
        table: dbconvert.rammodel.Table

    Return: DOM element table
    """
    # Create node
    node = xml.createElement("table")
    
    # Set attributes
    if table.name is not None:
        node.setAttribute("name", str(table.name))
    if  table.descr is not None:
        node.setAttribute("description", str(table.descr))
        
    # Create props
    propsList = []
    if table.add:
        propsList.append("add")
    if table.edit:
        propsList.append("edit")
    if table.delete:
        propsList.append("delete")
    # Set attribute props
    if propsList != []:
        node.setAttribute("props", ", ".join(propsList))
        
    # Set attributes again
    if table.ht_table_flags is not None:
        node.setAttribute("ht_table_flags", str(table.ht_table_flags))
    if table.access_level is not None:
        node.setAttribute("access_level", str(table.access_level))

    # Append fields elements
    createField = functools.partial(_createFieldNode, xml)
    for field in map(createField, table.fields):
        node.appendChild(field)

    # Append constraint elements
    createConstraint = functools.partial(_createConstraintNode, xml)
    for constraint in map(createConstraint, table.constraints):
        node.appendChild(constraint)
    
    # Append index elements
    createIndex = functools.partial(_createIndexNode, xml)
    for index in map(createIndex, table.indexes):
        node.appendChild(index)

    return node

def _createFieldNode(xml, field):
    """
    Create DOM element field

    Args:
        xml   : xml.dom.minidom.Document
        table : object Table

    Return: DOM element field
    """
    # Create node
    node = xml.createElement("field")
    
    # Set attributes
    if field.name is not None:
        node.setAttribute("name", str(field.name))
    if field.rname is not None:
        node.setAttribute("rname", str(field.rname))
    if field.domain is not None:
        if isinstance(field.domain, Domain):
            node = _createDomainNode(xml, field.domain, node)
        else:
            node.setAttribute("domain", str(field.domain))
    if field.descr is not None:
        node.setAttribute("description", str(field.descr))
        
    # Create props
    propsList = []
    if field.input:
        propsList.append("input")
    if field.edit:
        propsList.append("edit")
    if field.show_in_grid:
        propsList.append("show_in_grid")
    if field.show_in_details:
        propsList.append("show_in_details")
    if field.is_mean:
        propsList.append("is_mean")
    if field.autocalculated:
        propsList.append("autocalculated")
    if field.required:
        propsList.append("required")
    # Set attribute props
    if propsList != []:
        node.setAttribute("props", ", ".join(propsList))

    return node


def _createConstraintNode(xml, constraint):
    """
    Create DOM element constraint

    Args:
        xml   : xml.dom.minidom.Document
        table : object Table

    Return: DOM element constraint
    """
    # Create node
    node = xml.createElement("constraint")
    
    # Set attributes
    if constraint.name is not None:
        node.setAttribute("name", str(constraint.name))
    if constraint.kind is not None:
        node.setAttribute("kind", str(constraint.kind))
    if constraint.items is not None:
        if len(constraint.items) == 1:
              node.setAttribute("items", str(constraint.items[0]))
        else:
            pass # Когда много item'ов
    if constraint.reference_type is not None:
        node.setAttribute("reference_type", str(constraint.reference_type))
    if constraint.reference is not None:
        node.setAttribute("reference", str(constraint.reference))
    if constraint.expression is not None:
        node.setAttribute("expression", str(constraint.expression))
        
    # Create props
    propsList = []
    if constraint.has_value_edit:
        propsList.append("has_value_edit")
    if constraint.cascading_delete:
        propsList.append("cascading_delete")
    if constraint.full_cascading_delete:
        propsList.append("full_cascading_delete")
    # Set attribute props
    if propsList != []:
        node.setAttribute("props", ", ".join(propsList))
    return node


def _createIndexNode(xml, index):
    """
    Create DOM element index

    Args:
        xml   : xml.dom.minidom.Document
        table : object Table

    Return: DOM element index
    """
    # Check fields
    if index.fields != []:
        # Create node
        node = xml.createElement("index")
        # Check single field
        if len(index.fields) == 1:
            node.setAttribute("field", str(index.fields[0].name))
        else:
            # ветка для случая, когда в индекс входит больше одного поля
            createItem = functools.partial(_createIndexItem, xml)
            for item in map(createItem, index.fields):
                node.appendChild(item)
        
        # Set attributes
        if index.name is not None:
            node.setAttribute("name", str(index.name))
            
        # Create props
        propsList = []
        if index.fulltext:
            propsList.append("fulltext")
        if index.uniqueness:
            propsList.append("uniqueness")
        if index.is_clustered:
            propsList.append("clustered")
        # Set attribute props
        if propsList != []:
            node.setAttribute("props", ", ".join(propsList))

        return node
    else:
        # Raise if index doesn't have any fields 
        raise ValueError("Error! Index does not contain fields")
        

def _createIndexItem(xml, item):
    """
    Create DOM element item (index item)

    Args:
        xml   : xml.dom.minidom.Document
        item : object IndexItem

    Return: DOM element item
    """
    node = xml.createElement("item")
    node.setAttribute("name", str(item.name))
    node.setAttribute("position", str(item.position))
    if item.desc:
        node.setAttribute("desc")
    return node


