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
