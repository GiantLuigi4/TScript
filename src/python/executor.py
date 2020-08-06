import random
from traceback import *

import math
import time

from python import function_registry
from python.errors import *


def run(method_object, line=0, variables={}):
    method = method_object.list
    last_line = 0
    labels = {}
    try:
        while line < len(list(method)):
            if line < 0:
                raise BadGoToError(
                    "Tried to execute non existent line "
                    + str(line)
                    + " in method "
                    + str(method_object.name)
                    + " coming from line "
                    + str(last_line)
                )
            last_line = line
            line = run_line(method, line, method_object, labels, variables)
            if line == "end":
                return
            elif str(line).startswith("reload:"):
                return line
            elif str(line).startswith('return:'):
                return line.replace('return:', '', 1)
    except Exception as exc:
        print_tb(exc.__traceback__)
        print("Error: ", str(exc))
        print('\n\n')
        print("Error while interpreting line " + str(line))
        print("If you thing this error should not be occuring,")
        print("please report this (with the file " + method_object.name + ") to the creator of TScript.")
        print("https://github.com/GiantLuigi4/TScript/")
    if line > len(list(method)):
        raise BadGoToError(
            "Execution of method "
            + str(method_object.name)
            + " stopped at line "
            + str(line)
            + " coming from line "
            + str(last_line)
            + " when said method only goes up to line "
            + str(len(list(method)))
        )


