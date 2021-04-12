"""
开关机操作模块，支持AC、DC、reboot
"""
import logging
import time

from utils import keycontrol, tv_utlils
from task import device as dv


MODE_AC = 'AC'
MODE_DC = 'DC'
_Key = keycontrol.Key

MIN_ON_WAIT = 25
DEFAULT_ON_WAIT = 60
DEFAULT_DC_OFF_WAIT = 20
DEFAULT_AC_OFF_WAIT = 5


class Switch:
    def __init__(self,
                 on2check_interval: (int, float) = DEFAULT_ON_WAIT,
                 dc_off_interval: (int, float) = DEFAULT_DC_OFF_WAIT,
                 mode: str = MODE_DC,
                 reboot: bool = False):
        self.on2check_interval = on2check_interval
        self.dc_off_interval = dc_off_interval
        self.mode = mode
        self.reboot = reboot
        self.device = None

    def set_device(self, device: dv.Device):
        self.device = device

    def on_wait_rest(self):
        """
        开机阶段一般会有两段等待，一段是on_wait（固定等待20s），第二段是调用该方法（根据设置补充剩余的等待时长）
        :return:
        """
        # if self.reboot:
        #     wait = self.on2check_interval
        # else:
        #     wait = self.on2check_interval - MIN_ON_WAIT if self.on2check_interval > MIN_ON_WAIT else 0
        wait = self.on2check_interval - MIN_ON_WAIT if self.on2check_interval > MIN_ON_WAIT else 0
        logging.debug('on_wait_rest {}s'.format(wait))
        time.sleep(wait)

    @staticmethod
    def on_wait():
        """
        静态方法，开机后等待预置的固定时长(20s)
        :return:
        """
        logging.debug('on_wait {}s'.format(MIN_ON_WAIT))
        time.sleep(MIN_ON_WAIT)

    def off_wait(self):
        """
        关机后等待时长，AC的话等待预置的固定时长（5），DC等待时长由传参或者配置文件决定
        :return:
        """
        #wait = DEFAULT_AC_OFF_WAIT if self.mode == MODE_AC else self.dc_off_interval
        wait = self.dc_off_interval
        logging.debug('off_wait {}s'.format(wait))
        time.sleep(wait)

    def switch(self, state: bool, retry=False, times=None):
        """
        开关机操作流程
        :param state:
        :param retry:
        :return:
        """
        if self.device is None:
            raise PermissionError('device is None')
        logging.debug('switch {}{}{}'.format('ON' if state else 'OFF',
                                             ', retry ...' if retry else '', ',times: ' + str(times) if times else ''))
        if self.reboot:
            # reboot 操作
            if state:
                self.device.tv.send_cmd('reboot', timeout=1)
                self.on_wait()
            else:
                time.sleep(2)
            return
        if isinstance(times, int):
            times -= 1
            if times <= 0:
                if self.mode == MODE_AC:
                    raise Exception('AC客观环境存在异常，请检查')
                else:
                    raise Exception('红外客观环境存在异常，请检查')
        if self.mode == MODE_AC:
            # ac操作
            (self.device.mcu.ac_on() if state else self.device.mcu.ac_off())
        else:
            # dc操作
            self.device.mcu.press_ir(_Key.IR_POWER)
        if state:
            # 开机等待
            self.on_wait()
            # 检测是否开机(串口是否可用)，未能开启电视则重试开机
            if not tv_utlils.check_tv_com(self.device.tv_com)[0]:
                if times is None:
                    times = 10
                self.switch(state, True, times)
        else:
            # 关机等待
            self.off_wait()
            # # 检测是否关机(串口是否不可用)，仍然开机则重试开机
            if tv_utlils.check_tv_com(self.device.tv_com)[0]:
                if times is None:
                    times = 10
                self.switch(state, True, times)

    def get_switch_msg(self, state: bool) -> str:
        """
        获取开关机的相关描述
        :param state:
        :return:
        """
        suffix = '开机' if state else '关机'
        if self.reboot:
            msg = 'reboot' + suffix
        elif self.mode == MODE_DC:
            msg = '红外' + suffix
        elif self.mode == MODE_AC:
            msg = 'AC' + suffix
        else:
            msg = suffix
        return msg
