#from dbconvert.parser import Parser
##help(Parser)
#app = Parser()
#app.execute("tasks.xml")
#
#with open("result.xml", "w") as output_file:
#    app.createXML().writexml(output_file, addindent="  ", newl="\n", encoding="utf-8")
#    output_file.close()



import xml.dom.minidom as md

from dbconvert import xml2ram, ram2xml

xml = md.parse("tasks.xml")
schema = xml2ram(xml)
with open("result.xml", "w") as output_file:
    ram2xml(schema).writexml(output_file, addindent="  ", newl="\n", encoding="utf-8")
    output_file.close()
#==============================================================================
#     Test
#==============================================================================
with open("result.xml", "r") as result, open("tasks.xml", "r", encoding="utf-8") as origin:
#    print(result.read() == origin.read())
    i = 0
    errors = {}
    for r, o in zip(result, origin):
        i += 1
        if r != o:
            errors.update({i: {"origin": o, "result": r}})
    result.close()
    origin.close()

for er in errors:
    print(er,"\torigin: ", repr(errors[er]["origin"]), "\n\tresult: ", repr(errors[er]["result"]))

# Ошибка в первой строке из-за того,
# что оригинальный файл начинается с \ufeff
