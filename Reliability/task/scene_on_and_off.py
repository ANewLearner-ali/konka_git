"""
开关机检测场景的实现
"""
import logging
import time
import random
import traceback

import constant
from constant import get_second

from task import scene as sc, checker as ck, device as dv, excel as ex, switch as sw, msg_queue as mq
from utils import keycontrol, thread_utils, play_voice, tv_utlils

_Key = keycontrol.Key


class KeySet:
    """
    按键配置类
    """
    def __init__(self,
                 volume: bool = False,
                 channel: bool = False,
                 pad: bool = False,
                 voice: bool = False):
        self.keys = list()
        self.volume = volume
        self.channel = channel
        self.pad = pad
        self.voice = voice
        self.init_keys()

    def get_info(self):
        """
        获取已选的按键信息描述
        :return:
        """
        ret = ['音量+-' if self.volume else '',
               '频道+-' if self.channel else '',
               '五维键' if self.pad else '',
               '语音键' if self.voice else '']
        return '、'.join(filter(lambda x: x != '', ret))

    def init_keys(self):
        """
        根据配置初始化有效按键
        :return:
        """
        self.keys = self.keys + [_Key.IR_VOLUME_UP, _Key.IR_VOLUME_DOWN] if self.volume else self.keys
        self.keys = self.keys + [_Key.IR_CHANNEL_UP, _Key.IR_CHANNEL_DOWN] if self.channel else self.keys
        self.keys = self.keys + [_Key.IR_LEFT, _Key.IR_RIGHT, _Key.IR_UP, _Key.IR_DOWN, _Key.IR_ENTER] if self.pad else self.keys
        self.keys = self.keys + [_Key.BLUE_VOICE] if self.voice else self.keys

    def get_key_random(self) -> _Key:
        """
        随机获取下一个按键
        :return:
        """
        return random.choice(self.keys)

    def serialize(self):
        return {
            'volume': self.volume,
            'channel': self.channel,
            'pad': self.pad,
            'voice': self.voice
        }

    def env_check(self):
        """
        用于一键调试中的按键发送
        :return:
        """
        if self.keys:
            for key in self.keys:
                mq.ck_queue.put((mq.TAG_MSG, '发送' + key.cn_name))
                time.sleep(1)


class KeyThread(thread_utils.LoopThread):
    """
    按键操作线程
    """
    def __init__(self, key_set: KeySet, device: dv.Device):
        thread_utils.LoopThread.__init__(self)
        self.key_set = key_set
        self.device = device

    def my_loop(self):
        try:
            key = random.choice(self.key_set.keys)
            if key.cn_name.startswith('蓝牙'):
                self.device.mcu.press_blue(key)
            else:
                self.device.mcu.press_ir(key)
            time.sleep(random.uniform(1.0, 1.5))
        except:
            self.flag = False
            self.stopped = True
            logging.debug('KeyThread error: {}'.format(traceback.format_exc()))


class FarThread(thread_utils.LoopThread):
    """
    远场音频播放线程
    """
    def __init__(self):
        thread_utils.LoopThread.__init__(self)

    def my_loop(self):
        play_voice.play_normal(constant.WAKE_UP_MP3)
        time.sleep(random.uniform(1.0, 2.0))


