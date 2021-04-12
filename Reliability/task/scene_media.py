"""
视频类压测场景
"""
import logging
import random
import time
import constant

from constant import get_second
from task import scene as sc, excel as ex, checker as ck, performance as pf, device as dv, msg_queue as mq
from utils import thread_utils, shellcmd, config_utils, tv_utlils


class MediaBrandSwitchThread(thread_utils.LoopThread):
    """
    视频商切换线程
    """
    def __init__(self, brand_list: list, interval: int, device: dv.Device, local_video: dict, profile: str, mpf: pf.Performance):
        super(MediaBrandSwitchThread, self).__init__()
        self.brand_list = brand_list
        self.interval = interval
        self.device = device
        self.cur_brand = ''
        self.local_video = local_video
        self.pf = mpf
        self.settings = config_utils.read_config(profile)
        logging.debug(f'brand_list {self.brand_list}\n'
                      f'interval {self.interval}\n'
                      f'local_video {self.local_video}\n'
                      f'settings {self.settings}')
        if len(brand_list) < 1:
            raise ValueError('brand list must not null')

    def my_loop(self):
        """
        工作流程
        :return:
        """
        # 随机视频商播放
        self._random_brand_media()
        i = 0
        # 等待
        while self.flag and i < self.interval:
            i += 1
            time.sleep(1)
            # 检测是否本地视频不支持视频文件的弹窗，出现则关闭
            tv_utlils.close_multi_media_dialog(self.device)

    def _random_brand_media(self):
        """
        随机下一个视频商
        :return:
        """
        if len(self.brand_list) == 0:
            raise AssertionError("null brand_list, exit")
        elif len(self.brand_list) == 1:
            self.cur_brand = self.brand_list[0]
            self._set_brand_media(self.brand_list[0])
        else:
            while True:
                brand = random.choice(self.brand_list)
                logging.debug('random brand : ' + brand)
                if brand != self.cur_brand:
                    self._set_brand_media(brand)
                    self.cur_brand = brand
                    break

    def _set_brand_media(self, brand):
        """
        通过传进来的视频商类型，进行对应的视频播放处理
        :param brand:
        :return:
        """
        logging.debug(f'_set_brand_media : {brand}')
        if brand.startswith('本地视频'):
            self.pf_set_mode('本地视频')
            if self.local_video[brand].strip():
                fils_num = tv_utlils.device_send_r(self.device, 'ls -l ' + self.local_video[brand] + '| wc -l')
                start_index = random.randint(0, int(fils_num)-2)
                tv_utlils.device_send(self.device, 'am force-stop com.konka.multimedia')
                time.sleep(1)
                tv_utlils.load_media_dir(self.device, self.local_video[brand])
                time.sleep(2)
                tv_utlils.play_video(self.device, self.local_video[brand], start_index, )
            else:
                logging.warning(f'directory of brand {brand} is null')
        elif brand == '信源':
            self.pf_set_mode('信源')
            tv_utlils.device_send(self.device, 'am broadcast -a com.konka.GO_TO_TV')
        else:
            if not self.settings[brand]:
                self.pf_set_mode('无效brand')
                logging.warning(f'cmd of brand {brand} is null, please check video_brand.json')
            else:
                self.pf_set_mode(brand)
                if self.settings[brand]:
                    tv_utlils.input_android_key(self.device, 3)
                    time.sleep(3)
                    index = random.randint(0, len(self.settings[brand]) - 1)
                    tv_utlils.device_send(self.device, self.settings[brand][index])

    def pf_set_mode(self, mode):
        if self.pf is not None:
            self.pf.set_mode(mode)


