try:
    from entity import Entity
except ModuleNotFoundError:
    from .entity import Entity

class Schema(Entity):

    def __init__(self):
        self.fulltext_engine = None
        self.version = None
        self.name = None
        self.descr = None
        self.domains = []
        self.tables = []

    def __repr__(self):
        return "<Schema fulltext_engine={} version={} name={} descr={} >".format(
                self.fulltext_engine,
                self.version,
                self.name,
                self.descr
                )
    def fullPrintStr(self):
        s = repr(self)
        for domain in self.domains:
            s += "\n\t" + repr(domain)
        for table in self.tables:
            s += "\n\t" + repr(table)
            for field in table.fields:
                s += "\n\t\t" + repr(field)
            for index in table.indexes:
                s += "\n\t\t" + repr(index)
            for constraint in table.constraints:
                s += "\n\t\t" + repr(constraint)
            s += "\n"

        return s + "\n"