class SceneOnAndOff(sc.Scene, sw.Switch):
    """
    开关机检测场景实现
    """
    def __init__(self,
                 name: str,
                 exec_time: int,
                 checker: ck.Checker,
                 key_set: dict,
                 far: bool,
                 mode: str = sw.MODE_DC,
                 on2check_interval: (int, float) = None,
                 dc_off_interval: (int, float) = None,
                 reboot: bool = False,
                 by: int = sc.BY_COUNT,
                 ad_root: str = ''):
        checker.launcher = True
        sc.Scene.__init__(self, name, exec_time, by, checker=checker)
        on2check_interval = get_second(on2check_interval, 'scene_on_and_off', 'on2check_interval')
        dc_off_interval = get_second(dc_off_interval, 'scene_on_and_off', 'dc_off_interval')
        sw.Switch.__init__(self, on2check_interval, dc_off_interval, mode=mode, reboot=reboot)
        self.key_set = KeySet(**key_set)
        self.far = far
        self.ad_root = ad_root.strip()
        # 修改日志到U盘
        self.save_in_usb = False
        self.dependent.init(
            usb=self.save_in_usb,
        )
        if not reboot or self.key_set.keys:
            self.dependent.muc = True

    def serialize(self):
        ret = {
            'key_set': self.key_set.serialize(),
            'far': self.far,
            'mode': self.mode,
            'on2check_interval': self.on2check_interval,
            'dc_off_interval': self.dc_off_interval,
            'reboot': self.reboot,
            'ad_root': self.ad_root
        }
        logging.warning(f'ret {ret}')
        ret.update(self.base_serialize())
        return ret

    @staticmethod
    def deserialize(d) -> 'SceneOnAndOff':
        return sc.Scene.base_deserialize(SceneOnAndOff, d)

    def _get_config_detail(self) -> list:
        second = list()
        second.append('模式:' + self.mode)
        if self.ad_root:
            second.append('替换开机广告:' + self.ad_root)
        if self.key_set:
            second.append('开机按键屏蔽' + '(' + self.key_set.get_info() + ')')
        if self.far:
            second.append('远场唤醒')
        return second

    def init_main_sheet(self):
        second_str = '\n'.join(self._get_config_detail())
        ex.init_main_sheet(self.report, self.name, second_str)

    def base_env_check_body(self):
        """
        自定义一键调试
        :return:
        """
        ir_interval = get_second(None, "scene_on_and_off", "ir_interval")
        bt_interval = get_second(None, "scene_on_and_off", "bt_interval")
        if self.key_set.keys:
            for key in self.key_set.keys:
                mq.ck_queue.put((mq.TAG_MSG, '发送' + key.cn_name))
                if key == _Key.BLUE_VOICE:
                    self.device.mcu.press_blue(key, mode=keycontrol.MODE_LONG_PRESS)
                    time.sleep(bt_interval)
                else:
                    self.device.mcu.press_ir(key)
                    time.sleep(ir_interval)
        if self.far:
            mq.ck_queue.put((mq.TAG_MSG, '播放小康音频'))
            play_voice.play_normal(constant.WAKE_UP_MP3)
        mq.ck_queue.put((mq.TAG_MSG, self.get_switch_msg(False)))
        self.switch(False)
        mq.ck_queue.put((mq.TAG_MSG, self.get_switch_msg(True)))
        self.switch(True)
        mq.ck_queue.put((mq.TAG_MSG, '等待开机完成...'))
        self.on_wait_rest()
        return True

    def work(self):
        """
        工作流程
        :return:
        """
        if self.device is None:
            return
        while not self.is_timeout():
            try:
                # 关机
                self.switch(False)
                if len(self.key_set.keys) > 0:
                    # 开启按键操作线程
                    key_thread = KeyThread(self.key_set, self.device)
                    key_thread.start()
                if self.far:
                    # 开启远场语音播放线程
                    far_thread = FarThread()
                    far_thread.start()
                # 开机
                self.switch(True)

                # 抓log
                self.fd.start_log(
                    i=self.cur_count,
                    logcat=True,
                    kernel=True,
                    blue=True,
                    wifi=self.checker.wifi
                )
                # 等待
                self.on_wait_rest()
            except:
                logging.debug('SceneOnAndOff work faction has enter the exception handing flow')
                if len(self.key_set.keys) > 0:
                    # 停止按键线程
                    key_thread.terminal()
                    logging.debug('key_thread had done terminal!')
                if self.far:
                    # 停止远场音频播放线程
                    far_thread.terminal()
                    logging.debug('far_thread had done terminal!')
                raise
            logging.debug('SceneOnAndOff enter the normal process...')
            if len(self.key_set.keys) > 0:
                # 停止按键线程
                key_thread.terminal()
                logging.debug('SceneOnAndOff stop key_thread')
            if self.far:
                # 停止远场音频播放线程
                far_thread.terminal()
                logging.debug('SceneOnAndOff stop far_thread')
            summary = self.checker.check(self.cur_count, prev='hdmi')
            result = summary[1]
            if self.ad_root:
                # 替换开机广告
                tv_utlils.replace_ad(self.device, self.ad_root, self.cur_count)
            # 更新报告
            self.upgrade_summary(self.cur_count, summary, record_times=True)
            # 停止log
            self.fd.stop_log()
            # 结果检测，如果全部检测项都成功的话就删除log和图片
            result = [result[b][1] for b in result if isinstance(result[b][1], bool)]
            if all(result):
                self.fd.remove_log_pic(self.cur_count, prev='hdmi')
            else:
                self.fd.mv_log_pic(self.cur_count, prev='hdmi')
                # 增加需求：如果有检测不通过就拷贝anr和tombstones文件夹
                self.fd.cp_traces_tomb(self.cur_count, remove=True)
                # 增加需求：如果有检测不通过拷贝bluedroid和bluetooth文件夹
                self.fd.cp_bluetooth(self.cur_count, remove=True)
            self.special_for_dc_error()

    def special_for_dc_error(self):
        self.device.tv.send_cmd('logcat -v time > /data/misc/konka/dc_error.log &')