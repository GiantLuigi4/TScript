from python import executor


class Method:
    list = []
    name = ''

    def __init__(self, function, name) -> None:
        super().__init__()
        self.name = name
        self.list = function

    def execute(self):
        executor.run(self)

    def __str__(self) -> str:
        return "Code="+str(self.list)+",Name="+str(self.name)


class Clazz:
    methodDict = {}
    fieldDict = {}
    name = ''

    def run_method(self, name):
        return (self.methodDict.get(name)).execute()

    def __str__(self) -> str:
        return "Methods="+str(self.methodDict)+",Fields="+str(self.fieldDict)+",Name="+str(self.name)