def run_line(method, line, method_object, markers, variables):
    func = str(method[line])
    # NOTIFY
    if func.startswith("notify:"):
        func = func.replace("notify:", '', 1)
        print("Hit line " + str(line) + " in method " + str(method_object.name) + ".")
        print("Text: " + str(func))
    if len(func) == 0:
        return line + 1
    if func.count(':') >= 1:
        func_split = func.split(':', 1)
        output = function_registry.run_line(func_split[0], func_split[1], method, line, method_object, markers,
                                            variables)
        if type(output) != type(None):
            return output
    if func.startswith('m:'):
        calc(func.replace('m:', '', 1), method_object, markers, variables)
    # REWIND
    elif func.startswith('rw:'):
        return line - handle_goto(func.replace('rw:', ''), method_object, markers, variables)
    # SKIP
    elif func.startswith('sk:'):
        return line + handle_goto(func.replace('sk:', ''), method_object, markers, variables)
    # GOTO
    elif func.startswith('gt:'):
        return handle_goto(func.replace('gt:', ''), method_object, markers, variables)
    # REWIND IF CONDITION IS FALSE
    elif func.startswith('ifNotRewind>'):
        num = get_num(func.replace("ifNotRewind>", "", 1))
        if not parse_whole_condition(func.replace("ifNotRewind>", "", 1).replace(str(num) + ":", '', 1), method_object,
                                     markers, variables):
            return line - num
    # SKIP IF CONDITION IS FALSE
    elif func.startswith('ifNotSkip>'):
        num = get_num(func.replace("ifNotSkip>", "", 1))
        if not parse_whole_condition(func.replace("ifNotSkip>", "", 1).replace(str(num) + ":", '', 1), method_object,
                                     markers, variables):
            return line + num
    # GOTO END IF CONDITION IS FALSE
    elif func.startswith('ifNotGotoEnd>'):
        num = get_num(func.replace("ifNotGotoEnd>", "", 1))
        if not parse_whole_condition(
                func.replace("ifNotGotoEnd>", "", 1).replace(str(num) + ":", '', 1), method_object, markers, variables):
            return "end"
    # GOTO END IF CONDITION IS TRUE
    elif func.startswith('ifGotoEnd>'):
        num = get_num(func.replace("ifGotoEnd>", "", 1))
        if parse_whole_condition(func.replace("ifGotoEnd>", "", 1).replace(str(num) + ":", '', 1), method_object,
                                 markers, variables):
            return "end"
    # REWIND IF CONDITION IS TRUE
    elif func.startswith('ifRewind>'):
        num = get_num(func.replace("ifRewind>", "", 1))
        if parse_whole_condition(func.replace("ifRewind>", "", 1).replace(str(num) + ":", '', 1), method_object,
                                 markers, variables):
            return line - num
    # GOTO IF CONDITION IS TRUE
    elif func.startswith('ifGoto>'):
        num = get_num(func.replace("ifGoto>", "", 1))
        if parse_whole_condition(func.replace("ifGoto>", "", 1).replace(str(num) + ":", '', 1), method_object, markers,
                                 variables):
            return num
    # GOTO MARKER IF CONDITION IS TRUE
    elif func.startswith('ifGotoMarker>'):
        mark = get_marker_name(func.replace("ifGotoMarker>", "", 1))
        if parse_whole_condition(func.replace("ifGotoMarker>", "", 1).replace(str(mark) + ":", '', 1), method_object,
                                 markers, variables):
            marked_label = markers.get(func.replace("ifGotoMarker>:", '', 1), "N\\A")
            if marked_label != "N\\A":
                return marked_label
            else:
                return find_marker(mark, method, line, method_object.name)
    # GOTO MARKER IF CONDITION IS FALSE
    elif func.startswith('ifNotGotoMarker>'):
        mark = get_marker_name(func.replace("ifNotGotoMarker>", "", 1))
        if not parse_whole_condition(func.replace("ifNotGotoMarker>", "", 1).replace(str(mark) + ":", '', 1),
                                     method_object, markers, variables):
            marked_label = markers.get(func.replace("ifNotGotoMarker>:", '', 1), "N\\A")
            if marked_label != "N\\A":
                return marked_label
            else:
                return find_marker(mark, method, line, method_object.name)
    # GOTO IF CONDITION IS FALSE
    elif func.startswith('ifNotGoto>'):
        num = get_num(func.replace("ifNotGoto>", "", 1))
        if not parse_whole_condition(func.replace("ifNotGoto>", "", 1).replace(str(num) + ":", '', 1), method_object,
                                     markers, variables):
            return num
    # SKIP IF CONDITION IS TRUE
    elif func.startswith('ifSkip>'):
        num = get_num(func.replace("ifSkip>", "", 1))
        if parse_whole_condition(func.replace("ifSkip>", "", 1).replace(str(num) + ":", '', 1), method_object, markers,
                                 variables):
            return line + num
    # PRINT EXECUTING FILE
    elif func.startswith('currentFile'):
        print("Current file: " + str(method_object.name))
    # EXIT
    elif func.startswith('exit'):
        # Python ends programs by throwing an error, idk why.
        if func.count(':') >= 1:
            raise SystemExit(get_num(func.replace('exit:', '')))
        else:
            raise SystemExit(0)
    # MARK
    elif func.startswith("mark:"):
        marked_label = markers.get(func.replace("mark:", '', 1), "N\\A")
        if marked_label != "N\\A":
            raise DoubledMarker("Doubled marker on line " + str(line) + " of method " + str(method_object.name))
        markers.update({func.replace("mark:", '', 1): line + 1})
    # DEFINE A VARIABLE
    elif func.startswith("dv:"):
        func_new = func.replace('dv:', '', 1)
        var = variables.get(func_new, "N\\A")
        if var != "N\\A":
            raise DoubledVariable("Doubled variable on line " + str(line) + " of method " + str(method_object.name))
        name = func_new.split(',')[0]
        if name.startswith('%'):
            name = str(
                parse_value_full(func_new.split(',')[0].replace("%", "", 1), method_object,
                                 markers, variables))
            if str(name) == 'False':
                name = func_new.split(',')[0]
        variables.update(
            {name: parse_value_full(func.replace('dv:', '', 1).split(',')[1],
                                    method_object, markers, variables)})
    # DESTROY A VARIABLE
    elif func.startswith("destroy:"):
        var = variables.get(func.replace("destroy:", '', 1), "N\\A")
        if var != "N\\A":
            variables.pop(func.replace('destroy:', '', 1))
    # UNMARK A MARKER
    elif func.startswith("unmark:"):
        mark = markers.get(func.replace("unmark:", '', 1), "N\\A")
        if mark != "N\\A":
            markers.pop(func.replace('unmark:', '', 1))
    # GOTO A MARKER
    elif func.startswith("gtm:"):
        marked_label = markers.get(func.replace("gtm:", '', 1), "N\\A")
        if marked_label != "N\\A":
            return marked_label
        else:
            return find_marker(func.replace("gtm:", '', 1), method, line, method_object.name)
    # CAST TO INT
    elif func.startswith('i:'):
        var = variables.get(func.replace("i:", '', 1), "N\\A")
        if var != "N\\A":
            name = func.replace('i:', '', 1)
            variables[name] = int(get_num(str(variables[name])))
    # CAST TO FLOAT
    elif func.startswith('f:'):
        var = variables.get(func.replace("f:", '', 1), "N\\A")
        if var != "N\\A":
            name = func.replace('f:', '', 1)
            variables[name] = float(get_num(str(variables[name])))
    # ROUND
    elif func.startswith('r:'):
        var = variables.get(func.replace("r:", '', 1), "N\\A")
        if var != "N\\A":
            name = func.replace('r:', '', 1)
            variables[name] = float(int(get_num(str(variables[name]))))
    # # ADD 1 TO A VARIABLE
    # elif func.endswith('++'):
    #     var = variables.get(func.replace("++", '', 1), "N\\A")
    #     if var != "N\\A" and str(var).isnumeric():
    #         name = func.replace('++', '', 1)
    #         variables[name] = int(variables[name]) + 1
    # # SUBTRACT 1 FROM A VARIABLE
    # elif func.endswith('--'):
    #     var = variables.get(func.replace("--", '', 1), "N\\A")
    #     if var != "N\\A" and str(var).isnumeric():
    #         name = func.replace('--', '', 1)
    #         variables[name] = int(variables[name]) - 1
    return line + 1


