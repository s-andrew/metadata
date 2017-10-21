# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 01:01:44 2017

@author: 1
"""
class Field:

#    propsList = ['input', 'edit', 'show_in_grid', 'show_in_details', 'is_mean', 'autocalculated', 'required']

    def __init__(self):
        self.name = None
        self.rname = None
        self.domain = None
        self.descr = None
#        self.props = None
        self.input = False
        self.edit = False
        self.show_in_grid = False
        self.show_in_details = False
        self.is_mean = False
        self.autocalculated = False
        self.required = False


    def setPropsFromStr(self, propsStr, sep=", "):
        for prop in propsStr.split(sep):
            if prop == "input":
                self.input = True
            elif prop == "edit":
                self.edit = True
            elif prop == "show_in_grid":
                self.show_in_grid = True
            elif prop == "show_in_details":
                self.show_in_details = True
            elif prop == "is_mean":
                self.is_mean = True
            elif prop == "autocalculated":
                self.autocalculated = True
            elif prop == "required":
                self.required = True
            else:
                raise ValueError("Invalid format of propsStr: {}".format(propsStr))

    def getPropsAsStr(self, sep=", "):
        l = []
        if self.input:
            l.append("input")
        if self.edit:
            l.append("edit")
        if self.show_in_grid:
            l.append("show_in_grid")
        if self.show_in_details:
            l.append("show_in_details")
        if self.is_mean:
            l.append("is_mean")
        if self.autocalculated:
            l.append("autocalculated")
        if self.required:
            l.append("required")
        return sep.join(l)


    def __repr__(self):
        return "<Field name={} rname={} domain={} descr={} props={}>".format(
                self.name,
                self.rname,
                self.domain,
                self.descr,
                self.props
                )
