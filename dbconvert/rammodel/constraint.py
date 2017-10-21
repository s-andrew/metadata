# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 01:01:44 2017

@author: 1
"""
class Constraint:
#    propsList = ['has_value_edit', 'cascading_delete', 'full_cascading_delete']

    def __init__(self):
        self.name = None
        self.kind = None
        self.items = None
        self.reference_type = None
        self.reference = None
#        self.props = None
        self.has_value_edit = False
        self.cascading_delete = False
        self.full_cascading_delete = False

    def setPropsFromStr(self, propsStr, sep=", "):
        for prop in propsStr.split(sep):
            if prop == "has_value_edit":
                self.has_value_edit = True
            elif prop == "cascading_delete":
                self.cascading_delete = True
            elif prop == "full_cascading_delete":
                self.full_cascading_delete = True
            else:
                raise ValueError("Invalid format of propsStr: {}".format(propsStr))

    def getPropsAsStr(self, sep=", "):
        l = []
        if self.has_value_edit:
            l.append("has_value_edit")
        if self.cascading_delete:
            l.append("cascading_delete")
        if self.full_cascading_delete:
            l.append("full_cascading_delete")
        return sep.join(l)


    def __repr__(self):
        return "<Constraint name={} kind={} items={} reference_type={} reference={} props={} >".format(
                self.name,
                self.kind,
                self.items,
                self.reference_type,
                self.reference,
                self.props
                )


