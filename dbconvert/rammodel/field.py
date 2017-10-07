# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 01:01:44 2017

@author: 1
"""
try:
    from entity import Entity
except ModuleNotFoundError:
    from .entity import Entity

class Field(Entity):

    def __init__(self):
        self.name = None
        self.rname = None
        self.domain = None
        self.descr = None
        self.props = None


    def __repr__(self):
        return "<Field name={} rname={} domain={} descr={} props={}>".format(
                self.name,
                self.rname,
                self.domain,
                self.descr,
                self.props
                )
