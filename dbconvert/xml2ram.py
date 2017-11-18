# -*- coding: utf-8 -*-
"""
Created on Sat Oct 21 11:43:51 2017

@author: 1
"""
import xml.dom.minidom as md

from dbconvert.rammodel import Domain, Table, Field, Index, Constraint, Schema


__all__ = ["xml2ram"]


def xml2ram(xml):
    """
    Create object Schema from xml.dom.minidom.Document
    XML -> RAM model
    Args:
        xml : xml.dom.minidom.Document
    Return: object Schema
    """
    schema = Schema()
    for attrName, attrValue in xml.documentElement.attributes.items():
        if attrName.lower() == "fulltext_engine":
            schema.fulltext_engine = attrValue
        elif attrName.lower() == "version":
            schema.version = attrValue
        elif attrName.lower() == "name":
            schema.name = attrValue
        elif attrName.lower() == "description":
            schema.descr = attrValue
        else:
            raise ValueError("In tag \"{}\" invalid attribute name \"{}\"".format(schema.nodeName, attrName))
    schema.domains = _parseDomains(xml)
    schema.tables = _parseTables(xml)

    return schema

def _parseDomains(xml):
    """
    Create list of objects Domain

    Args:
        xml : xml.dom.minidom.Document

    Return: list<Domain>

    """
    domainList = []
    for domain in xml.getElementsByTagName("domain"):
        tmp = Domain()
        for attrName, attrValue in domain.attributes.items():
            if attrName.lower() == "name":
                tmp.name = attrValue
            elif attrName.lower() == "description":
                tmp.descr = attrValue
            elif attrName.lower() == "type":
                tmp.type = attrValue
            elif attrName.lower() == "align":
                tmp.align = attrValue
            elif attrName.lower() == "width":
                tmp.width = attrValue
            elif attrName.lower() == "precision":
                tmp.precision = attrValue
            elif attrName.lower() == "props":
                for prop in attrValue.split(", "):
                    if prop == "show_null":
                        tmp.show_null = True
                    elif prop == "summable":
                        tmp.summable = True
                    elif prop == "case_sensitive":
                        tmp.case_sensitive = True
                    elif prop == "show_lead_nulls":
                        tmp.show_lead_nulls = True
                    elif prop == "thousands_separator":
                        tmp.thousands_separator = True
                    else:
                        raise ValueError("Invalid format of props string: {}".format(attrValue))
            elif attrName.lower() == "char_length":
                tmp.char_length = attrValue
            elif attrName.lower() == "length":
                tmp.length = attrValue
            elif attrName.lower() == "scale":
                tmp.scale = attrValue
            else:
                raise ValueError("In tag \"{}\" Invalid attribute name \"{}\"".format(domain, attrName))

        domainList.append(tmp)

    return domainList

def _parseTables(xml):
    """
    Create list of object Table

    Args:
        xml : xml.dom.minidom.Document

    Return: list<Table>

    """
    tableList = []
    for table in xml.getElementsByTagName("table"):
        tmp = Table()

        for attrName, attrValue in table.attributes.items():
            if attrName.lower() == "name":
                tmp.name = attrValue
            elif attrName.lower() == "description":
                tmp.descr = attrValue
            elif attrName.lower() == "props":
                for prop in attrValue.split(", "):
                    if prop == "add":
                        tmp.add = True
                    elif prop == "edit":
                        tmp.edit = True
                    elif prop == "delete":
                        tmp.delete = True
                    else:
                        raise ValueError("Invalid format of props string: {}".format(attrValue))
            elif attrName.lower() == "ht_table_flags":
                tmp.ht_table_flags = attrValue
            elif attrName.lower() == "access_level":
                tmp.access_level = attrValue
            else:
                raise ValueError("In tag {} invalid attribute name \"{}\"".format(table.nodeName, attrName))

        tmp.fields = _parseFields(table)
        tmp.indexes = _parseIndexes(table)
        tmp.constraints = _parseConstraints(table)

        tableList.append(tmp)

    return tableList

