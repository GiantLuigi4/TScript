import classes


def build(name, data):
    list = []
    for methodText in data:
        list.append(methodText.lstrip())
    method = classes.Method(name=name, function=list)
    return method


def build_from_file(name):
    name = str(name)
    f = open(name)
    lines = []
    lines.clear()
    for line in f.readlines():
        lines.append(line.rstrip())
    f.close()
    return build(name, lines)
