#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys


def search_file(file_name):
    '通过文件名查找文件 - http://python3-cookbook.readthedocs.io/zh_CN/latest/c13/p09_find_files_by_name.html'
    curr_dir = os.path.abspath(os.curdir)
    for rel_path, dirs, files in os.walk(curr_dir):
        if file_name in files:
            full_path = os.path.join(curr_dir, rel_path, file_name)
            # print file_name, ":", full_path
            return full_path
    raise Exception(str(file_name) + ' not found')
    return None


def read_file(file_path):
    '从指定的文件路径中读取文件内容，并且返回一个 string'
    # print('Request read file:', file_path)

    file = open(file_path)

    total_read = ''
    curr_read = file.read()
    while len(curr_read) > 0:
        total_read = total_read + curr_read
        curr_read = file.read()

    file.close()
    return total_read


def write_file(file_path, string=''):
    '将文件使用指定的字符串填充'
    file = open(file_path, 'w+')
    file.write(string)
    file.close()
    return


def ensure_dirs_for_path(file_path):
    '根据给定的路径，创建该路径下的所有目录层级'
    # reference: [python 中的split()函数和os.path.split()函数](https://blog.csdn.net/sxingming/article/details/51475382)
    if file_path is None:
        return

    dirs, file_name = os.path.split(file_path)
    if len(dirs) == 0 or dirs == '.':
        # 当前目录，直接返回即可
        return
    elif os.path.exists(dirs) is False:
        os.makedirs(dirs)
        return
    return


def system_is_big_endian():
    '判断本机是不是大端系统'
    return True if 'big' == sys.byteorder else False


def system_is_little_endian():
    '判断本机是不是小端系统'
    return not system_is_big_endian()


if __name__ == '__main__':
    # 测试代码
    '''
    test = 'hello'
    dir_name, file_name = os.path.split(test)
    print('result: "%s", "%s"' % (dir_name, file_name))
    '''
    ensure_dirs_for_path('hello')
