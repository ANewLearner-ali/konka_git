"""
monkey相关的场景实现
"""
import logging
import random
import re
import time
import constant
from constant import get_second

from task import scene as sc, excel as ex, checker as ck, device as dv, fd
from utils import thread_utils, config_utils, tv_utlils


_MODE_MONKEY = 'monkey'
_MODE_NORMAL = 'normal'
_MODE_MEDIA = 'media'

VIDEO = '视频'
MUSIC = '音乐'
IMAGE = '图片'

DEFAULT_MONKEY_PREV = 'export CLASSPATH=/data/misc/konka/monkey.jar\r' \
                      'app_process /data/misc/konka com.android.commands.monkey.Monkey  '
DEFAULT_MONKEY_TAIL = ' --ignore-crashes --ignore-timeouts --kill-process-after-error  ' \
                      '--ignore-security-exceptions --throttle 100 --pct-nav 35 --pct-majornav 30 ' \
                      '--pct-syskeys 30 --pct-appswitch 5 -v -v -v  9999999 '


def _stop_monkey(device: dv.Device):
    """
    停止指定设备的monkey测试
    :param device:
    :return:
    """
    logging.debug('stop monkey')
    tv_utlils._send_cmd(device, 'busybox killall com.android.commands.monkey')


def _start_monkey(device: dv.Device, cmd: str, restart: bool = False, daemon: bool = False):
    """
    通过传进来的设备和monkey命令，开启monkey测试
    :param device:
    :param cmd:
    :param restart:
    :param daemon:
    :return:
    """
    if restart:
        _stop_monkey(device)
        tv_utlils._send_cmd(device, cmd)
    elif daemon:
        if not device.tv.send_cmd_get_result('busybox ps |grep "com.android.commands.monkey$"').strip():
            tv_utlils._send_cmd(device, cmd)
    else:
        tv_utlils._send_cmd(device, cmd)
    time.sleep(1)


def _valid_package(package_string: str):
    """
    通过包名或者是Activity类名获取有效的monkey命令(特指-p后面接的命令)
    :param package_string:
    :return:
    """
    if '/' in package_string:
        package, activity_clazz = package_string.split('/')
        if '/.' in package_string:
            activity_clazz = package + activity_clazz
        package_string = package + ' --konka-p ' + package + ' --konka-a ' + activity_clazz
    return package_string


def parse_cmd(cmd, monkey_error):
    """
    解析原始的monkey指令，并进行处理，使其适用于康佳自研的monkey.jar
    :param cmd:
    :param monkey_error:
    :return:
    """
    cmd_list = re.split(r'\s+', cmd)
    i = 0
    is_prev_p = False
    while i < len(cmd_list):
        if is_prev_p:
            cmd_list[i] = _valid_package(cmd_list[i])
            is_prev_p = False
        elif cmd_list[i] == '-p':
            is_prev_p = True
        i += 1
    cmd = ' '.join(cmd_list)
    cmd = cmd.rsplit('&', 1)[0]
    cmd += ' 1>/dev/null 2>>' + monkey_error
    cmd = cmd.strip().lstrip('monkey')
    cmd = DEFAULT_MONKEY_PREV + cmd + ' &'
    return cmd


def _get_monkey_cmd(package: str, monkey_error: str):
    """
    通过包名或Activity类型获取完整的有效的monkey指令
    :param package:
    :param monkey_error:
    :return:
    """
    package = package.strip()
    if not package:
        raise AssertionError('null package')
    cmd = DEFAULT_MONKEY_PREV + '-p ' + _valid_package(package) + \
          DEFAULT_MONKEY_TAIL + ' 1>/dev/null 2>>' + monkey_error + ' &'
    return cmd


def _parse_media_root(com, root: str):
    """
    通过配置文件的media根目录，初始化数据，如果未找到任何多媒体资源则抛异常
    :param com:
    :param root:
    :return:
    """
    ret = dict()
    ret['video'] = root + '/' + VIDEO, tv_utlils.parse_str2int(tv_utlils.file_count(com, root + '/' + VIDEO))
    ret['music'] = root + '/' + MUSIC, tv_utlils.parse_str2int(tv_utlils.file_count(com, root + '/' + MUSIC))
    ret['image'] = root + '/' + IMAGE, tv_utlils.parse_str2int(tv_utlils.file_count(com, root + '/' + IMAGE))
    s = sum([ret[key][1] for key in ret if ret[key][1] > 0])
    if s <= 0:
        raise AssertionError(f'not found any multimedia file in {root}')
    return ret


