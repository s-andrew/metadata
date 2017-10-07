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
        self.reference_type = None
        self.reference = None
        self.props = None

    def __repr__(self):
        return "<Constraint name={} kind={} items={} reference_type={} reference={} props={} >".format(
                self.name,
                self.kind,
                self.items,
                self.reference_type,
                self.reference,
                self.props
                )


