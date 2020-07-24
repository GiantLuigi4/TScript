from src.classes import *


def build(name, data):
    method = Method()
    method.name = name
    for methodText in data:
        method.list.append(methodText.lstrip())
    return method


def build_from_file(name):
    name = str(name)
    f = open(name)
    lines = []
    for line in f.readlines():
        lines.append(line.rstrip())
    return build(name, lines)
