# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 01:01:44 2017

@author: 1
"""
class Table:
#    propsList = ['add', 'edit', 'delete']

    def __init__(self):
        self.name = None
        self.descr = None
#        self.props = None
        self.add = False
        self.edit = False
        self.delete = False
        self.ht_table_flags = None
        self.access_level = None
        self.fields = []
        self.constraints = []
        self.indexes = []

    def setPropsFromStr(self, propsStr, sep=", "):
        for prop in propsStr.split(sep):
            if prop == "add":
                self.add = True
            elif prop == "edit":
                self.edit = True
            elif prop == "delete":
                self.delete = True
            else:
                raise ValueError("Invalid format of propsStr: {}".format(propsStr))

    def getPropsAsStr(self, sep=", "):
        l = []
        if self.add:
            l.append("add")
        if self.edit:
            l.append("edit")
        if self.delete:
            l.append("delete")
        return sep.join(l)


    def __repr__(self):
        return "<Table name={} descr={},props={} ht_table_flags={} access_level={} >".format(
                self.name,
                self.descr,
                self.props,
                self.ht_table_flags,
                self.access_level
                )