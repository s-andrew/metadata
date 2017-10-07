# -*- coding: utf-8 -*-
"""
Created on Sun Sep 24 01:01:44 2017

@author: 1
"""

#import Entity
try:
    from entity import Entity
except ModuleNotFoundError:
    from .entity import Entity


class Domain(Entity):
#    __slots__ = ["name", "descr", "type", "align", "widtn", "props", "char_length", "length", "scale"]


#    def __init__(self, **kwargs ):
#        for slot in self.__slots__:
#            exec("self.{} = {}".format(slot, repr(kwargs.get(slot, None))))

    def __init__(self):
        self.name = None
        self.descr = None
        self.type = None
        self.align = None
        self.width = None
        self.precision = None
        self.props = None
        self.char_length = None
        self.length = None
        self.scale = None


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


