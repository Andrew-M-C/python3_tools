#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# Reference:
#   [如何获取Python中最后一部分路径？](https://codeday.me/bug/20170616/27046.html)

import traceback
# import time
import datetime
# import os
import file
import atexit

_enable_log_func = True
_enable_log_line = True
_enable_log_file = True
_enable_log_statement = False
_log_identifier = ''


LOG_EMERG = 0       # 0: system is unusable
LOG_ALERT = 1       # 1: action must be taken immediately
LOG_CRIT = 2        # 2: critical conditions
LOG_ERROR = 3       # 3: error conditions
LOG_ERR = 3         # 3: error conditions
LOG_WARNING = 4     # 4: warning conditions
LOG_WARN = 4        # 4: warning conditions
LOG_NOTICE = 5      # 5: normal, but significant, condition
LOG_INFO = 6        # 6: informational message
LOG_DEBUG = 7       # 7: debug-level message


console_level = LOG_DEBUG   # 输出到对话的日志级别
file_level = LOG_INFO       # 写入文件的日志级别
should_adjust = False       # 是否应该对齐


_file_part_len_max = 0
_log_file_path = './log.log'

_log_file = None


class _ManualStack():
    '假的 stack，用来自定义函数信息'

    def __init__(self, func='unknown_func', line=-1, file='unknown_file', statement='unknown_caller'):
        self.name = func
        self.filename = file
        self.lineno = line
        self.line = statement
        return

    def set_func(self, func):
        self.name = func
        return

    def set_line(self, line):
        self.lineno = line
        return

    def set_file(self, file):
        self.filename = file
        return

    def set_statement(self, statement):
        self.line = statement
        return


def enable_log_function(flag):
    '启用/禁止在 log 中输入函数名'
    global _enable_log_func
    if flag:
        _enable_log_func = True
    else:
        _enable_log_func = False
    return


def enable_log_line(flag):
    '启用/禁止在 log 中输入行号'
    global _enable_log_line
    global _enable_log_file
    if flag:
        _enable_log_line = True
        _enable_log_file = True
    else:
        _enable_log_line = False
    return


def enable_log_file(flag):
    '启用/禁止在 log 中输入文件名'
    global _enable_log_file
    if flag:
        _enable_log_file = True
    else:
        _enable_log_file = False
    return


def set_log_file_path(path):
    '修改 log 文件名'
    global _log_file_path
    global _log_file
    if path == _log_file_path:
        # log 文件路径不变
        return
    else:
        _log_file_path = path
        if _log_file:
            _log_file.close()
            _log_file = None
    return


def enable_enable_log_statement(flag):
    '启用/禁止在 log 中输出语句信息'
    global _enable_log_statement
    if flag:
        _enable_log_statement = True
    else:
        _enable_log_statement = False
    return


def _pack_msg(level, stack, message):
    '打包组装最终的字符串'
    global _file_part_len_max
    log_parts = []

    # 添加时间信息
    # part = '[%s]' % time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    part = '[%s]' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    log_parts.append(part)

    # 添加文件信息
    if _enable_log_file:
        file_dir_and_name = str(stack.filename).split('/')
        if _enable_log_line:
            part = ' [%s, Line %d' % (file_dir_and_name[-1], stack.lineno)
        else:
            part = ' [%s' % file_dir_and_name[-1]
        # log_parts.append(part)

        if _enable_log_func:
            part += ', %s()]' % stack.name
        else:
            part += ']'

        # 对齐操作
        if should_adjust:
            if len(part) < _file_part_len_max:
                part = part.ljust(_file_part_len_max)
            else:
                # print('%d -> %d' % (_file_part_len_max, len(part)))
                _file_part_len_max = len(part)
        log_parts.append(part)

    elif _enable_log_func:
        part = ' [%s()]' % stack.name
        log_parts.append(part)

    # 添加日志等级
    if LOG_DEBUG == level:
        part = ' [DEBUG]     -'
    elif LOG_INFO == level:
        part = ' [INFO ] (...)'
    elif LOG_NOTICE == level:
        part = ' [NOTCE] (:.:)'
    elif LOG_WARNING == level:
        part = ' [WARN ] (!.!)'
    elif LOG_ERR == level:
        part = ' [ERROR] (!!!)'
    elif LOG_CRIT == level:
        part = ' [CRIT ] (X!!)'
    elif LOG_ALERT == level:
        part = ' [ALERT] (XX!)'
    elif LOG_EMERG == level:
        part = ' [EMERG] (XXX)'
    else:
        part = ' [DEBUG]     -'
    log_parts.append(part)

    # 添加日志正文
    log_parts.append(' - ')

    if len(_log_identifier) > 0:
        log_parts.append('%s: ' % _log_identifier)

    log_parts.append(message)

    # 添加调用语句
    if _enable_log_statement:
        part = ' <caller: "%s">' % stack.line
        log_parts.append(part)

    return ''.join(log_parts)


