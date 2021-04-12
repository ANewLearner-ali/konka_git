"""
开机直达场景
"""

import logging
import time
import re
import random

from constant import get_second
from task import scene as sc, excel as ex, checker as ck, switch as sw
from utils import shellcmd


class SceneBootEnter(sc.Scene, sw.Switch):
    def __init__(self,
                 name: str,
                 exec_time: int,
                 inner: bool,
                 third: bool,
                 tv: bool,
                 by: int = sc.BY_COUNT,
                 checker: ck.Checker = None,
                 on2check_interval=None,
                 dc_off_interval=None,
                 mode=sw.MODE_DC,
                 reboot=True
                 ):
        sc.Scene.__init__(self, name=name, exec_time=exec_time, by=by, checker=checker)
        on2check_interval = get_second(on2check_interval, 'scene_boot_enter', 'on2check_interval')
        dc_off_interval = get_second(dc_off_interval, 'scene_boot_enter', 'dc_off_interval')
        sw.Switch.__init__(
            self,
            on2check_interval=on2check_interval,
            dc_off_interval=dc_off_interval,
            mode=mode,
            reboot=reboot)
        checker.window_assert = True
        checker.launcher = True
        self.inner = inner
        self.third = third
        self.tv = tv

        self.app_list_sp = '/data/data/com.konka.tvmanager/shared_prefs/share_data.xml'
        self.boot_enter_sp = '/data/data/com.konka.tvmanager/shared_prefs/boot_enter.xml'
        self.tv_manager_main = 'com.konka.tvmanager/com.konka.tvmanager.HomeActivity'
        self.tv_manager_boot_enter = 'com.konka.tvmanager/com.konka.tvmanager.bootenter.BootEnterActivity'
        self.app_list = dict()
        self.inner_app = list()
        self.third_app = list()
        self.selected_app = dict()
        self.index = 0

    def serialize(self):
        ret = {
            'inner': self.inner,
            'third': self.third,
            'tv': self.tv,
            'on2check_interval': self.on2check_interval,
            'dc_off_interval': self.dc_off_interval,
            'mode': self.mode,
            'reboot': self.reboot
        }
        ret.update(self.base_serialize())
        return ret

    @staticmethod
    def deserialize(d: dict) -> 'SceneBootEnter':
        return sc.Scene.base_deserialize(SceneBootEnter, d)

    def work(self):
        """
        场景具体工作流程
        :return:
        """
        if self.device is None:
            return
        self.init_data()
        while not self.is_timeout():
            app = self._next_app()
            logging.debug(f'selected package {app}')
            # 设置下次开机直达的应用
            self._set_boot_enter(app)
            self.checker.set_window(self.selected_app[app][1])
            # 关机
            self.switch(False)
            # 开机
            self.switch(True)
            # 等待
            self.on_wait_rest()
            # 检查
            summary = self.checker.check()
            # 更新报告
            self.upgrade_summary(self.cur_count, summary)
        self._set_boot_enter_launcher()

    def _get_config_detail(self):
        second = list()
        if self.inner:
            second.append('内置应用')
        if self.third:
            second.append('第三方应用')
        if self.tv:
            second.append('信源')
        return second

    def init_main_sheet(self):
        second_str = '\n'.join(self._get_config_detail())
        ex.init_main_sheet(self.report, self.name, second_str)

    def _get_apps(self, cmd) -> list:
        """
        通过传入的pm list packages命令获取包名列表
        :param cmd:
        :return:
        """
        packages = shellcmd.send_cmd_get_result(self.device.tv_com, cmd)
        ret = list()
        for line in packages.split('\r\n'):
            package = line.split(':', 1)[-1]
            if package in self.app_list:
                ret.append(package)
        return ret

    def _update_selected_app(self, app_list: list):
        """
        将传入的app列表更新到有效app列表中
        :param app_list:
        :return:
        """
        for package in app_list:
            try:
                self.selected_app[package] = self.app_list[package]
            except BaseException as e:
                logging.warning(f'set selected app fail, package is {package}')
                logging.exception(e)

    def init_data(self):
        """
        初始化数据，主要是初始化电视管家的配置文件；并获取电视已安装的包名，区分系统和第三方应用，生成最终需要遍历的app列表
        :return:
        """
        self.device.tv.send_cmd('am start -n ' + self.tv_manager_main)
        time.sleep(30)
        self.device.tv.send_cmd('am start -n ' + self.tv_manager_boot_enter)
        time.sleep(30)
        app_list_info = self.device.tv.send_cmd_get_result('cat ' + self.app_list_sp)
        for line in app_list_info.split('\r\n'):
            line = line.strip()
            match_list = re.findall(r'<string name=".*">(.*)-(.*)</string>', line)
            if len(match_list) < 1:
                continue
            match_list = match_list[0]
            # logging.debug('line:\n{}\nmatch_list:\n{}\n'.format(line, match_list))
            if not match_list:
                continue
            elif len(match_list) != 2:
                continue
            elif match_list[0] == 'null' and match_list[1] == 'null':
                self.app_list['com.konka.livelauncher'] = \
                    'null-null', 'com.konka.livelauncher/com.konka.livelauncher.Launcher'
            else:
                self.app_list[match_list[1]] = '-'.join(match_list), match_list[1] + '/' + match_list[0]
        logging.debug('app list:')
        for key, value in self.app_list.items():
            logging.debug('package {} : {}'.format(key, value))
        self.inner_app = self._get_apps('pm list packages -s')
        self.third_app = self._get_apps('pm list packages -3')
        if self.inner:
            self._update_selected_app(self.inner_app)
        if self.third:
            self._update_selected_app(self.third_app)
        if self.tv:
            self._update_selected_app(['com.konka.tvsettings'])
        for key, value in self.selected_app.items():
            logging.debug('package {} : {}'.format(key, value))

    def _random_app(self) -> str:
        """
        不用了，随机获取一个app
        :return:
        """
        if len(self.selected_app) < 1:
            raise AssertionError('not found selected apps, How To Do')
        index = random.randint(0, len(self.selected_app) - 1)
        key = list(self.selected_app.keys())[index]
        return key

    def _next_app(self) -> str:
        """
        获取下一个app
        :return:
        """
        if len(self.selected_app) < 1:
            raise AssertionError('not found selected apps, How To Do')
        if self.index >= len(self.selected_app):
            self.index = 0
        ret = list(self.selected_app.keys())[self.index]
        self.index += 1
        return ret

    def _set_boot_enter(self, package: str):
        """
        设置下次开机直达的应用
        :param package:
        :return:
        """
        self.device.tv.send_cmd('setprop persist.app.launch ' + self.selected_app[package][1])
        string = '<?xml version=\'1.0\' encoding=\'utf-8\' standalone=\'yes\' ?>\n<map>\n<string name=\\"boot_' \
                 'enter\\">' + self.selected_app[package][0] + '</string>\n</map>\n'
        self.device.tv.send_cmd('echo "' + string + '" > ' + self.boot_enter_sp)

    def _set_boot_enter_launcher(self):
        try:
            package = 'com.konka.livelauncher'
            self.device.tv.send_cmd('setprop persist.app.launch ' + self.app_list[package][1])
            string = '<?xml version=\'1.0\' encoding=\'utf-8\' standalone=\'yes\' ?>\n<map>\n<string name=\\"boot_' \
                     'enter\\">' + self.app_list[package][0] + '</string>\n</map>\n'
            self.device.tv.send_cmd('echo "' + string + '" > ' + self.boot_enter_sp)
        except BaseException as e:
            logging.warning('_set_boot_enter_launcher fail')
            logging.exception(e)


if __name__ == '__main__':
    s = SceneBootEnter(
        name='123',
        exec_time=10,
        inner=True,
        third=False,
        tv=True,
        checker=ck.Checker()
    )
    s.save()
