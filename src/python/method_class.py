from python import executor


class Method:
    list = []
    name = ''

    def __init__(self, function, name) -> None:
        super().__init__()
        self.name = name
        self.list = function

    def execute(self, variables={}):
        line = 0
        while True:
            val = self.__execute__(line, variables)
            if not str(val).startswith('reload:'):
                return val
            else:
                line = int(val.replace('reload:', '', 1))+1

    def __execute__(self, line, variables={}):
        return executor.run(self, line, variables)

    def __str__(self) -> str:
        return "Code=" + str(self.list) + ",Name=" + str(self.name)
