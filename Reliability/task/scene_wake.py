"""
待机唤醒相关场景实现
"""
import logging
import time
import constant
from constant import get_second

from task import scene as sc, excel as ex, checker as ck, dc_wake as dk, msg_queue as mq
from utils import play_voice, tv_utlils


DEFAULT_DC_OFF_TIMEOUT = 60
DEFAULT_WAKE_UP_TIMEOUT = 80
DEFAULT_WAKE_UP_QUICK_TIMEOUT = 10

MODE_NORMAL = dk.MODE_NORMAL
MODE_AI = dk.MODE_AI
MODE_QUICK = dk.MODE_QUICK


class SceneDCWake(sc.Scene):
    """
    待机唤醒相关场景实现
    """
    def __init__(self,
                 name: str,
                 exec_time: int,
                 checker: ck.Checker,
                 mode: int,
                 low_power_mode: bool = False,
                 dc_off_tag: str = '',
                 dc_off_timeout: (int, float) = None,
                 wake_up_timeout: (int, float) = None,
                 by: int = sc.BY_COUNT):
        sc.Scene.__init__(self, name=name, exec_time=exec_time, by=by, checker=checker)
        self.mode = mode
        self.low_power_mode = low_power_mode
        self.dc_off_tag = dc_off_tag
        self.dc_off_timeout = get_second(dc_off_timeout, 'scene_wake', 'dc_off_timeout')
        if self.mode == dk.MODE_NORMAL:
            self.wake_up_timeout = get_second(wake_up_timeout, 'scene_wake', 'wake_up_timeout')
        else:
            self.wake_up_timeout = get_second(wake_up_timeout, 'scene_wake', 'wake_up_timeout_quick')
        self.dk = None

        self.save_in_usb = True
        self.dependent.init(
            usb=self.save_in_usb,
        )

    def serialize(self):
        ret = {
            'mode': self.mode,
            'dc_off_tag': self.dc_off_tag,
            'dc_off_timeout': self.dc_off_timeout,
            'wake_up_timeout': self.wake_up_timeout,
            'low_power_mode': self.low_power_mode
        }
        ret.update(self.base_serialize())
        return ret

    @staticmethod
    def deserialize(d: dict) -> 'SceneDCWake':
        return sc.Scene.base_deserialize(SceneDCWake, d)

    def _get_config_detail(self):
        second = list()
        if self.low_power_mode:
            second.append('低功耗模式')
        return second

    def init_main_sheet(self):
        second_str = '\n'.join(self._get_config_detail())
        ex.init_main_sheet(self.report, self.name, second_str)

    def base_env_check_body(self):
        """
        自定义一键检测
        :return:
        """
        if not super().base_env_check_body():
            return False
        tmp_dk = dk.DCWake(self.device, self.mode, self.dc_off_timeout, self.wake_up_timeout, self.dc_off_tag)
        mq.ck_queue.put((mq.TAG_MSG, '开始待机'))
        off = tmp_dk.dc_off()
        if not off:
            mq.ck_queue.put((mq.TAG_EXCEPTION, '待机失败'))
        mq.ck_queue.put((mq.TAG_MSG, '开始唤醒'))
        if self.mode in [MODE_NORMAL, MODE_AI]:
            play_voice.play(constant.WAKE_UP_MP3, play_voice.PlayMode.NORMAL)
            # for _ in range(3):
            #     play_voice.play(constant.WAKE_UP_MP3, play_voice.PlayMode.NORMAL)
        else:
            tv_utlils.input_android_key(self.device, 26)
        mq.ck_queue.put((mq.TAG_MSG, '等待唤醒'))
        on = tmp_dk.wait_to_wakeup()
        on_msg = '唤醒成功' if on else '唤醒失败，但是不算检测失败，请手动唤醒再开始测试'
        mq.ck_queue.put((mq.TAG_MSG, on_msg))
        return True

    def work(self):
        if self.device is None:
            return
        self.fd.start_log_single()
        # 创建开机唤醒场景的具体处理器
        self.dk = dk.DCWake(self.device, self.mode, self.dc_off_timeout, self.wake_up_timeout, self.dc_off_tag)
        # 初始化网络，使其有网，挂载上wifi和有线模块
        tv_utlils.set_eth(self.device, True)
        tv_utlils.set_wlan(self.device, True)
        state = True
        while not self.is_timeout():
            result = {'on': ('唤醒成功', False), 'off': ('待机成功', False)}
            if self.dk.is_wakeup():
                tv_utlils.go_to_tv(self.device)
                time.sleep(5)
                # 关机，并获取状态
                off = self.dk.dc_off()
                result['off'] = '待机成功', off
            if self.mode in [MODE_NORMAL, MODE_AI]:
                # 语音唤醒
                play_voice.play(constant.WAKE_UP_MP3, play_voice.PlayMode.NORMAL)
                # for _ in range(3):
                #     play_voice.play(constant.WAKE_UP_MP3, play_voice.PlayMode.NORMAL)
            else:
                tv_utlils.input_android_key(self.device, 26)
            # 唤醒，并获取状态
            on = self.dk.wait_to_wakeup()
            result['on'] = '唤醒成功', on
            logging.debug(f'result : {result}')
            # 调用拓展检测方法，即不做实际检测，而是把已有的result当做检测结果
            summary = self.checker.check_ext(result)
            # 更新报告
            self.upgrade_summary(self.cur_count, summary, record_times=True)
            # 500次就交替模拟断网和联网操作
            if self.cur_count % 500:
                state = not state
                state_info = 'ON' if state else 'OFF'
                logging.debug(f'set net state : {state_info}')
                # 交替挂载和卸载有线和wifi，模拟断网和联网操作
                tv_utlils.set_eth(self.device, state)
                tv_utlils.set_wlan(self.device, state)
            if not on:
                tv_utlils.input_android_key(self.device, 26)
                time.sleep(5)
        self.fd.stop_log()
        # 测试结束，确保网络恢复
        tv_utlils.set_eth(self.device, True)
        tv_utlils.set_wlan(self.device, True)
