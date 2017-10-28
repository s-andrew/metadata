# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 01:01:44 2017

@author: 1
"""
class Table:
    __slots__ = [
        "name",
        "descr",
        "add",
        "edit",
        "delete",
        "ht_table_flags",
        "access_level",
        "fields",
        "constraints",
        "indexes"
        ]

    def __init__(self):
        self.name = None
        self.descr = None
        self.add = False
        self.edit = False
        self.delete = False
        self.ht_table_flags = None
        self.access_level = None
        self.fields = []
        self.constraints = []
        self.indexes = []