# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 01:01:44 2017

@author: 1
"""
class Domain:
    __slots__ = [
        "name",
        "descr",
        "type",
        "align",
        "width",
        "precision",
        "show_null",
        "summable",
        "case_sensitive",
        "show_lead_nulls",
        "thousands_separator",
        "char_length",
        "length",
        "scale"
        ]

    def __init__(self):
        self.name = None
        self.descr = None
        self.type = None
        self.align = None
        self.width = None
        self.precision = None
        self.show_null = False
        self.summable = False
        self.case_sensitive = False
        self.show_lead_nulls = False
        self.thousands_separator = False
        self.char_length = None
        self.length = None
        self.scale = None

