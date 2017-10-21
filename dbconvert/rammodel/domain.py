# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 01:01:44 2017

@author: 1
"""
class Domain:
#    propsList = ['show_null', 'summable', 'case_sensitive']

    def __init__(self):
        self.name = None
        self.descr = None
        self.type = None
        self.align = None
        self.width = None
        self.precision = None
#        self.props = None
        self.show_null = False
        self.summable = False
        self.case_sensitive = False
        self.char_length = None
        self.length = None
        self.scale = None

    def setPropsFromStr(self, propsStr, sep=", "):
        for prop in propsStr.split(sep):
            if prop == "show_null":
                self.show_null = True
            elif prop == "summable":
                self.summable = True
            elif prop == "case_sensitive":
                self.case_sensitive = True
            else:
                raise ValueError("Invalid format of propsStr: {}".format(propsStr))

    def getPropsAsStr(self, sep=", "):
        l = []
        if self.show_null:
            l.append("show_null")
        if self.summable:
            l.append("summable")
        if self.case_sensitive:
            l.append("case_sensitive")
        return sep.join(l)


    def __repr__(self):
        return "<Domain name={} descr={} type={} align={} width={} precision={} props={} char_length={} tlength={} tscale={}>".format(
                self.name,
                self.descr,
                self.type,
                self.align,
                self.width,
                self.precision,
                self.props,
                self.char_length,
                self.length,
                self.scale
                )


if __name__ == "__main__":
    d = Domain()
    dir(d)
    print(d)