def get_variable_name(text, variables):
    if text.startswith('%'):
        text = variables[text.replace('%', '', 1)]
    return text


def calc(text, method_object, markers, variables):
    if text.count('=') >= 1:
        args = text.split('=')
        variables[get_variable_name(args[0], variables)] = parse_value_full(args[1], method_object, markers, variables)
    elif text.count('+') >= 1:
        args = text.split('+')
        arg1 = variables[get_variable_name(args[0], variables)]
        variables[get_variable_name(args[0], variables)] = add(arg1, parse_value_full(args[1], method_object,
                                                                                      markers, variables))
        # if str(arg1).isnumeric():
        #     arg1 = int(arg1)
        #     variables[get_variable_name(args[0], variables)] = arg1 + int(parse_value_full(args[1], method_object,
        #                                                                                    markers, variables))
        # elif str(arg1).isdecimal():
        #     arg1 = float(arg1)
        #     variables[get_variable_name(args[0], variables)] = arg1 + float(parse_value_full(args[1], method_object,
        #                                                                                      markers, variables))
        # else:
        #     if args[1].isnumeric():
        #         variables[get_variable_name(args[0], variables)] = arg1 + int(parse_value_full(args[1], method_object,
        #                                                                                        markers, variables))
        #     else:
        #         variables[get_variable_name(args[0], variables)] = str(arg1) + str(parse_value_full(args[1],
        #                                                                                             method_object,
        #                                                                                             markers, variables))
    elif text.count('-') >= 1:
        args = text.split('-')
        arg1 = variables[args[0]]
        if str(arg1).isnumeric():
            arg1 = int(arg1)
        elif str(arg1).isdecimal():
            arg1 = float(arg1)
        variables[args[0]] = arg1 - int(parse_value_full(args[1], method_object, markers, variables))
    elif text.count('*') >= 1:
        args = text.split('*')
        arg1 = variables[args[0]]
        if str(arg1).isnumeric():
            arg1 = int(arg1)
        elif str(arg1).isdecimal():
            arg1 = float(arg1)
        variables[args[0]] = arg1 * int(parse_value_full(args[1], method_object, markers, variables))
    elif text.count('/') >= 1:
        args = text.split('/')
        arg1 = variables[args[0]]
        if str(arg1).isdecimal():
            arg1 = float(arg1)
        elif str(arg1).isnumeric():
            arg1 = int(arg1)
        variables[args[0]] = arg1 / int(parse_value_full(args[1], method_object, markers, variables))


def find_marker(name, method, line_num, method_name):
    for i in range(0, len(method)):
        line = method[i]
        if line.startswith('notify:'):
            line = line.replace('notify:', '', 1)
        if line.startswith("mark:") and line.replace('mark:', '', 1) == name:
            return i + 1
        if line_num + i + 1 < len(method):
            line = method[line_num + i]
            if line.startswith('notify:'):
                line = line.replace('notify:', '', 1)
            if line.startswith("mark:") and line.replace('mark:', '', 1) == name:
                return line_num + i + 1
    raise RuntimeError(
        "Line "
        + str(line_num)
        + " tried to goto non existent goto "
        + str(name)
        + " in method "
        + str(method_name)
    )


def get_marker_name(text):
    if text.startswith('ifGotoMarker>'):
        text = text.replace('ifGotoMarker>', '', 1)
    text_return = ""
    is_end = False
    i = 0
    while not is_end:
        if text[i] == ':':
            is_end = True
        else:
            text_return = text_return + text[i]
        i = i + 1
    return text_return


