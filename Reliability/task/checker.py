"""
检查器，通用的检测模块
"""
import logging
import time
import constant

from utils import tv_utlils, play_voice, keycontrol, capture_utils
from task import device as dv, i_serializable as i_s, dependent as dp, fd


class Checker(i_s.ISerializable):
    def __init__(self,
                 launcher: bool = False,
                 net: bool = False,
                 wifi: bool = False,
                 wifi_driver: bool = False,
                 usb: bool = False,
                 hdmi: bool = False,
                 camera: bool = False,
                 near: bool = False,
                 far: bool = False,
                 blue_controller: bool = False,
                 blue_speaker: bool = False,
                 window_assert: bool = False,
                 power_on: bool = False,
                 power_off: bool = False,
                 sub_screen: bool = False,
                 install_apk: bool = False,
                 check_apk: bool = False,
                 usb_count: int = 1,
                 a2dp_mac: str = '',
                 apk_root: str = None,
                 bt_ct_mac: str = ''
                 ):
        self.launcher = launcher
        self.net = net
        self.wifi = wifi
        self.wifi_driver = wifi_driver
        self.usb = usb
        self.hdmi = hdmi
        self.camera = camera
        self.near = near
        self.far = far
        self.blue_controller = blue_controller
        self.blue_speaker = blue_speaker
        self.window_assert = window_assert
        self.power_on = power_on
        self.power_off = power_off
        self.sub_screen = sub_screen
        self.install_apk = install_apk
        self.check_apk = check_apk
        self.usb_count = usb_count
        self.bt_ct_mac = bt_ct_mac
        self.a2dp_mac = a2dp_mac
        self.apk_root = apk_root

        self.device: dv.Device = None
        self.fd: fd.FD = None
        self.result = dict()
        self.summary = dict()
        self.count = 0
        self.window = None

    def serialize(self):
        return {'launcher': self.launcher,
                'net': self.net,
                'wifi': self.wifi,
                'wifi_driver': self.wifi_driver,
                'usb': self.usb,
                'hdmi': self.hdmi,
                'camera': self.camera,
                'near': self.near,
                'far': self.far,
                'blue_controller': self.blue_controller,
                'blue_speaker': self.blue_speaker,
                'window_assert': self.window_assert,
                'power_on': self.power_on,
                'power_off': self.power_off,
                'sub_screen': self.sub_screen,
                'install_apk': self.install_apk,
                'check_apk': self.check_apk,
                'usb_count': self.usb_count,
                'a2dp_mac': self.a2dp_mac,
                'apk_root': self.apk_root,
                'bt_ct_mac': self.bt_ct_mac
                }

    @staticmethod
    def deserialize(d: dict) -> 'Checker':
        return Checker(**d)

    def get_detail(self, indentation: str = '    ') -> list:
        """
        获取检测项的文本描述
        :param indentation:
        :return:
        """
        entries = {
            "launcher": 'Launcher',
            "net": '网络',
            "wifi": 'WIFI',
            "wifi_driver": 'WIFI驱动',
            "usb": 'U盘',
            "hdmi": 'HDMI',
            "camera": '摄像头',
            "near": '近场语音',
            "far": '远场语音',
            "blue_controller": '蓝牙遥控器',
            "blue_speaker": '蓝牙音箱/耳机',
            'window_assert': '界面检测',
            'install_apk': '批量安装apk',
            'check_apk': '检测第三方应用'
        }
        ret = list()
        ret.append('检测内容:')
        for key in entries.keys():
            if getattr(self, key, False):
                ret.append(indentation + entries[key])
        return ret

    def setup(self, device: dv.Device, fd_: fd.FD):
        """
        初始化设备和文件处理器
        :param device:
        :param fd_:
        :return:
        """
        self.device = device
        self.fd = fd_

    def check(self, count=None, prev='hdmi', third_apks=None, is_on_and_off=True):
        """
        检测各个需要的检测项并返回检测结果统计
        """
        logging.debug(f'checking ...')
        self.result = dict()
        if self.device is None:
            raise PermissionError('device is not Initialized')
        if not tv_utlils.check_tv_com(self.device):
            raise PermissionError('tv serial can not connect')
        if is_on_and_off:
            tv_utlils.init_tv_env(self.device)
        if self.window_assert:
            self.result['window_assert'] = 'window检测', tv_utlils.is_window_shown(self.device.tv_com, self.window)
        if self.launcher:
            self.device.tv.send_cmd('input keyevent 3')
            time.sleep(5)
            is_launcher_show = tv_utlils.is_window_shown(self.device.tv_com, 'com.konka.livelauncher/com.konka.livelauncher.Launcher') or tv_utlils.is_window_shown(self.device.tv_com, 'com.konka.livelauncher/com.konka.livelauncher.TrueLauncher')
            self.result['launcher'] = 'launcher显示正常', is_launcher_show
        if self.net:
            self.result['net'] = '电视网络正常', tv_utlils.get_tv_ip(self.device).count('.') == 3
        if self.wifi:
            self.result['wifi'] = 'wifi连接正常', tv_utlils.get_wlan0_ip(self.device).count('.') == 3
        if self.wifi_driver:
            self.result['wifi_driver'] = 'wifi驱动正常', tv_utlils.get_wifi_driver_state(self.device)
        if self.usb:
            self.result['usb'] = 'usb挂载正常', tv_utlils.is_usb_mounted(self.device, self.usb_count)
        if self.hdmi:
            tv_utlils.set_channel(self.device, tv_utlils.HDMI1)
            time.sleep(1)
            self.fd.shot(count, prev=prev)
            self.result['hdmi'] = 'hdmi播放正常', self.fd.cur_scene_pic
        if self.camera:
            tv_utlils.start_ai(self.device, wait=25)
            self.fd.shot(count, prev='ai_camera')
            self.result['camera'] = '摄像头正常', self.fd.cur_scene_pic
        if self.near:
            self.device.mcu.press_blue(keycontrol.Key.BLUE_VOICE)
            self.result['near'] = '近场语音唤醒', tv_utlils.is_voice_window_show(self.device)
        if self.far:
            tv_utlils.close_voice_window(self.device)
            play_voice.play_normal(constant.WAKE_UP_MP3)
            self.result['far'] = '远场语音唤醒', tv_utlils.is_voice_window_show(self.device)
        if self.blue_controller:
            self.result['blue_controller'] = '遥控器连接正常', tv_utlils.bt_ct_state(self.device)
        if self.blue_speaker:
            self.result['blue_speaker'] = '蓝牙音箱连接正常', tv_utlils.bt_a2dp_state(self.device)
        if self.check_apk:
            s1 = set(third_apks)
            s2 = set(tv_utlils.third_apks(self.device))
            logging.debug(f's1 apk_list : {s1}')
            logging.debug(f's2 apk_list : {s2}')
            s3 = s1 & s2
            self.result['install_apk'] = '第三方应用存在', s3 == s1
        if self.sub_screen:
            self.fd.camera_shot(count, 'sub_screen_')
            self.result['sub_screen'] = '副屏正常', self.fd.root_pc
        logging.warning(f'check result {self.result}')
        return self._summary()

    def check_ext(self, result):
        """
        拓展的检测，主要根据外部传进来的结果，做结果汇总
        :param result:
        :return:
        """
        logging.debug(f'check_ext, input result: {result}')
        self.result = result
        return self._summary()

    def _summary(self):
        """
        根据检测结果，生成统计结果
        :return:
        """
        self.count += 1
        result = self.result.copy()
        for key, value in self.result.items():
            if isinstance(value[1], bool):
                pass_count = self.summary[key][2] if self.summary.get(key, None) else 0
                pass_count = pass_count + (1 if value[1] else 0)
                self.summary[key] = value[0], round(pass_count / self.count, 2), pass_count
            else:
                self.summary[key] = value[0], value[1], self.count
        logging.debug(f'_summary result {self.summary}')
        return self.summary, result

    def generate_dependent(self) -> dp.Dependent:
        """
        根据检测项，生成需要的环境依赖对象
        :return:
        """
        # if self.near or self.blue_controller:
        # if self.near:
        #     return dp.Dependent(muc=True)

        return dp.Dependent(muc=self.near, bt_ct=self.blue_controller, bt_a2dp=self.blue_speaker)

    def set_window(self, window: str):
        """
        设置当前需要检测的window
        :param window:
        :return:
        """
        logging.debug(f'set_window {window}')
        self.window = window


if __name__ == '__main__':
    from utils import shellcmd
    com = 'com32'
    c = Checker(
        launcher = True,
        net = True,
        wifi = True,
        usb = True,
        hdmi = True,
        camera = True,
        near = False,
        far = True,
        blue_controller = True,
        blue_speaker = True
    )
    c.device = dv.Device(com)
    c.check()
    shellcmd.close_kk_serial(com)
