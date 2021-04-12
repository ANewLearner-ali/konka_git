"""
TV端log处理器
"""
from task import device as dv
from utils import time_utils, tv_utlils

MODE_SINGLE = 1
MODE_MULTI = 2


class Logger:
    def __init__(self, device: dv.Device = None, create_time: str = None, mode: int = MODE_SINGLE):
        self.device = device
        self.create_time = time_utils.datetime_string(time_utils.TYPE1) if create_time is None else create_time
        self.mode = mode
        self.pid = []

    def start_logcat(self, file):
        """
        开启抓log
        :param file:
        :return:
        """
        self.pid.append(tv_utlils.start_logcat(self.device, file))

    def start_kmsg(self, file):
        """
        开启抓kernel log
        :param file:
        :return:
        """
        self.pid.append(tv_utlils.start_kmsg(self.device, file))

    def stop_log(self, pid: str):
        """
        停止指定pid的log进程
        :param pid:
        :return:
        """
        pid = pid.strip()
        if not pid:
            tv_utlils.device_send(self.device, 'kill ' + pid)

    def stop_all_log(self, pid: list = None):
        """
        停止所有log进程
        :param pid:
        :return:
        """
        pid = self.pid if pid is None else pid
        if not pid:
            return
        while pid:
            tv_utlils.device_send(self.device, 'kill ' + str(pid.pop()))

    def shot(self, file):
        """
        电视截图
        :param file:
        :return:
        """
        tv_utlils.shot(self.device, file)

    def cp_anr(self, file_dir, is_rm=True):
        """
         拷贝anr文件夹
        :param file_dir:
        :param is_rm: 拷贝后是否删除
        :return:
        """
        tv_utlils.copy_traces(self.device, file_dir, is_rm=is_rm)

    def cp_tombstones(self, file_dir, is_rm=True):
        """
        拷贝tombstones文件夹
        :param file_dir:
        :param is_rm:
        :return:
        """
        tv_utlils.copy_tombstones(self.device, file_dir, is_rm=is_rm)