def check_for_marker(name, markers):
    return markers.get(name, "N\\A") != "N\\A"


def trim_line(line):
    return line.lstrip()


def handle_goto(text, method_object, markers, variables):
    if text.isnumeric():
        return int(text)
    else:
        return int(parse_value(text, method_object, markers, variables))


def get_num(line):
    num = 0
    i = 0
    not_num = False
    negative = False
    while not not_num:
        if i < len(line):
            not_num = not str(line)[i].isnumeric()
            if str(line)[i] == '-':
                negative = True
                not_num = False
            else:
                if not not_num:
                    num = num * 10 + int(str(line)[i])
            i = i + 1
        else:
            break
    if not negative:
        return int(num)
    else:
        return int(-num)


def parse_whole_condition(condition, method_object, markers, variables):
    if str(condition) == 'true':
        return True
    elif str(condition) == 'false':
        return False
    else:
        val = False
        operator = ''
        for condition_val in str(condition).split():
            condition_val = condition_val.replace(' ', '')
            if condition_val == 'or' or condition_val == '||':
                operator = '&&'
            elif condition_val == 'and' or condition_val == '&&':
                operator = '||'
            elif operator == '||':
                operator = ''
                val = val and parse_condition(condition_val, method_object, markers, variables)
            elif operator == '&&':
                operator = ''
                val = val or parse_condition(condition_val, method_object, markers, variables)
            else:
                val = parse_condition(condition_val, method_object, markers, variables)
        if type(val) == bool_type:
            return val
    raise RuntimeError("Tried to parse boolean out of text " + str(condition))


def parse_condition(condition, method_object, markers, variables):
    condition_without_not = condition
    # NOT
    if condition.startswith('!'):
        condition_without_not = condition.replace('!', '', 1)
    value = False
    # TRUE
    if condition == 'true' or condition == '!true':
        value = True
    # FALSE
    elif condition == 'false' or condition == '!false':
        value = False
    elif condition_without_not.startswith('checkMarker:'):
        value = check_for_marker(condition_without_not.replace('checkMarker:', '', 1), markers)
    # RANDOM
    elif condition_without_not == 'random' or condition_without_not == 'rand':
        value = random.randrange(0, 2) == 1
    # RESOLVE
    elif str(condition_without_not).startswith('r:('):
        value = resolve(condition_without_not.replace('r:(', '', 1).replace(')', '', 1), method_object, markers,
                        variables)
    # NOT
    if str(condition).startswith('!'):
        return not value
    # NORMAL
    else:
        return value


def resolve(condition, method_object, markers, variables):
    if condition.count('==') >= 1:
        condition_split = condition.split('==', 1)
        return str(parse_value_full(condition_split[0], method_object, markers, variables
                                    )) == str(parse_value_full(condition_split[1], method_object, markers, variables))
    if condition.count('!=') >= 1:
        condition_split = condition.split('!=', 1)
        return str(parse_value_full(condition_split[0], method_object, markers, variables
                                    )) != str(parse_value_full(condition_split[1], method_object, markers, variables))
    elif condition.count('>=') >= 1:
        condition_split = condition.split('>=', 1)
        return int(parse_value_full(condition_split[0], method_object, markers, variables
                                    )) >= int(parse_value_full(condition_split[1], method_object, markers, variables))
    elif condition.count('<=') >= 1:
        condition_split = condition.split('<=', 1)
        return int(parse_value_full(condition_split[0], method_object, markers, variables
                                    )) <= int(parse_value_full(condition_split[1], method_object, markers, variables))
    elif condition.count('>') >= 1:
        condition_split = condition.split('>', 1)
        return int(parse_value_full(condition_split[0], method_object, markers, variables
                                    )) > int(parse_value_full(condition_split[1], method_object, markers, variables))
    elif condition.count('<') >= 1:
        condition_split = condition.split('<', 1)
        return int(parse_value_full(condition_split[0], method_object, markers, variables
                                    )) < int(parse_value_full(condition_split[1], method_object, markers, variables))
    else:
        return False


