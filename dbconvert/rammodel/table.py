# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 01:01:44 2017

@author: 1
"""
try:
    from entity import Entity
except ModuleNotFoundError:
    from .entity import Entity

class Table(Entity):

    def __init__(self):
        self.name = None
        self.descr = None
        self.props = None
        self.ht_table_flags = None
        self.access_level = None
        self.fields = []
        self.constraints = []
        self.indexes = []

    def __repr__(self):
        return "<Table name={} descr={},props={} ht_table_flags={} access_level={} >".format(
                self.name,
                self.descr,
                self.props,
                self.ht_table_flags,
                self.access_level
                )