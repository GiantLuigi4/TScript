import random

import time

from python import method_loader
from python.errors import *


def run(method_object):
    method = method_object.list
    line = 0
    last_line = 0
    labels = {}
    variables = {}
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
    if len(func) == 0:
        return line + 1
    # NOTIFY
    if func.startswith("notify:"):
        func = func.replace("notify:", '', 1)
        print("Hit line " + str(line) + " in method " + str(method_object.name) + ".")
    if func.startswith('m:'):
        math(func.replace('m:', '', 1), method_object, markers, variables)
    # REWIND
    elif func.startswith('goBack:'):
        return line - handle_goto(func.replace('goBack:', ''), method_object, markers, variables)
    # REWIND
    elif func.startswith('rewind:'):
        return line - handle_goto(func.replace('rewind:', ''), method_object, markers, variables)
    # SKIP
    elif func.startswith('skip:'):
        return line + handle_goto(func.replace('skip:', ''), method_object, markers, variables)
    # SKIP
    elif func.startswith('goForward:'):
        return line + handle_goto(func.replace('goForward:', ''), method_object, markers, variables)
    # GOTO
    elif func.startswith('goTo:'):
        return handle_goto(func.replace('goTo:', ''), method_object, markers, variables)
    # GOTO
    elif func.startswith('goto:'):
        return handle_goto(func.replace('goto:', ''), method_object, markers, variables)
    # SAY
    elif func.startswith('say:\''):
        print(func.replace("say:'", "", 1).replace('\'', '', 1))
        return line + 1
    # SAY NO RETURN
    elif func.startswith('saynl:\''):
        print(func.replace("saynl:'", "", 1).replace('\'', '', 1), end='')
        return line + 1
    # SAY VALUE
    elif func.startswith('sayAndParse:'):
        print(parse_value_full(func.replace("sayAndParse:", "", 1), method_object, markers, variables))
        return line + 1
    # SAY VALUE NO RETURN
    elif func.startswith('sayAndParsenl:'):
        print(parse_value_full(func.replace("sayAndParsenl:", "", 1), method_object, markers, variables), end='')
        return line + 1
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
        if parse_whole_condition(func.replace("ifNotGotoMarker>", "", 1).replace(str(mark) + ":", '', 1), method_object,
                                 markers, variables):
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
    # WAIT
    elif func.startswith('wait:'):
        time.sleep(int(parse_value(func.replace('sleep:', ""), method_object, markers, variables) / 1000))
    # SLEEP (more precise version of wait)
    elif func.startswith('sleep:'):
        time.sleep(int(parse_value(func.replace('sleep:', ""), method_object, markers, variables) / 1000))
    # WAIT SECONDS
    elif func.startswith('waitSeconds:'):
        time.sleep(int(parse_value(func.replace('waitSeconds:', ""), method_object, markers, variables)))
    # WAIT SECONDS
    elif func.startswith('sleepSeconds:'):
        time.sleep(int(parse_value(func.replace('sleepSeconds:', ""), method_object, markers, variables)))
    # TODO:Call another file based on the text in a variable
    # CALL ANOTHER FILE
    elif func.startswith('call:'):
        method_loader.load_or_get(func.replace('call:', '')).execute()
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
    # GOTO END OF SCRIPT
    elif func.startswith("gotoEnd"):
        return "end"
    # GOTO END OF SCRIPT
    elif func.startswith("goToEnd"):
        return "end"
    # MARK
    elif func.startswith("mark:"):
        marked_label = markers.get(func.replace("mark:", '', 1), "N\\A")
        if marked_label != "N\\A":
            raise DoubledMarker("Doubled marker on line " + str(line) + " of method " + str(method_object.name))
        markers.update({func.replace("mark:", '', 1): line + 1})
    # DEFINE A VARIABLE
    elif func.startswith("def:"):
        var = variables.get(func.replace("def:", '', 1), "N\\A")
        if var != "N\\A":
            raise DoubledVariable("Doubled variable on line " + str(line) + " of method " + str(method_object.name))
        name = func.replace("def:", '', 1).split(',')[0]
        if name.startswith('%'):
            name = "%" + str(
                parse_value_full(func.replace("def:", '', 1).split(',')[0].replace("%", "", 1), method_object,
                                 markers, variables))
            if str(name) == 'False':
                name = func.replace("def:", '', 1).split(',')[0]
        variables.update(
            {name: parse_value_full(func.replace('def:', '', 1).split(',')[1],
                                    method_object, markers, variables)})
    # DEFINE A VARIABLE
    elif func.startswith("define:"):
        var = variables.get(func.replace("define:", '', 1), "N\\A")
        if var != "N\\A":
            raise DoubledVariable("Doubled variable on line " + str(line) + " of method " + str(method_object.name))
        variables.update(
            {func.replace("define:", '', 1).split(',')[0]: parse_value_full(
                func.replace('define:', '', 1).split(',')[1], method_object, markers, variables)})
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
    elif func.startswith("gotoMark:"):
        marked_label = markers.get(func.replace("gotoMark:", '', 1), "N\\A")
        if marked_label != "N\\A":
            return marked_label
        else:
            return find_marker(func.replace("gotoMark:", '', 1), method, line, method_object.name)
    # GOTO A MARKER
    elif func.startswith("goToMark:"):
        marked_label = markers.get(func.replace("goToMark:", '', 1), "N\\A")
        if marked_label != "N\\A":
            return marked_label
        else:
            return find_marker(func.replace("goToMark:", '', 1), method, line, method_object.name)
    # ADD 1 TO A VARIABLE
    elif func.endswith('++'):
        var = variables.get(func.replace("++", '', 1), "N\\A")
        if var != "N\\A" and str(var).isnumeric():
            name = func.replace('++', '', 1)
            variables[name] = int(variables[name]) + 1
    # SUBTRACT 1 FROM A VARIABLE
    elif func.endswith('--'):
        var = variables.get(func.replace("--", '', 1), "N\\A")
        if var != "N\\A" and str(var).isnumeric():
            name = func.replace('--', '', 1)
            variables[name] = int(variables[name]) - 1
    return line + 1


