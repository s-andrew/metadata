import xml.dom.minidom as md
import sqlite3

from dbconvert import xml2ram, ram2xml, ram2sqlite

# Чтение XML при помощи minidom
xml = md.parse("tasks.xml")

# Создание объекта Schema из XML
schema = xml2ram(xml)

# Создание XML из объекта Schema
resXML = ram2xml(schema)


# Создание соединения с базой при помощи sqlite3
#connect = sqlite3.connect("test_db.db")
connect = sqlite3.connect(":memory:")

# Заполнение базы данными из объекта Schema
ram2sqlite(schema, connect)

# Закрытие соединения с базой
connect.close()


import re
s = """
self.name = None
        self.descr = None
        self.add = False
        self.edit = False
        self.delete = False
        self.ht_table_flags = None
        self.access_level = None
        self.fields = []
        self.constraints = []
        self.indexes = []
"""


l = [i[1:] for i in re.findall(r"\.\w+", s)]


print("[\n\"" + "\",\n\"".join(l) + "\"\n]")




