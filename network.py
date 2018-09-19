#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import urllib.request
import urllib.parse
import json
import socket

import log
import char

if __name__ == '__main__':
    print('%s is not executable' % sys.argv[0])
    sys.exit(1)


def http_request(url, url_para=None, post_data=None):
    'send HTTP/HTTPS request and get response'
    # parameter check
    # url should be a string
    if isinstance(url, str) is False:
        log.error('"url" parameter should be a string type')
        return None
    # url_para should be dict or None
    if isinstance(url_para, (dict, type(None))) is False:
        log.error('"url_para" parameter shoule be a dictionary type')
        return None
    # post_data could be None, dict, list, string or byte
    if isinstance(post_data, dict):
        post_bytes = json.dumps(post_data, ensure_ascii=False).encode('utf-8')
    elif isinstance(post_data, list):
        post_bytes = json.dumps(post_data, ensure_ascii=False).encode('utf-8')
    elif isinstance(post_data, str):
        post_bytes = post_data.encode('utf-8')
    elif isinstance(post_data, bytes):
        post_bytes = post_data
    elif post_data is None:
        post_bytes = None
    else:
        log.error('"post_data" should be None, dict, list, string or byte')

    if url_para is None or len(url_para) == 0:
        full_url = url
    else:
        full_url = '%s?%s' % (url, urllib.parse.urlencode(url_para))

    request = urllib.request.Request(full_url)
    response = urllib.request.urlopen(request, post_bytes)
    return response.read()


def simple_udp_echo(port, config={}):
    'run a simple UDP echo server which could be terminated by Ctrl+C'
    port = int(port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', port))

    should_show_data = bool(config.get('show_data', False))
    should_show_data_len = bool(config.get('show_data_len', False))
    should_show_client_addr = bool(config.get('show_client', True))
    show_data_len_limit = int(config.get('show_data_len_limit', 1024))

    try:
        while True:
            data, addr = sock.recvfrom(10240)
            if should_show_client_addr:
                log.debug('Got incomming data from %s' % str(addr))
            if should_show_data_len:
                log.debug('Data length: %d' % len(data))
            if should_show_data and len(data) <= show_data_len_limit:
                log.debug(char.dump_bytes(data))

            sock.sendto(data, addr)

    except KeyboardInterrupt as e:
        pass
    else:
        pass
    finally:
        log.debug('server with port %d quit' % port)
        sock.close()
        sock = None
    pass

    return


def simple_udp_send(ip, port, data, limit=10240):
    'send some data to target and then get response'
    ip = str(ip)
    port = int(port)
    limit = int(limit)
    if isinstance(data, bytes) is False:
        return None

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data, (ip, port))
    response, address = sock.recvfrom(limit)

    return response


# debug code
"""
if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(1)
    if sys.argv[1] == 'server':
        config = {}
        config['show_data'] = True
        simple_udp_echo(20000, config)
    elif sys.argv[1] == 'client':
        resp = simple_udp_send('127.0.0.1', 20000, '1234567890123456!12345678901234'.encode('utf-8'))
        log.debug('Got response: %s' % str(resp))
    else:
        sys.exit(1)
"""
