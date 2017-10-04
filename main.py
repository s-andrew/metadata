from dbconvert import Parser
#help(Parser)
app = Parser()
app.execute("TASKS.xml")
#app.execute("..\PRJAdm.xml")
#s = app.schema.fullPrintStr()
#x = app.createXML().toprettyxml()
#print(app.createXML().toprettyxml())
