# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 01:01:44 2017

@author: 1
"""
class Domain:
#    propsList = ['show_null', 'summable', 'case_sensitive', 'show_lead_nulls', 'thousands_separator']

    def __init__(self):
        self.name = None
        self.descr = None
        self.type = None
        self.align = None
        self.width = None
        self.precision = None
        # Props:
        self.show_null = False
        self.summable = False
        self.case_sensitive = False
        self.show_lead_nulls = False
        self.thousands_separator = False
        # endProps
        self.char_length = None
        self.length = None
        self.scale = None

    def asTuple(self):
        return (
                self.name,
                self.descr,
                self.type,
                self.length,
                self.precision,
                self.scale,
                self.width,
                self.align,
                self.show_null,
                self.show_lead_nulls,
                self.thousands_separator,
                self.summable,
                self.case_sensitive
                )

    def setPropsFromStr(self, propsStr, sep=", "):
        for prop in propsStr.split(sep):
            if prop == "show_null":
                self.show_null = True
            elif prop == "summable":
                self.summable = True
            elif prop == "case_sensitive":
                self.case_sensitive = True
            elif prop == "show_lead_nulls":
                self.show_lead_nulls = True
            elif prop == "thousands_separator":
                self.thousands_separator = True
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
        if self.show_lead_nulls:
            l.append("show_lead_nulls")
        if self.thousands_separator:
            l.append("thousands_separator")
        return sep.join(l)


    def __repr__(self):
        return "<Domain name={} descr={} type={} align={} width={} precision={} props={} char_length={} tlength={} tscale={}>".format(
                self.name,
                self.descr,
                self.type,
                self.align,
                self.width,
                self.precision,
                self.getPropsAsStr(),
                self.char_length,
                self.length,
                self.scale
                )


if __name__ == "__main__":
    d = Domain()
    d.__dict__
    dir(d)
    print(d)


