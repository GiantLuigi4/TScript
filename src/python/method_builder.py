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
    # if function_text.startswith('def:'):
    #     function_text = function_text.replace('def:', 'dv:', 1)
    # elif function_text.startswith('define:'):
    #     function_text = function_text.replace('define:', 'dv:', 1)
    # elif function_text.startswith('gotoEnd'):
    #     function_text = function_text.replace('gotoEnd', 'ge', 1)
    # elif function_text.startswith('goToEnd'):
    #     function_text = function_text.replace('goToEnd', 'ge', 1)
    # elif function_text.startswith('wait:'):
    #     function_text = function_text.replace('wait:', 'w:', 1)
    # elif function_text.startswith('sleep:'):
    #     function_text = function_text.replace('sleep:', 'w:', 1)
    # elif function_text.startswith('goto:'):
    #     function_text = function_text.replace('goto:', 'gt:', 1)
    # elif function_text.startswith('goTo:'):
    #     function_text = function_text.replace('goTo:', 'gt:', 1)
    # elif function_text.startswith('gotoMark:'):
    #     function_text = function_text.replace('gotoMark:', 'gtm:', 1)
    # elif function_text.startswith('goToMark:'):
    #     function_text = function_text.replace('goToMark:', 'gtm:', 1)
    # elif function_text.startswith('skip:'):
    #     function_text = function_text.replace('skip:', 'sk:', 1)
    # elif function_text.startswith('goForward:'):
    #     function_text = function_text.replace('goForward:', 'sk:', 1)
    # elif function_text.endswith('--'):
    #     function_text = 'm:'+function_text.replace('-', '')+'-'+str((function_text.count('-')-1))
    # elif function_text.endswith('++'):
    #     function_text = 'm:'+function_text.replace('+', '')+'+'+str((function_text.count('+')-1))
    # return function_text


def build_from_file(name):
    name = str(name)
    if path.exists(name):
        f = open(name)
        lines = []
        lines.clear()
        for line in f.readlines():
            lines.append(line.rstrip())
        f.close()
        return build(name, lines)
    else:
        return method_class.Method(name='missing', function=['gotoEnd'])
