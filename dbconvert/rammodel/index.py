# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 01:01:44 2017

@author: 1
"""
class Index:
    def __init__(self):
        self.name = None
        self.fulltext = False
        self.uniqueness = False
        self.fields = []
    
        self.is_clustered = False
        
        
class IndexItem:
    def __init__(self):
        self.name = None
        self.expression = None
        self.desc = False
