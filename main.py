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

# Заполнение базы из объекта Schema
ram2sqlite(schema, connect)

# Закрытие соединения с базой
connect.close()