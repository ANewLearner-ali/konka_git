"""
开机唤醒场景的具体处理模块
"""
import logging
import time
import constant

from task import scene as sc, excel as ex, checker as ck, device as dv
from utils import tv_utlils,  kkserial, play_voice


MODE_NORMAL = 1
MODE_AI = 2
MODE_QUICK = 3

DC_WAKEUP_WAIT = 30


class DCWake:
    def __init__(self, device: dv.Device, mode: int, dc_off_timeout: (int, float), wakeup_timeout: (int, float),
                 dc_tag: str = ''):
        self.device = device
        self.dc_off_timeout = dc_off_timeout
        self.wakeup_timeout = wakeup_timeout
        self.dc_tag = dc_tag
        if mode not in [MODE_NORMAL, MODE_AI, MODE_QUICK]:
            raise ValueError('mode not in [MODE_NORMAL, MODE_AI, MODE_QUICK]')
        self.mode = mode

    def dc_off(self, count=3):
        """
        关机
        :param count:
        :return:
        """
        if count < 0:
            logging.warning('unable dc off, how to do ???')
            return False
        if self.is_wakeup():
            if self._dc_off():
                return True
        count -= 1
        return self.dc_off(count)

    def wait_to_wakeup(self):
        """
        等待唤醒并返回实际的唤醒结果
        :return:
        """
        start = time.time()
        if self.mode == MODE_NORMAL:
            self.wakeup_timeout = DC_WAKEUP_WAIT + 5 if self.wakeup_timeout <= DC_WAKEUP_WAIT else self.wakeup_timeout
            time.sleep(DC_WAKEUP_WAIT)
            cmd = 'dumpsys window|grep mFocusedWindow=.*com.konka.livelauncher.Launcher'
            while time.time() - start < self.wakeup_timeout:
                time.sleep(1)
                self.device.tv.send_cmd('input keyevent 4;input keyevent 3')
                time.sleep(2)
                if self.device.tv.send_cmd_get_result(cmd):
                    return True
        elif self.mode == MODE_AI:
            cmd = 'dumpsys window|grep "mFocusedWindow=.*com.konka.SmartControl}"'
            i = 0
            while i < 3:
                if self.device.tv.send_cmd_get_result(cmd):
                    play_voice.play(constant.TURN_ON, play_voice.PlayMode.NORMAL)
                    time.sleep(3)
                    return self.is_wakeup()
                time.sleep(1)
                i += 1
        else:
            while time.time() - start < self.wakeup_timeout:
                time.sleep(1)
                if self.is_wakeup():
                    return True
        return False

    def is_wakeup(self):
        """
        判断是否已唤醒
        :return:
        """
        fun = {
            MODE_NORMAL: self._is_wakeup_normal,
            MODE_QUICK: self._is_wakeup_quick,
            MODE_AI: self._is_wakeup_ai
        }
        return fun[self.mode]()

    def _dc_off_normal(self):
        serial = kkserial.KKSerialFactory.get_kk_serial(self.device.tv_com)
        serial.clear_cache()
        time.sleep(10)
        start = time.time()
        while time.time() - start < self.dc_off_timeout:
            time.sleep(1)
            if self.dc_tag.encode() in serial.cache:
                logging.debug('cache found tag {}'.format(self.dc_tag))
                return True
        logging.debug('dc off timeout, how to do ???')
        return False

    def _dc_off_quick(self):
        return True

    def _dc_off_ai(self):
        i = 0
        ret, cmd = False, 'dumpsys window |grep "mFocusedWindow=.*com.konka.speakermode.SpeakerModelActivity"'
        while i < 10:
            if tv_utlils.device_send_r(self.device, cmd):
                time.sleep(10 - i)
                return True
            i += 1
            time.sleep(1)
        return False

    def _dc_off(self):
        self.device.tv.send_cmd('input keyevent 26')
        fun = {
            MODE_NORMAL: self._dc_off_normal,
            MODE_QUICK: self._dc_off_quick,
            MODE_AI: self._dc_off_ai
        }
        return fun[self.mode]()

    def _is_dc_off(self):
        return not self._is_wakeup_normal()

    def _is_dc_off_ai(self):
        if not tv_utlils.check_tv_com(self.device.tv_com)[0]:
            raise AssertionError('tv serial closed, is tv real power down ??? how to do ???')
        cmd = 'getprop sys.konka.lowpower.enable'
        if self.device.tv.send_cmd_get_result(cmd) == 'true':
            return True
        return False

    def _is_dc_off_quick(self):
        if not tv_utlils.check_tv_com(self.device.tv_com)[0]:
            raise AssertionError('tv serial closed, is tv real power down ??? how to do ???')
        cmd = 'dumpsys window |grep "Window #.*com.konka.quickstandby/com.konka.quickstandby.MainActivity}:"'
        if self.device.tv.send_cmd_get_result(cmd):
            return True
        return False

    def _is_wakeup_normal(self):
        return tv_utlils.check_tv_com(self.device.tv_com)[0]

    def _is_wakeup_quick(self):
        return not self._is_dc_off_quick()

    def _is_wakeup_ai(self):
        return not self._is_dc_off_ai()