class _MultiMediaThread(thread_utils.LoopThread):
    """
    monkey测试中的多媒体播放场景
    """
    def __init__(self, device, root):
        super(_MultiMediaThread, self).__init__()
        self.device = device
        self.root = root
        self.r = _parse_media_root(self.device, self.root)
        self.interval = get_second(None, 'scene_monkey_logic', 'multimedia')
        self.wait = get_second(None, 'scene_monkey_logic', 'multimedia_page')

    # def load_all(self):
    #     tv_utlils.device_send(self.device, 'am force-stop com.konka.multimedia')
    #     time.sleep(self.wait)
    #     for key, value in self.r.items():
    #         tv_utlils.load_media_dir(self.device, value[0])
    #         time.sleep(self.wait)
    #         tv_utlils.go_home(self.device)
    #         time.sleep(self.wait)

    def my_loop(self):
        """
        工作流程
        :return:
        """
        # 关闭文件管理
        tv_utlils.device_send(self.device, 'am force-stop com.konka.multimedia')
        while self.flag:
            i = 0
            # 随机播放多媒体文件
            self.random_multimedia()
            # 等待
            while self.flag and i < self.interval:
                time.sleep(1)
                i += 1

    def random_multimedia(self):
        """
        随机播放多媒体文件
        :return:
        """
        keys = ['video', 'music', 'image']
        key = random.choice(keys)
        root, count = self.r[key]
        if count <= 0:
            self.random_multimedia()
        else:
            tv_utlils.go_home(self.device)
            time.sleep(self.wait)
            n = random.randint(0, count - 1)
            tv_utlils.load_media_dir(self.device, root)
            time.sleep(self.wait)
            if key == 'video':
                tv_utlils.play_video(self.device, root, n, 0)
            elif key == 'music':
                tv_utlils.play_music(self.device, root, n, 0)
            elif key == 'image':
                tv_utlils.play_image(self.device, root, n, 0)
            else:
                raise AssertionError(f'error type : {key}')


class _GlobalHandleThread(thread_utils.LoopThread):
    """
    默认逻辑monkey的处理线程，这里名字起错了，不改了
    """
    def __init__(self, profile: list(), interval: int, device: dv.Device, tfd: fd.FD):
        super(_GlobalHandleThread, self).__init__()
        self.profile = profile
        self.interval = interval
        self.device = device
        self.fd = tfd
        self.index = -1
        self._config = self._parse_profile()
        self._keys = list(self._config.keys())
        self._index = -1
        self.multimedia_thread = None

    def my_loop(self):
        """
        工作流程
        :return:
        """
        mode = None
        try:
            # 获取下一个场景模式
            mode = self._next_handle()
        except RecursionError as e:
            logging.exception(e)
            # TODO config all entry illegal, how to do
        i = 0
        # 等待
        while mode != _MODE_NORMAL and self.flag and i < self.interval:
            i += 1
            time.sleep(1)
        if mode == _MODE_MONKEY:
            # monkey场景模式的处理，即停止monkey进程
            _stop_monkey(self.device)
        elif mode == _MODE_MEDIA:
            # 多媒体场景模式的处理，即停止多媒体线程
            self.multimedia_thread.terminal()

    def _parse_profile(self) -> dict:
        """
        解析默认逻辑monkey的配置文件
        :return:
        """
        ret = {}
        settings = config_utils.read_config(self.profile)
        packages = self.device.tv.send_cmd_get_result('pm list packages | busybox awk -F ":" \'{print $2}\'')
        packages = packages.split('\r\n')
        for key, value in settings.items():
            if key in packages:
                ret[key] = value
        return ret

    def _next_handle(self):
        """
        执行下一个场景模式
        :return:
        """
        # cmd 的解析可以放到_parse_profile去做，但是算了
        if len(self._keys) < 1:
            return
        self._index += 1
        if self._index == len(self._keys):
            self._index = 0
        value = self._config[self._keys[self._index]]
        if value.get('mode', None):
            logging.debug(f'_next_handle mode : {value.get("mode")}')
            # monkey模式
            if value['mode'] == _MODE_MONKEY:
                if value.get('cmd', None):
                    cmd = value['cmd']
                    tv_utlils._send_cmd(self.device, cmd)
                else:
                    package = value.get('main_activity', '').strip()
                    package = package if package else self._keys[self._index]
                    cmd = _get_monkey_cmd(package, self.fd.monkey_error)
                    _start_monkey(self.device, cmd)
            # normal模式，即命令模式
            elif value['mode'] == _MODE_NORMAL:
                cmd = value.get('cmd', 'sleep 1')
                tv_utlils._send_cmd(self.device, cmd)
            # 多媒体模式
            elif value['mode'] == _MODE_MEDIA:
                # todo
                self.multimedia_thread = _MultiMediaThread(self.device, value['directory'])
                self.multimedia_thread.start()
                logging.debug(f'multimedia_thread started')
            else:
                raise TypeError('illegal mode {}'.format(value['mode']))
            return value['mode']
        elif value.get('cmd', None):
            # 未设置模式，但是有cmd参数则执行cmd命令
            self.device.tv.send_cmd(value['cmd'])
            return _MODE_NORMAL
        else:
            # 算是配置不完全，或者是无效包名，这里处理方式是继续执行下一个模式
            # TODO config error, ignore
            return self._next_handle()


