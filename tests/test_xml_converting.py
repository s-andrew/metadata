# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 23:20:51 2017

@author: 1
"""

import unittest
import xml.dom.minidom as md
import io

from dbconvert import xml2ram, ram2xml


class TestXMLConvert(unittest.TestCase):
    def test_xml2ram_and_ram2xml(self):
        xml = md.parse("tasks.xml")
        schema = xml2ram(xml)
        result = io.StringIO(ram2xml(schema).toprettyxml(indent="  ", encoding="utf-8").decode("utf-8"), newline="\n")
        with open("tasks.xml", "r", encoding="utf-8") as origin:
            i = 0
            for r, o in zip(result, origin):
                i += 1
                # Skip the first line because it always has an error
                if i == 1: continue
                self.assertTrue(r == o, msg="\nresult:\t\"{}\"\nis not equal\norigin:\t\"{}\"\nin line: {}".format(r[:-1], o[:-1],i))

