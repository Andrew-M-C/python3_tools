#!/usr/bin/python3
# -*- coding: UTF-8 -*-
#
# 最简单的方法就是使用 psutil，但是这个需要额外安装。本文件使用 /proc/stat 来计算 CPU使用率
# Reference:
#     - [系统性能信息模块psutil](https://www.jianshu.com/p/50de2235a35d)
#     - [几种Python执行时间的计算方法](https://blog.csdn.net/wangshuang1631/article/details/54286551)

import time


def _debug(msg):
    # print('[opsys] %s' % msg)
    return


class CpuUsage:
    '统计 CPU　使用率'

    def __init__(self):
        self.latest_calc_time = self._read_clock()
        self.latest_cpu_stat = self._read_cpu_stat()
        self.last_calc_time = self.latest_calc_time
        self.last_cpu_stat = self.latest_cpu_stat
        _debug('Init CPU stat: %s' % self.last_cpu_stat)
        return

    def _read_cpu_stat(self):
        cpu_stat = []

        # read stat file content
        stat_file_lines = []
        with open('/proc/stat') as f:
            while True:
                line = f.readline()
                if line:
                    stat_file_lines.append(line)
                else:
                    break

        # translate file lines
        for index in range(len(stat_file_lines)):
            line = stat_file_lines[index]
            if line.startswith('cpu'):
                parts = line.split()
                cpu = {}
                cpu['user'] = int(parts[1])
                cpu['nice'] = int(parts[2])
                cpu['system'] = int(parts[3])
                cpu['idle'] = int(parts[4])
                cpu['iowait'] = int(parts[5])
                cpu['irq'] = int(parts[6])
                cpu['softirq'] = int(parts[7])
                cpu_stat.append(cpu)
            else:
                break
        return cpu_stat

    def _read_clock(self):
        uptime_secs = 0.0
        with open('/proc/uptime') as f:
            line = f.readline()
            # _debug('Uptime: %s' % line.split())
            uptime_secs = float(line.split()[0])
        return uptime_secs

    def aging(self):
        '上一次计算 CPU 距现在的时间'
        curr = self._read_clock()
        ret = curr - self.latest_calc_time
        _debug('aging: %f' % ret)
        return ret

    def update(self):
        '计算一次 CPU 使用率'
        self.last_calc_time = self.latest_calc_time
        self.last_cpu_stat = self.latest_cpu_stat
        self.latest_calc_time = self._read_clock()
        self.latest_cpu_stat = self._read_cpu_stat()
        return

    def cpu_time(self, cpu_num=-1):
        '返回各个 CPU 的状态，参数默认 -1 表示返回所有 CPU 状态和'
        cpu_num = int(cpu_num)
        if cpu_num < 0:
            cpu_num = -1
        cpu_num += 1

        if cpu_num >= len(self.latest_cpu_stat):
            # 不合法的 CPU 号
            return {}

        _debug('self.latest_cpu_stat[%d]: %s' % (cpu_num, str(self.latest_cpu_stat[cpu_num])))
        time_intvl = self.latest_calc_time - self.last_calc_time
        this_stat = self.latest_cpu_stat[cpu_num]
        last_stat = self.last_cpu_stat[cpu_num]

        ret_stat = {}
        for key in this_stat:
            ret_stat[key] = this_stat[key] - last_stat[key]

        return ret_stat

    def cpu_usage(self):
        '简易地计算 CPU 使用率'
        cpu_time = self.cpu_time()
        cpu_idle = cpu_time['idle']
        cpu_total = 0
        for key in cpu_time:
            cpu_total += cpu_time[key]

        if cpu_total == 0:
            return 0.0
        else:
            return 1.0 - cpu_idle / cpu_total
