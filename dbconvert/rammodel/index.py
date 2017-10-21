# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 01:01:44 2017

@author: 1
"""
class Index:
#    propsList = ['fulltext', 'uniqueness']

    def __init__(self):
        self.name = None
#        self.props = None
        self. fulltext = False
        self.uniqueness = False
        self.fields = []

    def setPropsFromStr(self, propsStr, sep=", "):
        for prop in propsStr.split(sep):
            if prop == "fulltext":
                self.fulltext = True
            elif prop == "uniqueness":
                self.uniqueness = True
            else:
                raise ValueError("Invalid format of propsStr: {}".format(propsStr))

    def getPropsAsStr(self, sep=", "):
        l = []
        if self.fulltext:
            l.append("fulltext")
        if self.uniqueness:
            l.append("uniqueness")
        return sep.join(l)


    def __repr__(self):
        return "<Index name={} props={} fields={} >".format(
                self.name,
                self.props,
                repr(self.fields)
                )
