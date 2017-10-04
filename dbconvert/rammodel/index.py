# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 01:01:44 2017

@author: 1
"""

try:
    from entity import Entity
except ModuleNotFoundError:
    from .entity import Entity

class Index(Entity):

    def __init__(self):
        self.name = None
        self.props = None
        self.fields = []

    def __repr__(self):
        return "<Index name={} props={} fields={} >".format(
                self.name,
                self.props,
                repr(self.fields)
                )
