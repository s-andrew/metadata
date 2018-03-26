import sqlite3
import sys

from dbconvert.sqlite2ram import sqlite2ram
from dbconvert.ram2xml import ram2xml

if len(sys.argv) < 4:
    print("Bad argument\n\nArgument example:\npython dbd2xdb.py <db_file_name> <xml_file_name> <schema_name>\n")
    sys.exit(1)
db_file_name = sys.argv[1]
xml_file_name = sys.argv[2]
schema_name = sys.argv[3]

#db_file_name = "tasks.db"
#xml_file_name = "test.xml"
#schema_name = "TASKS"

connect = sqlite3.connect(db_file_name)
schema =  sqlite2ram(schema_name, connect)
xml = ram2xml(schema)
x = xml.toprettyxml(encoding="utf-8").decode("utf-8")
with open(xml_file_name, "w") as file:
    file.write(xml.toprettyxml(encoding="utf-8").decode("utf-8"))