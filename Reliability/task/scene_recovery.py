"""
恢复出厂设置场景实现
"""
import logging
import time
import constant

from task import scene as sc, excel as ex, checker as ck, dc_wake as dk, device as dv, script_parser as sp
from utils import play_voice, tv_utlils


class SceneRecovery(sc.Scene):
    """
    恢复出厂设置场景实现
    """
    def __init__(self,
                 name: str,
                 exec_time: int,
                 checker: ck.Checker,
                 retain_app: bool,
                 serial_open: bool,
                 by: int = sc.BY_COUNT):
        sc.Scene.__init__(self, name=name, exec_time=exec_time, by=by, checker=checker)
        self.retain_app = retain_app
        self.serial_open = serial_open

    def serialize(self):
        ret = {
            'retain_app': self.retain_app,
            'serial_open': self.serial_open,
        }
        ret.update(self.base_serialize())
        return ret

    @staticmethod
    def deserialize(d: dict) -> 'SceneRecovery':
        return sc.Scene.base_deserialize(SceneRecovery, d)

    def _get_config_detail(self):
        second = list()
        second.append('保留应用:' + '是' if self.retain_app else '否')
        return second

    def init_main_sheet(self):
        second_str = '\n'.join(self._get_config_detail())
        ex.init_main_sheet(self.report, self.name, second_str)

    def work(self):
        if self.device is None:
            return
        third_apks = list()
        while not self.is_timeout():
            if self.checker.install_apk:
                # 批量安装apk
                tv_utlils.install_apks(self.device, self.checker.apk_root)
                # 获取第三方apk列表
                third_apks = tv_utlils.third_apks(self.device)
            # 执行
            self._recover()
            if not self.serial_open:
                self._open_serial()
            self._serial_init()
            summary = self.checker.check(third_apks=third_apks)
            self.upgrade_summary(self.cur_count, summary)
            # 增加延时动作避免太快
            tv_utlils.go_home(self.device)
            time.sleep(2)
            tv_utlils.go_home(self.device)

    def _recover(self):
        """
        执行恢复出厂设置脚本，即reset.txt脚本
        :return:
        """
        logging.debug('_recover ScriptHandler')
        handler = sp.ScriptHandler(script_file=constant.RESET_SCRIPT, device=self.device, serial_enable=True)
        logging.debug('_recover ing...')
        handler.handle()

    def _open_serial(self):
        """
        执行开串口脚本，即open_serial.txt
        :return:
        """
        logging.debug('_open_serial ScriptHandler')
        handler = sp.ScriptHandler(script_file=constant.RECOVERY_SCRIPT, device=self.device)
        logging.debug('_open_serial ing...')
        handler.handle()

    def _serial_init(self):
        """
        检测串口是否可用，不可用则抛异常以停止本场景的测试
        :return:
        """
        ret, msg = tv_utlils.check_tv_com(self.device)
        if not ret:
            logging.warning(f'serial init fail, msg: {msg}')
            raise AssertionError('serial init fail, exit')
        logging.debug('serial init success')