def _open_enable_log_file_if_needed():
    '有必要的话，打开 log 文件'
    global _log_file
    if _log_file is None:
        file.ensure_dirs_for_path(_log_file_path)
        _log_file = open(_log_file_path, 'a+', encoding='utf-8')
        info('Log file opened. (current file path: %s)' % _log_file_path)
        atexit.register(lambda: _log_file.close())
    return


def log(log_level, msg, stack=None):
    '输出 log'
    if stack is None:
        stack_list = traceback.extract_stack()
        stack = stack_list[-2]

    final_msg = _pack_msg(log_level, stack, msg)
    ret = len(final_msg)

    # 输出到 console
    if log_level <= console_level:
        print(final_msg)

    # 输出到文件
    if log_level <= file_level:
        _open_enable_log_file_if_needed()
        _log_file.write(final_msg)
        _log_file.write('\n')

    # 返回
    return ret


def raw_log(log_level, message, func=None, file=None, line=None, statement=None):
    '输出各部分自定义的 log'
    stack_list = traceback.extract_stack()
    stack = stack_list[-2]
    if func is None:
        func = stack.name
    if file is None:
        file = stack.filename
    if line is None:
        line = stack.lineno
    if statement is None:
        statement = stack.line

    dummy_stack = _ManualStack(func=func, file=file, line=line, statement=statement)
    return log(log_level, message, dummy_stack)


def mark():
    stack = traceback.extract_stack()
    last_stack = stack[-2]
    return log(LOG_DEBUG, '<<< MARK >>>', last_stack)


def debug(msg):
    stack = traceback.extract_stack()
    last_stack = stack[-2]
    return log(LOG_DEBUG, msg, last_stack)


def info(msg):
    stack = traceback.extract_stack()
    last_stack = stack[-2]
    return log(LOG_INFO, msg, last_stack)


def notice(msg):
    stack = traceback.extract_stack()
    last_stack = stack[-2]
    return log(LOG_NOTICE, msg, last_stack)


def warn(msg):
    stack = traceback.extract_stack()
    last_stack = stack[-2]
    return log(LOG_WARN, msg, last_stack)


def error(msg):
    stack = traceback.extract_stack()
    last_stack = stack[-2]
    return log(LOG_ERROR, msg, last_stack)


def critical(msg):
    stack = traceback.extract_stack()
    last_stack = stack[-2]
    return log(LOG_CRIT, msg, last_stack)


def alert(msg):
    stack = traceback.extract_stack()
    last_stack = stack[-2]
    return log(LOG_ALERT, msg, last_stack)


def emerge(msg):
    stack = traceback.extract_stack()
    last_stack = stack[-2]
    return log(LOG_EMERG, msg, last_stack)


def function_name():
    stack = traceback.extract_stack()
    last_stack = stack[-2]
    return last_stack.name


def caller_name():
    stack = traceback.extract_stack()
    last_stack = stack[-3]
    return last_stack.name


def caller_file():
    stack = traceback.extract_stack()
    last_stack = stack[-3]
    return last_stack.filename


def set_log_identifier(id):
    global _log_identifier
    _log_identifier = str(id)
    return
