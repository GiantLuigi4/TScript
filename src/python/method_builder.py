# https://www.guru99.com/python-check-if-file-exists.html
from os import path

from python import function_registry
from python import method_class


def build(name, data):
    func_list = []
    for function_text in data:
        function_text = function_text.lstrip()
        if function_text.startswith('//'):
            function_text = ''
        func_list.append(map_func(function_text))
    method = method_class.Method(name=name.replace("../", ''), function=func_list)
    return method


def map_func(function_text):
    function_text = str(function_text)
    return function_registry.remap(function_text)


def build_from_file(name):
    name = str(name)
    if path.exists(name):
        f = open(name, encoding="utf8")
        lines = []
        lines.clear()
        line = ''
        try:
            for line in f.readlines():
                lines.append(line.rstrip())
        except Exception as exc:
            print('File Name: ' + name)
            print('Reading Line: ' + line)
            raise exc
        f.close()
        return build(name, lines)
    else:
        return method_class.Method(name='missing', function=['gotoEnd'])
