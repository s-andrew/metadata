# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 01:01:44 2017

@author: 1
"""
class Index:
    __slots__ = [
        "name",
        "fulltext",
        "uniqueness",
        "fields"
        ]

    def __init__(self):
        self.name = None
        self.fulltext = False
        self.uniqueness = False
        self.fields = []