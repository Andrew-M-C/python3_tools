#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys

_UINT8_TO_CHAR = [
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.',
    ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?',
    '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
    'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_',
    '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', '.',
]

if __name__ == '__main__':
    print('%s does not provide main()' % __file__)
    sys.exit(1)


def _hex_str(byte):
    return '%02X' % (int(byte) & 0xFF)


def _hex_char(byte):
    byte = int(byte) & 0xFF
    if byte > 0x7F:
        return '.'
    else:
        return _UINT8_TO_CHAR[byte]


def dump_bytes(data):
    'dump data in a readable string table'
    if isinstance(data, bytes) is False:
        return ''

    lines = []
    data_len = len(data)
    lines.append('data length %d' % data_len)
    lines.append(
        '------      0  1  2  3  4  5  6  7  | 8  9  A  B  C  D  E  F      01234567 89ABCDEF')

    for index in range(0, data_len, 16):
        remain_len = data_len - index
        if remain_len >= 16:
            string = '0x%04X      %s %s %s %s %s %s %s %s | %s %s %s %s %s %s %s %s     %s%s%s%s%s%s%s%s %s%s%s%s%s%s%s%s' % (
                    index,
                    _hex_str(data[index + 0]), _hex_str(data[index + 1]), _hex_str(data[index + 2]), _hex_str(data[index + 3]),
                    _hex_str(data[index + 4]), _hex_str(data[index + 5]), _hex_str(data[index + 6]), _hex_str(data[index + 7]),
                    _hex_str(data[index + 8]), _hex_str(data[index + 9]), _hex_str(data[index + 10]), _hex_str(data[index + 11]),
                    _hex_str(data[index + 12]), _hex_str(data[index + 13]), _hex_str(data[index + 14]), _hex_str(data[index + 15]),
                    _hex_char(data[index + 0]), _hex_char(data[index + 1]), _hex_char(data[index + 2]), _hex_char(data[index + 3]),
                    _hex_char(data[index + 4]), _hex_char(data[index + 5]), _hex_char(data[index + 6]), _hex_char(data[index + 7]),
                    _hex_char(data[index + 8]), _hex_char(data[index + 9]), _hex_char(data[index + 10]), _hex_char(data[index + 11]),
                    _hex_char(data[index + 12]), _hex_char(data[index + 13]), _hex_char(data[index + 14]), _hex_char(data[index + 15]),
                )
            lines.append(string)
        else:
            this_line = []
            this_line.append('0x%04X      ' % index)
            for col in range(index, data_len):
                this_line.append('%s ' % _hex_str(data[col]))
            if remain_len > 8:
                this_line.insert(9, '| ')
                this_line.append('   ' * (16 - remain_len))
            else:
                this_line.append('   ' * (16 - remain_len))
                this_line.append('  ')
            print('remain_len = %d' % remain_len)
            # this_line.append('    ')

            this_line.append('    ')
            for col in range(index, data_len):
                this_line.append(_hex_char(data[col]))
                if col == index + 7:
                    this_line.append(' ')

            lines.append(''.join(this_line))

    return '\n'.join(lines)
