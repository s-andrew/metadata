class Schema:
#    __slots__ = [
#        "fulltext_engine",
#        "version",
#        "name",
#        "descr",
#        "domains",
#        "tables"
#        ]

    def __init__(self):
        self.fulltext_engine = None
        self.version = None
        self.name = None
        self.descr = None
        self.domains = []
        self.tables = []