"""
信源煲机场景实现
"""
import logging
import time
from numpy import random

import constant
from constant import get_second
from task import scene as sc, checker as ck, excel as ex, performance as pf, device as dv
from utils import thread_utils, tv_utlils


class ChannelSwitchThread(thread_utils.LoopThread):
    """
    通道切换线程
    """
    def __init__(self, channel_list: list(), interval: int, device: dv.Device, per: pf.Performance):
        super(ChannelSwitchThread, self).__init__()
        self.channel_list = channel_list
        self.interval = interval
        self.device = device
        self.cur_channel = ''
        self.pf = per

    def my_loop(self):
        # 随机设置一个通道
        self._random_channel()
        i = 0
        # 等待
        while self.flag and i < self.interval:
            i += 1
            time.sleep(1)

    def _random_channel(self):
        """
        随机设置一个通道
        :return:
        """
        if len(self.channel_list) <= 0:
            raise AssertionError('null channel_list')
        elif len(self.channel_list) == 1:
            self.cur_channel = self.channel_list[0]
            self._set_channel(self.cur_channel)
            self.pf_set_mode(self.cur_channel)
        else:
            logging.debug('random channel ing...')
            logging.debug(f'list {self.channel_list}')
            while True:
                channel = random.choice(self.channel_list)
                if channel and channel != self.cur_channel:
                    self.cur_channel = channel
                    self._set_channel(channel)
                    self.pf_set_mode(self.cur_channel)
                    return

    def pf_set_mode(self, mode):
        if self.pf is not None:
            self.pf.set_mode(mode)

    def _set_channel(self, channel: str):
        """
        设置通道
        """
        logging.debug('set channel : {}'.format(channel))
        self.device.tv.send_cmd('am broadcast -a com.konka.GO_TO_TV')
        time.sleep(3)
        self.device.tv.send_cmd('am broadcast -a com.konka.tvsettings.action.GO_TO_SOURCEPAGE')
        tv_utlils.set_channel(self.device, channel)


class SceneTV(sc.Scene):
    """
    信源煲机场景实现
    """
    def __init__(self,
                 name: str,
                 exec_time: int,
                 checker: ck.Checker,
                 channel_list: list,
                 performance_str: str,
                 channel_switch_interval: (int, float) = None,
                 performance_interval: (int, float) = None,
                 check_interval: (int, float) = None,
                 by: int = sc.BY_TIME):
        sc.Scene.__init__(self, name=name, exec_time=exec_time, by=by, checker=checker)
        self.channel_list = channel_list
        self.channel_switch_interval = get_second(channel_switch_interval, 'scene_tv', 'channel_switch_interval')
        self.performance_interval = get_second(performance_interval, 'scene_tv', 'performance_interval')
        self.check_interval = get_second(check_interval, 'scene_tv', 'check_interval')
        logging.debug(
            f'by {"按次数" if self.by == sc.BY_COUNT else "按时间"}\n'
            f'channel_switch_interval {self.channel_switch_interval}\n'
            f'performance_interval {self.performance_interval}\n'
            f'check_interval {self.check_interval}\n')
        self.performance_str = performance_str
        self.performance_process = list()
        self._parse_performance_process(self.performance_str)

        self.performance_thread = None
        self.channel_switch_thread = None

        self.save_in_usb = True
        self.dependent.init(
            usb=self.save_in_usb,
        )

    def _parse_performance_process(self, performance_str):
        """
        解析进程文本生成性能检测进程列表
        :param performance_str:
        :return:
        """
        for item in performance_str.split(';'):
            item = item.strip()
            if not item:
                continue
            self.performance_process.append(item)

    def serialize(self):
        ret = {
            'channel_list': self.channel_list,
            'channel_switch_interval': self.channel_switch_interval,
            'performance_interval': self.performance_interval,
            'check_interval': self.check_interval,
            'performance_str': self.performance_str,
        }
        ret.update(self.base_serialize())
        return ret

    @staticmethod
    def deserialize(d: dict) -> 'SceneTV':
        return sc.Scene.base_deserialize(SceneTV, d)

    def _get_config_detail(self):
        second = list()
        second.append('信源:' + '、'.join(self.channel_list))
        second.append('信源切换时间:' + str(constant.second2other(self.channel_switch_interval, constant.HOUR)) + 'H')
        second.append('检测间隔:' + str(constant.second2other(self.check_interval, constant.MINUTE)) + '分钟')
        if self.performance_process:
            second.append('监测进程:' + '、'.join(self.performance_process))
            second.append('性能抓取间隔:' + str(constant.second2other(self.performance_interval, constant.MINUTE)) + '分钟')
        return second

    def init_main_sheet(self):
        second_str = '\n'.join(self._get_config_detail())
        ex.init_main_sheet(self.report, self.name, second_str)

    def work(self):
        if self.device is None:
            return
        self.fd.start_log_single()
        if self.performance_process:
            # 开启性能检测线程
            self.performance_thread = pf.Performance(
                process=self.performance_process,
                interval=self.performance_interval,
                device=self.device,
                fd=self.fd
            )
            self.performance_thread.start()
        # 开启通道切换线程
        self.channel_switch_thread = ChannelSwitchThread(
            self.channel_list,
            self.channel_switch_interval,
            self.device,
            self.performance_thread
        )
        self.channel_switch_thread.start()
        while not self.is_timeout():
            self.wait_timeout_or_interval(self.check_interval)
            # 检测
            summary = self.checker.check(is_on_and_off=False)
            # 更新报告
            self.upgrade_summary(time.time() - self.start_time, summary, record_times=True)
        if self.performance_process:
            # 停止性能检测进程
            self.performance_thread.terminal()
        # 停止通道切换线程
        self.channel_switch_thread.terminal()
        self.fd.stop_log()