def parse_value_full(text, method_object, markers, variables):
    if text.startswith('%'):
        text = '%' + str(parse_value_full(text.replace('%', '', 1), method_object, markers, variables))
    for line in text.split():
        if line.startswith('%'):
            line = line.replace('%', '', 1)
        var = variables.get(line, "N\\A")
        if var != "N\\A":
            return str(var)
    val = parse_string(text)
    if val != 'NAS':
        return val
    else:
        return parse_value(text, method_object, markers, variables)


def replace_last_char(text):
    new_text = ''
    index = 0
    length = len(text)
    for char in text:
        if length - 1 != index:
            new_text = new_text + char
        index = index + 1
    return new_text


def parse_value(text, method_object, markers, variables):
    val = parse_number(text, method_object, markers, variables)
    if val == "NAN":
        val = parse_string(text)
        if val != "NAS":
            return val
        else:
            return parse_whole_condition(text, method_object, markers, variables)
    else:
        return val


number_type = type(0)
string_type = type(0)
bool_type = type(True)


def try_to_num(text):
    if str(text).isnumeric():
        return int(str(text))
    elif str(text).count('.') > 0:
        args = str(text).split('.')
        text1 = get_num(args[0])
        text2 = get_num(args[1])
        if str(text1) + '.' + str(text2) == str(text):
            return float(str(text))
    return 'NAN'


def add(text1, text2):
    if str(try_to_num(text1)) == text1 and str(try_to_num(text2)) == text2:
        return try_to_num(text1) + try_to_num(text2)
    elif type(text1) == type(text2):
        return text1 + text2
    elif type(text1) == str:
        return text1 + str(text2)
    elif type(text2) == str:
        return str(text1) + text2


def power(text1, text2):
    if str(text1).isnumeric() and str(text2).isnumeric():
        return math.pow(int(text1), int(text2))
    elif str(text1).isdecimal() or str(text2).isdecimal():
        return math.pow(float(text1), float(text2))
    raise ArithmeticError('Tried to use power operator on a non number value')


def multiply(text1, text2):
    if str(text1).isnumeric() and str(text2).isnumeric():
        return int(text1) * int(text2)
    elif str(text1).isdecimal() or str(text2).isdecimal():
        return float(text1) * float(text2)
    raise ArithmeticError('Tried to use multiplication operator on a non number value: ' + (text1 + "*" + text2))


def divide(text1, text2):
    if str(text1).isnumeric() and str(text2).isnumeric():
        return int(text1) / int(text2)
    elif str(text1).isdecimal() or str(text2).isdecimal():
        return float(text1) / float(text2)
    raise ArithmeticError('Tried to use division operator on a non number value')


def subtract(text1, text2):
    if type(text1) == number_type:
        if type(text2) == number_type:
            return text1 - text2
    elif str(text1).isnumeric():
        if str(text2).isnumeric():
            return int(text1) - int(text2)


def parse_string(text):
    if text.startswith('\'') and text.endswith('\''):
        return replace_last_char(text.replace('\'', '', 1)).replace('\\n', '\n')
    elif text == 'input':
        return input('> ').replace('\\\\', '\\')
    else:
        return "NAS"


