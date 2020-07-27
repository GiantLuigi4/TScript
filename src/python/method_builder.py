from python import method_class


def build(name, data):
    func_list = []
    for function_text in data:
        function_text = function_text.lstrip()
        if function_text.startswith('//'):
            function_text = ''
        func_list.append(function_text)
    method = method_class.Method(name=name.replace("../", ''), function=func_list)
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