class _MonkeySwitchThread(thread_utils.LoopThread):
    """
    自定义的逻辑monkey处理线程
    """
    def __init__(self, packages: list(), interval: int, device: dv.Device, tfd: fd.FD):
        super(_MonkeySwitchThread, self).__init__()
        self.packages = packages
        self.interval = interval
        self.device = device
        self.fd = tfd
        self._index = -1

    def my_loop(self):
        """
        工作流程
        :return:
        """
        # 停止monkey
        _stop_monkey(self.device)
        # 下一个应用
        self._next_package()
        # 等待
        i = 0
        while self.flag and i < self.interval:
            i += 1
            time.sleep(1)

    def _next_package(self):
        """
        执行下一个应用的monkey
        :return:
        """
        if len(self.packages) < 1:
            return
        self._index += 1
        if self._index == len(self.packages):
            self._index = 0
        _start_monkey(self.device, _get_monkey_cmd(self.packages[self._index], self.fd.monkey_error))


class SceneMonkeyGlobal(sc.Scene):
    """
    全局monkey场景实现
    """
    def __init__(self,
                 name: str,
                 exec_time: int,
                 checker: ck.Checker,
                 cmd: str,
                 check_interval: (int, float) = None,
                 by: int = sc.BY_TIME):
        sc.Scene.__init__(self, name=name, exec_time=exec_time, by=by, checker=checker)
        self.cmd = cmd
        self.check_interval = get_second(check_interval, 'scene_monkey_global', 'check_interval')

        self.save_in_usb = True
        self.dependent.init(
            usb=self.save_in_usb,
            monkey_tool=True
        )

    def serialize(self):
        ret = {
            'cmd': self.cmd,
            'check_interval': self.check_interval
        }
        ret.update(self.base_serialize())
        return ret

    @staticmethod
    def deserialize(d: dict) -> 'SceneMonkeyGlobal':
        return sc.Scene.base_deserialize(SceneMonkeyGlobal, d)

    def _get_config_detail(self):
        second = list()
        second.append('全局测试')
        second.append('指令:' + self.cmd)
        return second

    def init_main_sheet(self):
        second_str = '\n'.join(self._get_config_detail())
        ex.init_main_sheet(self.report, self.name, second_str)

    def work(self):
        """
        工作流程
        :return:
        """
        if self.device is None:
            return
        # 抓log
        self.fd.start_log_single()
        # 解析monkey指令
        self.cmd = self.cmd.split('1>', 1)[0].split('>', 1)[0]
        cmd = parse_cmd(self.cmd, self.fd.monkey_error)
        # 停止当前的monkey测试
        _start_monkey(self.device, cmd, restart=True)
        while not self.is_timeout():
            # 开启monkey测试
            _start_monkey(self.device, cmd, daemon=True)
            # 等待
            self.wait_timeout_or_interval(self.check_interval)
            # 检测
            summary = self.checker.check()
            # 更新报告
            self.upgrade_summary(time.time() - self.start_time, summary, record_times=True)
        # 停止monkey
        _stop_monkey(self.device)
        # 停止log
        self.fd.stop_log()


