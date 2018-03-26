import sys
import xml.dom.minidom as md
import sqlite3

from dbconvert.xml2ram import xml2ram
from dbconvert.ram2sqlite import ram2sqlite


if len(sys.argv) < 3:
    print("Bad argument\n")
    sys.exit(1)
xml_file_name = sys.argv[1]
db_file_name = sys.argv[2]

xml = md.parse(xml_file_name)
schema = xml2ram(xml)
connect = sqlite3.connect(db_file_name)
ram2sqlite(schema, connect)
connect.commit()

