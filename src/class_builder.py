from src.classes import Clazz
from src.classes import Method


def build(name, data):
    clazz = Clazz()
    clazz.name = name
    for methodName in data["Methods"]:
        method = Method()
        method.name = methodName
        method.list.append(data["Methods"][methodName])
        clazz.methodDict.update({methodName: method})
    return clazz
