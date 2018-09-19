#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# Reference:
#   [如何获取Python中最后一部分路径？](https://codeday.me/bug/20170616/27046.html)
#   [atexit — 程式關閉時回呼 — 你所不知道的 Python 標準函式庫用法 08](https://blog.louie.lu/2017/08/03/你所不知道的-python-標準函式庫用法-08-atexit/)

import traceback
import log
import atexit
import socket
import json
import sys

if __name__ == '__main__':
    print('%s is not executable' % sys.argv[0])
    sys.exit(1)


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


_VAR_RUN_PATH = '/data'
_UNILOG_DIR_NAME = 'pyunilog'
_UDP_FILE_NAME = 'port.txt'


_identifier = 'unknown device'
_log_server_port = 0
_log_socket = None
_log_level = LOG_INFO


def _exit_log_socket():
    global _log_socket, _log_server_port

    if _log_socket:
        _log_socket.close()
        _log_socket = None

    _log_server_port = 0
    log.info('unilog client exited')
    return


def _send_to_log_server(json_obj):
    global _log_server_port, _log_socket

    if 0 == _log_server_port or _log_socket is None:
        # 初始化 log UDP
        port_file_path = '%s/%s/%s' % (_VAR_RUN_PATH, _UNILOG_DIR_NAME, _UDP_FILE_NAME)
        port = 0
        with open(port_file_path) as port_file:
            port_str = port_file.read()
            port = int(port_str)
        if port:
            _log_server_port = port
            _log_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            log.info('unilog client started')
            atexit.register(lambda: _exit_log_socket())

    _log_socket.sendto(json.dumps(json_obj).encode(), ('localhost', _log_server_port))
    return


def _log(level, caller_stack, msg):
    if level > _log_level:
        return

    json_obj = {}
    json_obj['file'] = str(caller_stack.filename).split('/')[-1]
    json_obj['line'] = int(caller_stack.lineno)
    json_obj['func'] = str(caller_stack.name)
    json_obj['log'] = '%s: %s' % (_identifier, str(msg).replace('\n', ' '))
    json_obj['level'] = int(level) if (int(level) <= LOG_DEBUG and int(level) >= 0) else LOG_DEBUG
    _send_to_log_server(json_obj)

    log.raw_log(level, 'UNILOG: ' + msg, func=caller_stack.name, file=caller_stack.filename, line=caller_stack.lineno, statement=caller_stack.line)
    return


def _get_caller_stack():
    stack_list = traceback.extract_stack()
    stack = stack_list[-3]
    return stack


def emerg(msg):
    'system is unusable'
    return _log(LOG_EMERG, _get_caller_stack(), msg)


def alert(msg):
    'action must be taken immediately'
    return _log(LOG_ALERT, _get_caller_stack(), msg)


def crit(msg):
    'critical conditions'
    return _log(LOG_CRIT, _get_caller_stack(), msg)


def error(msg):
    'error conditions'
    return _log(LOG_ERROR, _get_caller_stack(), msg)


def warning(msg):
    'warning conditions'
    return _log(LOG_WARN, _get_caller_stack(), msg)


def notice(msg):
    'normal, but significant, condition'
    return _log(LOG_NOTICE, _get_caller_stack(), msg)


def info(msg):
    'informational message'
    return _log(LOG_INFO, _get_caller_stack(), msg)


def debug(msg):
    'debug-level message'
    return _log(LOG_DEBUG, _get_caller_stack(), msg)


def unilog(log_level, msg):
    if log_level > LOG_DEBUG:
        log_level = LOG_DEBUG
    return _log(log_level, _get_caller_stack(), msg)


def set_identifier(guid):
    global _identifier
    _identifier = str(guid)
    return


def set_log_level(log_level):
    log_level = int(log_level)
    if log_level > LOG_DEBUG:
        log_level = LOG_DEBUG
    if log_level < 0:
        log_level = 0

    global _log_level
    _log_level = log_level
    return


def get_log_level():
    return _log_level
