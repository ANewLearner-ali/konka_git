"""
PC和TV两端的文件和文件夹处理器，包括log、图片、报告等
"""

import logging
import os

import time

import constant
from task import device as dv, excel as ex, logger
from utils import time_utils, tv_utlils, file_utils, capture_utils


class FD:
    def __init__(self, name: str = '', device: dv.Device = None, create_time: str = None):
        self.name = name
        self.device = device
        self.create_time = time_utils.datetime_string(time_utils.TYPE1) if create_time is None else create_time
        self.logger = None
        self._gn_name = ''
        self._root_prefix = ''
        self.root_pc = ''
        self.root_tv = ''
        self.excel = ''
        self.p_excel = ''
        self.cur_scene_name = ''
        self.cur_scene_root_tv = ''
        self.cur_scene_log = ''
        self.cur_scene_pic = ''
        self.monkey_error = ''
        # 一个用于表示U盘的本次报告的目录
        # case: H:\reliability\com6__20210312193226\9652-开关机压测50秒
        self.cur_scene_usb_root = ''

    def init(self, device: dv.Device):
        """
        初始化设备和log处理器
        :param device:
        :return:
        """
        self.device = self.device if device is None else device
        self.logger = logger.Logger(self.device, self.create_time)

    def create_root(self):
        """
        创建任务的测试报告目录
        :return:
        """
        self._gn_name = self.name + '_' + self.create_time
        self._root_prefix = self.device.tv_com + '_'
        self.root_pc = os.path.join(constant.REPORTS_ROOT, self._root_prefix + self._gn_name)
        file_utils.mkdir(self.root_pc)
        self.root_tv = constant.REPORTS_ROOT_TV + '/' + self._root_prefix + self._gn_name
        tv_utlils.mkdir(self.device, constant.REPORTS_ROOT_TV)
        tv_utlils.mkdir(self.device, self.root_tv)

    def create_excel(self):
        """
        创建excel测试报告
        :return:
        """
        self.excel = os.path.join(self.root_pc, self._gn_name + '.xlsx')
        ex.create_report(self.excel)
        return self.excel

    def p_create_excel(self, processes: list):
        """
        创建性能检测的excel测试报告
        :param processes:
        :return:
        """
        self.p_excel = os.path.join(self.root_pc, self._gn_name + '_pf.xlsx')
        ex.p_create_report(self.p_excel, processes)
        return self.excel

    def p_append(self, info: dict):
        ex.p_append(self.p_excel, info)

    def create_scene_root(self, name, save_in_usb: bool):
        """
        创建当前场景的目录结构
        :param name:
        :param save_in_usb:
        :return:
        """
        if save_in_usb:
            usb_root = tv_utlils.is_any_usb_mounted(self.device, return_device=True)
            logging.debug(f'create_scene_root usb root : {usb_root}')
            tool_root = usb_root + '/' + constant.REPORTS_ROOT_TV_DIR_NAME
            self.root_tv = tool_root + '/' + self._root_prefix + self._gn_name
            tv_utlils.mkdir(self.device, tool_root)
            tv_utlils.mkdir(self.device, self.root_tv)
        else:
            # 用于创建U盘目录，尝试本地保存后备份到U盘
            usb_root = tv_utlils.is_any_usb_mounted(self.device, return_device=True)
            logging.debug(f'create_scene_root usb root : {usb_root}')
            tool_root = usb_root + '/' + constant.REPORTS_ROOT_TV_DIR_NAME
            cur_scene_root_tv = tool_root + '/' + self._root_prefix + self._gn_name
            self.cur_scene_usb_root = cur_scene_root_tv + '/' + name
            cur_scene_log = self.cur_scene_usb_root + '/' + 'logs'
            cur_scene_pic = self.cur_scene_usb_root + '/' + 'pics'
            tv_utlils.mkdir(self.device, tool_root)
            tv_utlils.mkdir(self.device, cur_scene_root_tv)
            tv_utlils.mkdir(self.device, self.cur_scene_usb_root)
            tv_utlils.mkdir(self.device, cur_scene_log)
            tv_utlils.mkdir(self.device, cur_scene_pic)
        self.cur_scene_name = name
        self.cur_scene_root_tv = self.root_tv + '/' + self.cur_scene_name
        self.cur_scene_log = self.cur_scene_root_tv + '/' + 'logs'
        self.cur_scene_pic = self.cur_scene_root_tv + '/' + 'pics'
        self.monkey_error = self.cur_scene_log + '/monkey_error.txt'
        tv_utlils.mkdir(self.device, self.cur_scene_root_tv)
        tv_utlils.mkdir(self.device, self.cur_scene_log)
        tv_utlils.mkdir(self.device, self.cur_scene_pic)

    def start_log_single(self, logcat: bool = True, kernel: bool = False, blue: bool = False):
        """
        开启抓log，一般用于一个场景只要抓一份log的情况
        :param logcat:
        :param kernel:
        :param blue:
        :return:
        """
        tv_utlils.init_tv_env(self.device)
        if logcat:
            self.logger.start_logcat(self.cur_scene_log + '/' + 'log_' +
                                     str(time_utils.datetime_stamp(time_utils.TYPE1, self.create_time)) + '.txt')
        if kernel:
            self.logger.start_kmsg(self.cur_scene_log + '/' + 'kmsg_' +
                                   str(time_utils.datetime_stamp(time_utils.TYPE1, self.create_time)) + '.txt')
        if blue:
            ...

    def start_log(self, i, logcat: bool = True, kernel: bool = False, blue: bool = False, wifi: bool = False):
        """
        开启抓log，一般用于一个场景中需要抓多份log的情况，如开关机测试
        :param i:
        :param logcat:
        :param kernel:
        :param blue:
        :return:
        """
        tv_utlils.init_tv_env(self.device, wifi)
        if logcat:
            self.logger.start_logcat(self.cur_scene_log + '/' + 'log_第' + str(i) + '次' + '.txt')
        if kernel:
            self.logger.start_kmsg(self.cur_scene_log + '/' + 'kmsg_第' + str(i) + '次' + '.txt')
        if blue:
            ...
        if wifi:
            # self.logger.start_kmsg(self.cur_scene_log + '/' + 'kmsg_第' + str(i) + '次' + '.txt')
            ...

    def stop_log(self, pid: list = None):
        """
        停止log
        :param pid:
        :return:
        """
        if pid is None or isinstance(pid, list):
            self.logger.stop_all_log(pid)
        else:
            self.logger.stop_log(pid)

    def shot(self, i: int = None, is_tv_source=False, prev=''):
        """
        电视截图
        :param i:
        :param is_tv_source:
        :param prev:
        :return:
        """
        if i is None:
            save_path = self.cur_scene_pic + '/' + prev + str(int(time.time())) + '.png'
        else:
            save_path = self.cur_scene_pic + '/' + prev + '_第' + str(i) + '次' + '.png'
        tv_utlils.shot(com=self.device, save_path=save_path, is_tv_source=is_tv_source)

    def camera_shot(self, i: int = None, prev=''):
        """
        PC端的摄像头拍摄图片
        :param i:
        :param prev:
        :return:
        """
        if i is None:
            save_path = os.path.join(self.root_pc,  prev + str(int(time.time())) + '.jpg')
        else:
            save_path = os.path.join(self.root_pc, prev + '_第' + str(i) + '次' + '.jpg')
        ret = capture_utils.capture_shot(save_path)
        logging.debug(f'camera_shot result : {ret}')

    def remove_log_pic(self, i: int, prev=''):
        """
        删除log和图片，用于开关机测试中全部检测项都通过的情况下，不需要保留log和图片
        :param i:
        :param prev:
        :return:
        """
        log = self.cur_scene_log + '/' + 'log_第' + str(i) + '次.txt'
        kmsg = self.cur_scene_log + '/' + 'kmsg_第' + str(i) + '次.txt'
        pic = self.cur_scene_pic + '/' + prev + '_第' + str(i) + '次.png'
        tv_utlils.rm(self.device, log)
        tv_utlils.rm(self.device, kmsg)
        tv_utlils.rm(self.device, pic)

    def mv_log_pic(self, i: int, prev=''):
        """
        剪切log和图片，用于开关机测试中全部检测项都通过的情况下，不需要保留log和图片
        :param i:
        :param prev:
        :return:
        """
        log = self.cur_scene_log + '/' + 'log_第' + str(i) + '次.txt'
        kmsg = self.cur_scene_log + '/' + 'kmsg_第' + str(i) + '次.txt'
        pic = self.cur_scene_pic + '/' + prev + '_第' + str(i) + '次.png'
        tv_utlils.mv_log(self.device, log, self.cur_scene_usb_root + '/logs')
        tv_utlils.mv_log(self.device, kmsg, self.cur_scene_usb_root + '/logs')
        tv_utlils.mv_log(self.device, pic, self.cur_scene_usb_root + '/pics')

    def cp_traces_tomb(self, i: int, remove: bool):
        des_dir = self.cur_scene_usb_root if self.cur_scene_usb_root else self.cur_scene_log
        anr_file_dir = des_dir + '/' + 'a第' + str(i) + '次_anr'
        tomb_file_dir = des_dir + '/' + 'a第' + str(i) + '次_tombstones'
        tv_utlils.copy_traces(self.device, anr_file_dir, is_rm=remove)
        tv_utlils.copy_tombstones(self.device, tomb_file_dir, is_rm=remove)

    def cp_bluetooth(self, i: int, remove: bool):
        des_dir = self.cur_scene_usb_root if self.cur_scene_usb_root else self.cur_scene_log
        bluetooth_file_dif = (des_dir + '/' + 'a第' + str(i) + '次_bluetooth')
        bluedroid_file_dir = (des_dir + '/' + 'a第' + str(i) + '次_bluedroid')
        tv_utlils.copy_bluetooth(self.device, bluetooth_file_dif, is_rm=remove)
        tv_utlils.copy_bluedroid(self.device, bluedroid_file_dir, is_rm=remove)

    def optimize(self):
        ex.optimize(self.excel)
