import random

import time

from python import method_loader
from python.errors import *


def run(method_object):
    method = method_object.list
    line = 0
    last_line = 0
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
        line = run_line(method, line, method_object)
    if line > len(list(method)):
        raise BadGoToError(
            "Execution of method "
            + str(method_object.name)
            + " stopped at line "
            + str(line)
            + " comming from line "
            + str(last_line)
            + " when said method only goes up to line "
            + str(len(list(method)))
        )


def run_line(method, line, method_object):
    # print(line)
    func = str(trim_line(str(method[line])))
    # REWIND
    if func.startswith('goBack:'):
        return line - handle_goto(func.replace('goBack:', ''))
    # REWIND
    elif func.startswith('rewind:'):
        return line - handle_goto(func.replace('rewind:', ''))
    # SKIP
    elif func.startswith('skip:'):
        return line + handle_goto(func.replace('skip:', ''))
    # SKIP
    elif func.startswith('goForward:'):
        return line + handle_goto(func.replace('goForward:', ''))
    # GOTO
    elif func.startswith('goTo:'):
        return handle_goto(func.replace('goTo:', ''))
    # GOTO
    elif func.startswith('goto:'):
        return handle_goto(func.replace('goto:', ''))
    # SAY
    elif func.startswith('say:\''):
        print(func.replace("say:'", "", 1).replace('\'', '', 1))
        return line + 1
    # SAY
    elif func.startswith('sayAndParse:'):
        print(parse_value(func.replace("sayAndParse:", "", 1)))
        return line + 1
    # REWIND IF CONDITION IS FALSE
    elif func.startswith('ifNotRewind>'):
        num = get_num(func.replace("ifNotRewind>", "", 1))
        if not parse_whole_condition(func.replace("ifNotRewind>", "", 1).replace(str(num) + ":", '', 1)):
            return line - num
    # SKIP IF CONDITION IS FALSE
    elif func.startswith('ifNotSkip>'):
        num = get_num(func.replace("ifNotSkip>", "", 1))
        if not parse_whole_condition(func.replace("ifNotSkip>", "", 1).replace(str(num) + ":", '', 1)):
            return line + num
    # REWIND IF CONDITION IS TRUE
    elif func.startswith('ifRewind>'):
        num = get_num(func.replace("ifRewind>", "", 1))
        if parse_whole_condition(func.replace("ifRewind>", "", 1).replace(str(num) + ":", '', 1)):
            return line - num
    # GOTO IF CONDITION IS TRUE
    elif func.startswith('ifGoto>'):
        num = get_num(func.replace("ifGoto>", "", 1))
        if parse_whole_condition(func.replace("ifGoto>", "", 1).replace(str(num) + ":", '', 1)):
            return num
    # GOTO IF CONDITION IS FALSE
    elif func.startswith('ifNotGoto>'):
        num = get_num(func.replace("ifNotGoto>", "", 1))
        if not parse_whole_condition(func.replace("ifNotGoto>", "", 1).replace(str(num) + ":", '', 1)):
            return num
    # SKIP IF CONDITION IS TRUE
    elif func.startswith('ifSkip>'):
        num = get_num(func.replace("ifSkip>", "", 1))
        if parse_whole_condition(func.replace("ifSkip>", "", 1).replace(str(num) + ":", '', 1)):
            return line + num
    # WAIT
    elif func.startswith('wait:'):
        time.sleep(int(parse_value(func.replace('wait:', "")) / 1000))
    # WAIT
    elif func.startswith('sleep:'):
        time.sleep(int(parse_value(func.replace('sleep:', "")) / 1000))
    # WAIT SECONDS
    elif func.startswith('waitSeconds:'):
        time.sleep(int(parse_value(func.replace('waitSeconds:', ""))))
    # WAIT SECONDS
    elif func.startswith('sleepSeconds:'):
        time.sleep(int(parse_value(func.replace('sleepSeconds:', ""))))
    # TODO:Call another file based on the text in a variable
    # CALL ANOTHER FILE
    elif func.startswith('call:'):
        method_loader.load_or_get(func.replace('call:', '')).execute()
    # PRINT EXECUTING FILE
    elif func.startswith('currentFile'):
        print("Current file: "+str(method_object.name))
    # EXIT
    elif func.startswith('exit'):
        if func.count(':') >= 1:
            raise SystemExit(get_num(func.replace('exit:', '')))
        else:
            raise SystemExit(0)
    return line + 1


def trim_line(line):
    return line.lstrip()


def handle_goto(text):
    if text.isnumeric():
        return int(text)
    else:
        return int(parse_value(text))


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


def parse_whole_condition(condition):
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
                val = val and parse_condition(condition_val)
            elif operator == '&&':
                operator = ''
                val = val or parse_condition(condition_val)
            else:
                val = parse_condition(condition_val)
        if type(val) == bool_type:
            return val
    raise RuntimeError("Tried to parse boolean out of text " + str(condition))


def parse_condition(condition):
    value = False
    # TRUE
    if condition == 'true' or condition == '!true':
        value = True
    # FALSE
    elif condition == 'false' or condition == '!false':
        value = False
    # RANDOM
    elif str(condition).replace('!', '') == 'random' or str(condition).replace('!', '') == 'rand':
        value = random.randrange(0, 2) == 1
    # NOT
    if str(condition).startswith('!'):
        return not value
    # NORMAL
    else:
        return value


def parse_value(text):
    try:
        return parse_number(text)
    except:
        try:
            return parse_whole_condition(text)
        except:
            return text


number_type = type(0)
string_type = type(0)
bool_type = type(True)


def add(text1, text2):
    if type(text1) == type(text2):
        return text1 + text2
    if type(text1) == str:
        return text1 + str(text2)
    if type(text2) == str:
        return str(text1) + text2


def subtract(text1, text2):
    if type(text1) == number_type:
        if type(text2) == number_type:
            return text1 - text2
    if str(text1).isnumeric():
        if str(text2).isnumeric():
            return int(text1) - int(text2)


def parse_number(text):
    if text.isnumeric():
        return int(text)
    # TIME NANO
    elif text == 'time:nano':
        return int(int(time.time_ns())/100)
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
        return int(int(time.perf_counter_ns())/100)
    # RANDOM
    elif text.startswith('rand='):
        range_vals = text.replace('rand=', '')
        range_list = []
        if text.count('-') >= 1:
            range_list = range_vals.split('-', 1)
        elif text.count(',') >= 1:
            range_list = range_vals.split(',', 1)
        if len(range_list) > 1:
            return random.randrange(int(range_list[0]), int(range_list[1]) + 1)
        else:
            return random.randrange(0, int(range_list[0]) + 1)
    else:
        raise RuntimeError("Tried to parse number out of text " + str(text))
