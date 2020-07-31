import time

from python import executor
from python import method_loader


class Mapping:
    names = []
    mapped = ''
    split = ':'

    def __init__(self, names, mapped, split=':') -> None:
        super().__init__()
        self.names = names
        self.mapped = mapped
        self.split = split


class Function:
    name = ''

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def execute(self, args):
        pass


mapper = [
    Mapping(['def', 'define'], 'dv:'),
    Mapping(['gotoEnd', 'goToEnd'], 'ge', split='N\\A'),
    Mapping(['wait', 'sleep'], 'w:'),
    Mapping(['goto', 'goTo'], 'gt:'),
    Mapping(['gotoMark', 'goToMark'], 'gtm:'),
    Mapping(['skip', 'goForward'], 'sk:'),
    Mapping(['goBack', 'rewind'], 'rw:'),
    Mapping(['waitSeconds', 'sleepSeconds'], 'ws:'),
    Mapping(['py', 'pyExec', 'pyexec', 'execPy', 'execpy'], 'py:'),
    Mapping(['pyFile', 'pyFi', 'pyfile', 'pyfi'], 'pyfi:')
]


functions = []


def register_func(func):
    functions.append(func)


def remap(input_func):
    if input_func == '':
        return ''
    for mapping in mapper:
        for name in mapping.names:
            if name == input_func.split(mapping.split, 1)[0]:
                if mapping.split == 'N\\A':
                    return mapping.mapped
                return mapping.mapped + input_func.split(mapping.split, 1)[1]
    if input_func.endswith('--'):
        input_func = 'm:' + input_func.replace('-', '') + '-' + str((input_func.count('-') - 1))
    elif input_func.endswith('++'):
        input_func = 'm:' + input_func.replace('+', '') + '+' + str((input_func.count('+') - 1))
    return input_func


def register_mapping(names, mapping, splitter=':'):
    mapper.append(Mapping(names, mapping, splitter))


def run_line(func, args, method, line, method_object, markers, variables):
    if func == 'py':
        exec(args.replace('\\n', '\n'))
        return line + 1
    elif func == 'pyfi':
        file = open(args)
        command = file.read()
        exec(command)
        file.close()
        return line + 1
    elif func == 'w':
        time.sleep(float(executor.parse_value(args, method_object, markers, variables)) / 1000)
        return line + 1
        # WAIT SECONDS
    elif func == 'ws':
        time.sleep(int(executor.parse_value(args, method_object, markers, variables)))
        return line + 1
    # AWAIT USER INPUT
    elif func == 'await':
        input('')
        return line + 1
    # RELOAD
    elif func == 'reload':
        method_loader.method_dictionary.clear()
        return 'reload:' + str(line)
    # GET A VALUE, AND DO NOTHING WITH IT
    elif func.startswith('runVal:'):
        executor.parse_value_full(func.replace('runVal:', '', 1), method_object, markers, variables)
        return line + 1
    # SAY
    elif func == 'say':
        print(args.replace("'", "", 2))
        return line + 1
    # SAY NO RETURN
    elif func == 'saynl':
        print(args.replace("'", "", 2), end='')
        return line + 1
    # SAY VALUE
    elif func == 'sayAndParse':
        print(executor.parse_value_full(args, method_object, markers, variables))
        return line + 1
    # SAY VALUE NO RETURN
    elif func == 'sayAndParsenl':
        print(executor.parse_value_full(args, method_object, markers, variables), end='')
        return line + 1
    # GOTO END OF SCRIPT
    elif func == "ge":
        return "end"
    # CALL AND PARSE
    elif func == 'callAndParse':
        method_loader.load_or_get(executor.parse_value_full(args, method, markers, variables)) \
            .execute()
        return line + 1
    # CALL ANOTHER FILE
    elif func == 'call':
        method_loader.load_or_get(args).execute()
        return line + 1
    else:
        for function in functions:
            if function.name == func:
                function.execute(args)
