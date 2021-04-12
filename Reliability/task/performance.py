"""
性能数据检测模块
"""
import logging
import threading
import re
import time

from task import device as dv, fd as fdt
from utils import tv_utlils


SYSTEM_TAG = '系统占用'
DEFAULT_CPU = 'None'
DEFAULT_MEM = 'None'
DEFAULT_PID = 'None'


class Performance(threading.Thread):
    def __init__(self,
                 process: list,
                 interval: int,
                 fd: fdt.FD,
                 cpu: bool = True,
                 mem: bool = True,
                 device: dv.Device = None):
        super(Performance, self).__init__(daemon=True)
        self.process = process
        self.interval = interval
        self.fd = fd
        self.cpu = cpu
        self.mem = mem
        self.device = device
        self.flag = True
        self.process = [SYSTEM_TAG] + self.process
        self.p_report = self.fd.p_create_excel(self.process)
        self.mode = ''

    def set_mode(self, mode: str):
        """
        设置当前模式（其实就是设置当前是哪个通道或者是app）
        :param mode:
        :return:
        """
        self.mode = mode

    def set_device(self, device: dv.Device):
        self.device = device

    def run(self):
        """
        模块执行
        :return:
        """
        logging.debug('Performance Start')
        while self.flag:
            i = 0
            while i < self.interval and self.flag:
                i += 1
                time.sleep(1)
            tv_time = tv_utlils.tv_datetime(self.device)
            if self.flag:
                # 获取cpu数据
                cpu = self._cpu()
                # 获取内存数据
                mem, pid = self._mem()
                # 定义一行测试数据所需的字段
                info = {
                    'tv_time': tv_time,
                    'mode': self.mode,
                }
                pf = list()
                # 根据监测进程顺序依次获取内存和cup数据
                for process in self.process:
                    p = pid.get(process, DEFAULT_PID)
                    m = mem.get(process, DEFAULT_MEM)
                    c = cpu.get(process, DEFAULT_CPU)
                    pf.append((p, m, c))
                # 数据添加到info中
                info['pf'] = pf
                # 追加数据到报告中
                self.fd.p_append(info)
        logging.debug('Performance Finish')

    def terminal(self, join: bool = True):
        """
        停止性能测试
        :param join:
        :return:
        """
        self.flag = False
        if join:
            self.join()

    def _cpu(self) -> dict:
        """
        cpu数据获取
        :return:
        """
        cpu_str = self.device.tv.send_cmd_get_result('busybox top -bn1')
        ret = {process: DEFAULT_CPU for process in self.process}
        flag = True
        for line in cpu_str.split('\r\n'):
            line = line.strip()
            if not line:
                continue
            columns = re.split(r'\s+', line)
            if flag:
                if line.startswith('CPU:'):
                    ret[SYSTEM_TAG] = str(round(100.0 - float(line.split('nic ')[-1].split('% idle')[0]), 2)) + '%'
                if columns[0] == 'PID':
                    flag = False
                continue
            if columns[-1] in ret:
                if '.' not in columns[6]:
                    ret[columns[-1]] = columns[7]
                elif '.' not in columns[7]:
                    ret[columns[-1]] = columns[8]
        logging.debug('cpu:')
        for key, value in ret.items():
            logging.debug('{}   {} %'.format(key, value))
        return ret

    def _mem(self) -> (dict, dict):
        """
        内存数据获取
        :return:
        """
        ret = {process: DEFAULT_MEM for process in self.process}
        pid_ret = {process: DEFAULT_PID for process in self.process}
        ret[SYSTEM_TAG] = tv_utlils.dump_mem_info(self.device)['used ram'] + 'K'
        pid_ret[SYSTEM_TAG] = 'None'
        mem_str = self.device.tv.send_cmd_get_result('procrank')
        start, col_count = False, None
        for line in mem_str.split('\r\n'):
            line = line.strip()
            if not line:
                continue
            columns = re.split(r'\s+', line)
            if len(columns) > 1 and columns[0] == 'PID':
                start = True
                col_count = len(columns)
                continue
            if not start:
                continue
            if len(columns) != col_count:
                break
            if columns[-1] in ret:
                ret[columns[-1]] = columns[4]
                pid_ret[columns[-1]] = columns[0]

        logging.debug('pid, mem_name， mem:')
        for key, value in ret.items():
            logging.debug('{}  {}   {}'.format(pid_ret[key], key, value))
        return ret, pid_ret


if __name__ == '__main__':
    from task.fd import FD
    from task.device import Device
    from utils import shellcmd, log
    log.init_logging()
    devices = Device('com20', '')
    com = 'com20'
    d = dv.Device(com)
    fd = FD("PID_test", devices, '20200523')
    fd.create_root()
    excel = fd.create_excel()
    print(fd.excel)
    p = Performance(
        process=['com.konka.applist', 'com.konka.systemadvert'],
        interval=5,
        device=d,
        fd=fd
    )
    p.start()
    time.sleep(60)
    p.terminal()
    shellcmd.close_kk_serial(com)