def _parseFields(xml):
    """
    Create list of object Field

    Args:
        xml : DOM Element table

    Return: list<Field>

    """
    if xml.nodeName != "table":
        raise TypeError("Element is not table")

    fieldList = []
    for field in xml.getElementsByTagName("field"):
        tmp = Field()
        for attrName, attrValue in field.attributes.items():
            if attrName.lower() == "name":
                tmp.name = attrValue
            elif attrName.lower() == "rname":
                tmp.rname = attrValue
            elif attrName.lower() == "domain":
                tmp.domain = attrValue
            elif attrName.lower() == "props":
                for prop in attrValue.split(", "):
                    if prop == "input":
                        tmp.input = True
                    elif prop == "edit":
                        tmp.edit = True
                    elif prop == "show_in_grid":
                        tmp.show_in_grid = True
                    elif prop == "show_in_details":
                        tmp.show_in_details = True
                    elif prop == "is_mean":
                        tmp.is_mean = True
                    elif prop == "autocalculated":
                        tmp.autocalculated = True
                    elif prop == "required":
                        tmp.required = True
                    else:
                        raise ValueError("Invalid format of props string: {}".format(attrValue))
            elif attrName.lower() == "description":
                tmp.descr = attrValue
            else:
                raise ValueError("In tag \"{}\" invalid attribute name \"{}\"".format(field.nodeName, attrName))

        fieldList.append(tmp)

    return fieldList


def _parseConstraints(xml):
    """
    Create list of object Constraint

    Args:
        xml : DOM Element table

    Return: list<Constraint>

    """
    if xml.nodeName != "table":
        raise TypeError("Element is not table")

    constraintList = []
    for constraint in xml.getElementsByTagName("constraint"):
        tmp = Constraint()
        for attrName, attrValue in constraint.attributes.items():
            if attrName.lower() == "name":
                tmp.name = attrValue
            elif attrName.lower() == "kind":
                tmp.kind = attrValue
            elif attrName.lower() == "items":
                tmp.items = attrValue
            elif attrName.lower() == "props":
                for prop in attrValue.split(", "):
                    if prop == "has_value_edit":
                        tmp.has_value_edit = True
                    elif prop == "cascading_delete":
                        tmp.cascading_delete = True
                    elif prop == "full_cascading_delete":
                        tmp.full_cascading_delete = True
                    else:
                        raise ValueError("Invalid format of props string: {}".format(attrValue))
            elif attrName.lower() == "reference_type":
                tmp.reference_type = attrValue
            elif attrName.lower() == "reference":
                tmp.reference = attrValue
            else:
                raise ValueError("In tag \"{}\" invalid attribute name \"{}\"".format(constraint.nodeName, attrName))
        constraintList.append(tmp)
    return constraintList

def _parseIndexes(xml):
    """
    Create list of object Index

    Args:
        xml : DOM Element table

    Return: list<Index>

    """
    if xml.nodeName != "table":
        raise TypeError("Element is not table")

    indexList = []
    for index in xml.getElementsByTagName("index"):
        tmp = Index()
        if index.hasChildNodes():
            for item in index.getElementsByTagName("item"):
                pass
                # ветка для случая, когда в индекс входит больше одного поля
                # хз что тут делать
                # в предложенных xml файлах такого не было
        else:
            tmp.fields.append(index.getAttribute("field"))
        for attrName, attrValue in index.attributes.items():
            if attrName.lower() == "field":
                pass
            elif attrName.lower() == "props":
                for prop in attrValue.split(", "):
                    if prop == "fulltext":
                        tmp.fulltext = True
                    elif prop == "uniqueness":
                        tmp.uniqueness = True
                    else:
                        raise ValueError("Invalid format of props string: {}".format(attrValue))
            else:
                raise ValueError("In tag \"{}\" invalid attribute name \"{}\"".format(index.nodeName, attrName))
        indexList.append(tmp)
    return indexList