def get_variable_name(text, variables):
    if text.startswith('%'):
        text = '%'+variables[text.replace('%', '', 1)]
    return text


def math(text, method_object, markers, variables):
    if text.count('=') >= 1:
        args = text.split('=')
        variables[get_variable_name(args[0], variables)] = parse_value_full(args[1], method_object, markers, variables)
    elif text.count('+') >= 1:
        args = text.split('+')
        arg1 = variables[get_variable_name(args[0], variables)]
        if str(arg1).isdecimal():
            arg1 = float(arg1)
            variables[get_variable_name(args[0], variables)] = arg1 + parse_value_full(args[1], method_object, markers,
                                                                                       variables)
        elif str(arg1).isnumeric():
            arg1 = int(arg1)
            variables[get_variable_name(args[0], variables)] = arg1 + parse_value_full(args[1], method_object, markers,
                                                                                       variables)
        else:
            variables[get_variable_name(args[0], variables)] = arg1 + str(parse_value_full(args[1], method_object,
                                                                                           markers, variables))
    elif text.count('-') >= 1:
        args = text.split('-')
        arg1 = variables[args[0]]
        if str(arg1).isdecimal():
            arg1 = float(arg1)
        elif str(arg1).isnumeric():
            arg1 = int(arg1)
        variables[args[0]] = arg1 - parse_value_full(args[1], method_object, markers, variables)
    elif text.count('*') >= 1:
        args = text.split('*')
        arg1 = variables[args[0]]
        if str(arg1).isdecimal():
            arg1 = float(arg1)
        elif str(arg1).isnumeric():
            arg1 = int(arg1)
        variables[args[0]] = arg1 * parse_value_full(args[1], method_object, markers, variables)
    elif text.count('/') >= 1:
        args = text.split('/')
        arg1 = variables[args[0]]
        if str(arg1).isdecimal():
            arg1 = float(arg1)
        elif str(arg1).isnumeric():
            arg1 = int(arg1)
        variables[args[0]] = arg1 / parse_value_full(args[1], method_object, markers, variables)


def find_marker(name, method, line_num, method_name):
    i = 0
    for line in method:
        if line.startswith('notify:'):
            line = line.replace('notify:', '', 1)
        if line.startswith("mark:") and line.replace('mark:', '', 1) == name:
            return i + 1
        i = i + 1
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
                operator = '||'
            elif condition_val == 'and' or condition_val == '&&':
                operator = '&&'
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


def get_var(name, method_object):
    return method_object.variables.get(name, "N\\A")


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
        return int(parse_value_full(condition_split[0], method_object, markers, variables
                                    )) == int(parse_value_full(condition_split[1], method_object, markers, variables))
    if condition.count('!=') >= 1:
        condition_split = condition.split('!=', 1)
        return int(parse_value_full(condition_split[0], method_object, markers, variables
                                    )) != int(parse_value_full(condition_split[1], method_object, markers, variables))
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
        var = variables.get(line, "N\\A")
        if var != "N\\A":
            return str(var)
    val = get_var(text, method_object)
    if val != "N\\A":
        return val
    else:
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


def add(text1, text2):
    if type(text1) == type(text2):
        return text1 + text2
    elif type(text1) == str:
        return text1 + str(text2)
    elif type(text2) == str:
        return str(text1) + text2


def subtract(text1, text2):
    if type(text1) == number_type:
        if type(text2) == number_type:
            return text1 - text2
    elif str(text1).isnumeric():
        if str(text2).isnumeric():
            return int(text1) - int(text2)


def parse_string(text):
    if text.startswith('\'') and text.endswith('\''):
        return replace_last_char(text.replace('\'', '', 1))
    else:
        return "NAS"


def parse_number(text, method_object, markers, variables):
    if text.isnumeric():
        return int(text)
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
    else:
        return "NAN"