class SceneMedia(sc.Scene):
    """
    视频类压测场景实现
    """
    def __init__(self,
                 name: str,
                 exec_time: int,
                 checker: ck.Checker,
                 brand_list: list,
                 performance_str: str,
                 profile: str = None,
                 performance_interval: (int, float) = None,
                 brand_switch_interval: (int, float) = None,
                 check_interval: (int, float) = None,
                 local_video: dict = None,
                 by: int = sc.BY_TIME):
        sc.Scene.__init__(self, name=name, exec_time=exec_time, by=by, checker=checker)
        self.brand_list = brand_list
        self.profile = profile
        self._profile = constant.VIDEO_BRAND if self.profile is None or not profile.strip() else self.profile
        self.config_list += [self._profile]
        self.brand_switch_interval = get_second(brand_switch_interval, 'scene_media', 'brand_switch_interval')
        self.performance_interval = get_second(performance_interval, 'scene_media', 'performance_interval')
        self.check_interval = get_second(check_interval, 'scene_media', 'check_interval')

        self.performance_str = performance_str
        self.performance_process = list()
        self._parse_performance_process(self.performance_str)

        self.local_video = {'本地视频_大码率': '', '本地视频_混合编解码': ''}
        if local_video is not None:
            self.local_video = local_video

        self.performance_thread = None
        self.brand_switch_thread = None

        self.save_in_usb = True
        self.dependent.init(
            usb=self.save_in_usb,
        )

    def serialize(self):
        ret = {
            'brand_list': self.brand_list,
            'profile': self.profile,
            'performance_interval': self.performance_interval,
            'check_interval': self.check_interval,
            'brand_switch_interval': self.brand_switch_interval,
            'performance_str': self.performance_str,
            'local_video': self.local_video
        }
        ret.update(self.base_serialize())
        return ret

    @staticmethod
    def deserialize(d: dict) -> 'SceneMedia':
        return sc.Scene.base_deserialize(SceneMedia, d)

    def _parse_performance_process(self, performance_str):
        """
        解析性能检测进程字符串，生成进程列表
        :param performance_str:
        :return:
        """
        for item in performance_str.split(';'):
            item = item.strip()
            if not item:
                continue
            self.performance_process.append(item)

    def _get_config_detail(self) -> list:
        second = list()
        second.append('视频商:' + '、'.join(self.brand_list))
        second.append('在线视频配置文件:' + self._profile)
        tv_src_path = []
        for key, value in self.local_video.items():
            value = value.strip()
            if value.strip():
                tv_src_path.append(value)
        if tv_src_path:
            second.append('本地视频资源:' + ';'.join(tv_src_path))
        if self.performance_process:
            second.append('监测进程:' + '、'.join(self.performance_process))
            second.append('性能抓取间隔:' + str(constant.second2other(self.performance_interval, constant.MINUTE)) + '分钟')
        return second

    def init_main_sheet(self):
        second_str = '\n'.join(self._get_config_detail())
        ex.init_main_sheet(self.report, self.name, second_str)

    def base_env_check_body(self):
        """
        该场景自定义的一键调试
        :return:
        """
        mq.ck_queue.put((mq.TAG_MSG, '检测是否插入U盘'))
        if not tv_utlils.is_any_usb_mounted(self.device):
            mq.TAG_EXCEPTION((mq.TAG_EXCEPTION, '未检测到任何U盘'))
            return False
        return super().base_env_check_body()

    def work(self):
        """
        场景工作流程
        :return:
        """
        if self.device is None:
            return
        # 抓log
        self.fd.start_log_single()
        if self.performance_process:
            # 开启性能测试线程
            self.performance_thread = pf.Performance(
                process=self.performance_process,
                interval=self.performance_interval,
                device=self.device,
                fd=self.fd
            )
            self.performance_thread.start()
        # 开启视频商切换线程
        self.brand_switch_thread = MediaBrandSwitchThread(
            self.brand_list,
            self.brand_switch_interval,
            self.device,
            self.local_video,
            self._profile,
            self.performance_thread
        )
        self.brand_switch_thread.start()
        # 超时检测
        while not self.is_timeout():
            # 等待
            self.wait_timeout_or_interval(self.check_interval)
            # 检测
            summary = self.checker.check(is_on_and_off=False)
            # 更新报告
            self.upgrade_summary(time.time() - self.start_time, summary, record_times=True)
        if self.performance_process:
            # 停止性能检测线程
            self.performance_thread.terminal()
        # 停止视频商切换线程
        self.brand_switch_thread.terminal()
        # 停止抓log
        self.fd.stop_log()