MODE_DEFAULT = 1
MODE_CUSTOMIZATION = 2


class SceneMonkeyLogic(sc.Scene):
    """
    逻辑monkey场景实现
    """
    def __init__(self,
                 name: str,
                 exec_time: int,
                 checker: ck.Checker,
                 mode: int,
                 packages: str = '',
                 switch_interval: (int, float) = None,
                 check_interval: (int, float) = None,
                 by: int = sc.BY_TIME):
        sc.Scene.__init__(self, name=name, exec_time=exec_time, by=by, checker=checker)
        if mode not in [MODE_DEFAULT, MODE_CUSTOMIZATION]:
            raise ValueError('mode must in {!r}'.format([MODE_DEFAULT, MODE_CUSTOMIZATION]))
        self.mode = mode
        self.packages_str = packages
        self.packages = [i.strip() for i in packages.split(';') if i.strip()]
        if self.mode == MODE_CUSTOMIZATION and not self.packages:
            raise ValueError('MODE_CUSTOMIZATION monkey, but packages is null')

        self.profile = constant.MONKEY_DEFAULT

        self.check_interval = get_second(check_interval, 'scene_monkey_logic', 'check_interval')
        self.switch_interval = get_second(switch_interval, 'scene_monkey_logic', 'switch_interval')

        self.handle_thread = None
        self.monkey_thread = None

        self.save_in_usb = True
        self.dependent.init(
            usb=self.save_in_usb,
            monkey_tool=True
        )

    def serialize(self):
        ret = {
            'mode': self.mode,
            'packages': self.packages_str,
            'switch_interval': self.switch_interval,
            'check_interval': self.check_interval,
        }
        ret.update(self.base_serialize())
        return ret

    @staticmethod
    def deserialize(d: dict) -> 'SceneMonkeyLogic':
        return sc.Scene.base_deserialize(SceneMonkeyLogic, d)

    def _get_config_detail(self):
        second = list()
        if self.mode == MODE_DEFAULT:
            second.append('固定逻辑')
        else:
            second.append('自定义逻辑:' + self.packages_str)
        second.append('切换时长:' + str(constant.second2other(self.switch_interval, constant.HOUR)) + 'H')
        second.append('压测时长:' + str(constant.second2other(self.exec_time, constant.HOUR)) + 'H')
        return second

    def init_main_sheet(self):
        second_str = '\n'.join(self._get_config_detail())
        ex.init_main_sheet(self.report, self.name, second_str)

    def work(self):
        """
        工作流程
        :return:
        """
        if self.device is None:
            return
        # 抓log
        self.fd.start_log_single()
        if self.mode == MODE_DEFAULT:
            # 默认的monkey处理，即按monkey配置文件去执行
            # 启动默认逻辑monkey的处理线程
            self.handle_thread = _GlobalHandleThread(self.profile, self.switch_interval, self.device, self.fd)
            self.handle_thread.start()
            while not self.is_timeout():
                self.wait_timeout_or_interval(self.check_interval)
                summary = self.checker.check()
                self.upgrade_summary(time.time() - self.start_time, summary, record_times=True)
            self.handle_thread.terminal()
        else:
            # 自定义的monkey处理
            # 启动自定义的逻辑monkey处理线程
            self.monkey_thread = _MonkeySwitchThread(self.packages, self.switch_interval, self.device, self.fd)
            self.monkey_thread.start()
            while not self.is_timeout():
                self.wait_timeout_or_interval(self.check_interval)
                summary = self.checker.check()
                self.upgrade_summary(time.time() - self.start_time, summary, record_times=True)
            self.monkey_thread.terminal()
            _stop_monkey(self.device)
        # 停止log
        self.fd.stop_log()