def parse_number(text, method_object, markers, variables):
    if text.startswith('-'):
        return -parse_number(text.replace('-', '', 1), method_object, markers, variables)
    if text.isnumeric():
        return int(text)
    elif text.isdecimal():
        return float(text)
    elif text.count('.') > 0:
        args = text.split('.')
        text1 = get_num(args[0])
        text2 = get_num(args[1])
        if str(text1) + '.' + str(text2) == text:
            return float(text)
    # TIME NANO
    elif text == 'time:nano':
        return int(int(time.time_ns()) / 100)
    # idk
    elif text == 'time:thread':
        return int(time.thread_time())
    # idk
    elif text == 'time:thread.nano':
        return int(time.thread_time_ns())
    # idk
    elif text == 'time:process':
        return int(time.process_time())
    # idk
    elif text == 'time:process.nano':
        return int(time.process_time_ns())
    # TIME CLOCK (https://vstinner.github.io/python37-pep-564-nanoseconds.html)
    elif text == 'time:clock':
        return int(time.clock())
    # TIME
    elif text == 'time':
        return int(time.time())
    # idk
    elif text == 'time:monotonic':
        return int(time.monotonic())
    # EXECUTION TIME
    elif text == 'time:execution':
        return int(time.perf_counter())
    # EXECUTION TIME
    elif text == 'time:execution.nano':
        return int(int(time.perf_counter_ns()) / 100)
    # RANDOM
    elif text.startswith('rand='):
        range_vals = text.replace('rand=', '')
        range_list = []
        if text.count('-') >= 1:
            range_list = range_vals.split('-', 1)
        elif text.count(',') >= 1:
            range_list = range_vals.split(',', 1)
        elif text.count(':') >= 1:
            range_list = range_vals.split(':', 1)
        if len(range_list) > 1:
            return random.randrange(
                int(parse_value_full(range_list[0], method_object, markers, variables)),
                int(parse_value_full(range_list[1], method_object, markers, variables)) + 1
            )
        elif len(range_list) == 1:
            return random.randrange(0, int(parse_value_full(range_list[0], method_object, markers, variables)) + 1)
        else:
            print(range_list)
            print(text)
    elif \
            text.count('+') > 0 or \
                    text.count('-') > 0 or \
                    text.count('*') > 0 or \
                    text.count('/') > 0 or \
                    text.count('^') > 0:
        while text.count('^') > 0:
            args = text.split('^', 1)
            text1 = args[0]
            text2 = args[1]
            text1 = text1.replace('-', ' ').replace('+', ' ').replace('*', ' ').replace('^', ' ').replace('/', ' ')
            text2 = text2.replace('-', ' ').replace('+', ' ').replace('*', ' ').replace('^', ' ').replace('/', ' ')
            args = text1.split(' ')
            text1_2 = args[len(args) - 1]
            args = text2.split(' ')
            text2_2 = args[0]
            text1_3 = parse_value_full(text1_2, method_object, markers, variables)
            text2_3 = parse_value_full(text2_2, method_object, markers, variables)
            text = text.replace(str(text1_2) + '^' + str(text2_2), str(power(str(text1_3), str(text2_3))))
        while text.count('*') > 0:
            args = text.split('*', 1)
            text1 = args[0]
            text2 = args[1]
            text1 = text1.replace('-', ' ').replace('+', ' ').replace('*', ' ').replace('/', ' ')
            text2 = text2.replace('-', ' ').replace('+', ' ').replace('*', ' ').replace('/', ' ')
            args = text1.split(' ')
            text1_2 = args[len(args) - 1]
            args = text2.split(' ')
            text2_2 = args[0]
            text1_3 = parse_value_full(text1_2, method_object, markers, variables)
            text2_3 = parse_value_full(text2_2, method_object, markers, variables)
            text = text.replace(str(text1_2) + '*' + str(text2_2), str(multiply(str(text1_3), str(text2_3))))
        while text.count('/') > 0:
            args = text.split('/', 1)
            text1 = args[0]
            text2 = args[1]
            text1 = text1.replace('-', ' ').replace('+', ' ').replace('/', ' ')
            text2 = text2.replace('-', ' ').replace('+', ' ').replace('/', ' ')
            args = text1.split(' ')
            text1_2 = args[len(args) - 1]
            args = text2.split(' ')
            text2_2 = args[0]
            text1_3 = parse_value_full(text1_2, method_object, markers, variables)
            text2_3 = parse_value_full(text2_2, method_object, markers, variables)
            text = text.replace(str(text1_2) + '/' + str(text2_2), str(divide(str(text1_3), str(text2_3))))
        while text.count('+') > 0:
            args = text.split('+', 1)
            text1 = args[0]
            text2 = args[1]
            text1 = text1.replace('-', ' ').replace('+', ' ')
            text2 = text2.replace('-', ' ').replace('+', ' ')
            args = text1.split(' ')
            text1_2 = args[len(args) - 1]
            args = text2.split(' ')
            text2_2 = args[0]
            text1_3 = parse_value_full(text1_2, method_object, markers, variables)
            text2_3 = parse_value_full(text2_2, method_object, markers, variables)
            text = text.replace(str(text1_2) + '+' + str(text2_2), str(add(str(text1_3), str(text2_3))))
        while text.count('-') > 0:
            args = text.split('-', 1)
            text1 = args[0]
            text2 = args[1]
            text1 = text1.replace('-', ' ')
            text2 = text2.replace('-', ' ')
            args = text1.split(' ')
            text1_2 = args[len(args) - 1]
            args = text2.split(' ')
            text2_2 = args[0]
            text1_3 = parse_value_full(text1_2, method_object, markers, variables)
            text2_3 = parse_value_full(text2_2, method_object, markers, variables)
            text = text.replace(str(text1_2) + '-' + str(text2_2), str(subtract(str(text1_3), str(text2_3))))
        return try_to_num(text)
    else:
        return "NAN"
