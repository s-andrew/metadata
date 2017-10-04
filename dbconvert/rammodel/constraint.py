# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 01:01:44 2017

@author: 1
"""

try:
    from entity import Entity
except ModuleNotFoundError:
    from .entity import Entity

class Constraint(Entity):

    def __init__(self):
        self.name = None
        self.kind = None
        self.items = None
        self.props = None
        self.reference_type = None
        self.reference = None

    def __repr__(self):
        return "<Constraint name={} kind={} items={} props={} reference_type={} reference={} >".format(
                self.name,
                self.kind,
                self.items,
                self.props,
                self.reference_type,
                self.reference
                )


