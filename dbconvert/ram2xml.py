# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 11:43:51 2017

@author: 1
"""
from dbconvert import minidom_fixed as md

try:
    from dbconvert.rammodel import Domain, Table, Field, Index, Constraint, Schema
except ModuleNotFoundError:
    from rammodel import Domain, Table, Field, Index, Constraint, Schema

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

    node = xml.createElement("dbd_schema")
    if schema.fulltext_engine is not None:
        node.setAttribute("fulltext_engine", schema.fulltext_engine)
    if schema.version is not None:
        node.setAttribute("version", schema.version)
    if schema.name is not None:
        node.setAttribute("name", schema.name)
    if schema.descr is not None:
        node.setAttribute("description", schema.descr)
    node.appendChild(xml.createElement("custom"))

    domains = xml.createElement("domains")
    for domain in _domainGenerator(xml, schema.domains):
        domains.appendChild(domain)
    node.appendChild(domains)

    tables = xml.createElement("tables")
    for table in _tableGenerator(xml, schema.tables):
        tables.appendChild(table)
    node.appendChild(tables)

    xml.appendChild(node)
    return xml

def _domainGenerator(xml, domains):
    """
    Generator of DOM element domain

    Args:
        xml : xml.dom.minidom.Document

    Yield: DOM element domain
    """
    for domain in domains:
        node = xml.createElement("domain")
        if domain.name is not None:
            node.setAttribute("name", domain.name)
        if domain.descr is not None:
            node.setAttribute("description", domain.descr)
        if domain.type is not None:
            node.setAttribute("type", domain.type)
        if domain.align is not None:
            node.setAttribute("align", domain.align)
        if domain.width is not None:
            node.setAttribute("width", domain.width)
        if domain.length is not None:
            node.setAttribute("length", domain.length)
        if domain.precision is not None:
            node.setAttribute("precision", domain.precision)
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
        if propsList != []:
            node.setAttribute("props", ", ".join(propsList))


        if domain.char_length is not None:
            node.setAttribute("char_length", domain.char_length)
        if domain.length is not None:
            node.setAttribute("length", domain.length)
        if domain.scale is not None:
            node.setAttribute("scale", domain.scale)
        yield node

def _tableGenerator(xml, tables):
    """
    Generator of DOM element table

    Args:
        xml : xml.dom.minidom.Document

    Yield: DOM element table
    """
    for table in tables:
        node = xml.createElement("table")
        if table.name is not None:
            node.setAttribute("name", table.name)
        if  table.descr is not None:
            node.setAttribute("description", table.descr)
        propsList = []
        if table.add:
            propsList.append("add")
        if table.edit:
            propsList.append("edit")
        if table.delete:
            propsList.append("delete")
        if propsList != []:
            node.setAttribute("props", ", ".join(propsList))

        if table.ht_table_flags is not None:
            node.setAttribute("ht_table_flags", table.ht_table_flags)
        if table.access_level is not None:
            node.setAttribute("access_level", table.access_level)

        if table.fields != []:
            for field in _fieldGenerator(xml, table.fields):
                node.appendChild(field)

        if table.constraints != []:
            for constrint in _constraintGenerator(xml, table.constraints):
                node.appendChild(constrint)

        if table.indexes != []:
            for index in _indexGenerator(xml, table.indexes):
                node.appendChild(index)

        yield node

def _fieldGenerator(xml, fields):
    """
    Generator of DOM element field

    Args:
        xml   : xml.dom.minidom.Document
        table : object Table

    Yield: DOM element field
    """
    for field in fields:
        node = xml.createElement("field")
        if field.name is not None:
            node.setAttribute("name", field.name)
        if field.rname is not None:
            node.setAttribute("rname", field.rname)
        if field.domain is not None:
            node.setAttribute("domain", field.domain)
        if field.descr is not None:
            node.setAttribute("description", field.descr)
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
        if propsList != []:
            node.setAttribute("props", ", ".join(propsList))

        yield node


def _constraintGenerator(xml, constraints):
    """
    Generator of DOM element constraint

    Args:
        xml   : xml.dom.minidom.Document
        table : object Table

    Yield: DOM element constraint
    """
    for constraint in constraints:
        node = xml.createElement("constraint")
        if constraint.name is not None:
            node.setAttribute("name", constraint.name)
        if constraint.kind is not None:
            node.setAttribute("kind", constraint.kind)
        if constraint.items is not None:
            node.setAttribute("items", constraint.items)
        if constraint.reference_type is not None:
            node.setAttribute("reference_type", constraint.reference_type)
        if constraint.reference is not None:
            node.setAttribute("reference", constraint.reference)
        propsList = []
        if constraint.has_value_edit:
            propsList.append("has_value_edit")
        if constraint.cascading_delete:
            propsList.append("cascading_delete")
        if constraint.full_cascading_delete:
            propsList.append("full_cascading_delete")
        if propsList != []:
            node.setAttribute("props", ", ".join(propsList))
        yield node


def _indexGenerator(xml, indexes):
    """
    Generator of DOM element index

    Args:
        xml   : xml.dom.minidom.Document
        table : object Table

    Yield: DOM element index
    """
    for index in indexes:
        if index.fields != []:
            node = xml.createElement("index")
            if len(index.fields) == 1:
                node.setAttribute("field", index.fields[0])
            else:
                # ветка для случая, когда в индекс входит больше одного поля
                pass
            if index.name is not None:
                node.setAttribute("name", index.name)
            propsList = []
            if index.fulltext:
                propsList.append("fulltext")
            if index.uniqueness:
                propsList.append("uniqueness")
            if propsList != []:
                node.setAttribute("props", ", ".join(propsList))

            yield node
        else:
            raise ValueError("Error! Index does not contain fields")


