#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import io


def set_stdout_encoding(encoding_str):
    'Set encoding of console'
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=encoding_str)
    return


def get_stdout_encoding():
    'Get encoding of console'
    return sys.stdout.encoding


if __name__ == '__main__':
    print('%s does not provide main()' % __file__)
    sys.exit(1)
