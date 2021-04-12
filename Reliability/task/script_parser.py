import logging
import time

from task import device as dv
from utils import keycontrol, tv_utlils
from task import msg_queue as mq


TYPE_IR = 'ir'
TYPE_LONG_IR = 'long_ir'
TYPE_SLEEP = 'sleep'
TYPE_CMD = 'cmd'


class ScriptHandler:
    """
    自定义脚本处理器，用于恢复出厂设置场景
    """
    def __init__(
            self,
            script_file: str,
            device: dv.Device = None,
            serial_enable: bool = False
    ):
        self.script_file = script_file
        self.device = device
        self.serial_enable = serial_enable
        self.tag = 'ScriptHandler'

    def log(self, msg, level='debug'):
        """
        该模块自定义的log打印格式
        :param msg:
        :param level:
        :return:
        """
        if level == 'debug':
            logging.debug(self.tag + '  ' + msg)
        else:
            logging.warning(self.tag + '  ' + msg)

    def handle(self):
        """
        执行脚本
        :return:
        """
        mq.sk_queue.put((mq.TAG_START, mq.TAG_START))
        if self.device is None:
            mq.sk_queue.put((mq.TAG_EXCEPTION, f'ScriptHandler handle fail, device : {self.device}'))
            raise AssertionError(f'ScriptHandler handle fail, device : {self.device}')
        with open(self.script_file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip()
                if line.startswith('#'):
                    continue
                cmd = line.split(' ')
                cmd = [i for i in cmd if i]
                if not cmd:
                    continue
                if len(cmd) == 1:
                    # 短按红外
                    self.step_ir(cmd[0])
                elif cmd[0] == TYPE_SLEEP:
                    # 等待
                    self.step_sleep(float(cmd[1]))
                elif cmd[0] == TYPE_CMD:
                    # 串口命令
                    if self.serial_enable:
                        mq.sk_queue.put((mq.TAG_MSG, f'执行串口命令：'+' '.join(cmd[1:])))
                        tv_utlils.device_send(self.device, ' '.join(cmd[1:]))
                    else:
                        mq.sk_queue.put((mq.TAG_MSG, f'未连接串口：跳过 ' + ' '.join(cmd[1:])))
                else:
                    # 发送长按红外
                    self.step_ir(cmd[0], cmd[1])
            mq.sk_queue.put((mq.TAG_END, mq.TAG_END))

    def step_sleep(self, value):
        """
        步骤：等待
        :param value:
        :return:
        """
        mq.sk_queue.put((mq.TAG_MSG, f'等待：{value}s'))
        self.log(f'sleep {value}s')
        time.sleep(value)

    def step_ir(self, key, wait=None):
        """
        步骤: 发送红外按键
        :param key:
        :param wait:
        :return:
        """
        if wait:
            wait = float(wait)
            mq.sk_queue.put((mq.TAG_MSG, f'长按红外按键key:{key}，时间：{wait}s'))
            self.log(f'send long ir, wait:{wait}s, key:{key}')
        else:
            mq.sk_queue.put((mq.TAG_MSG, f'短按红外按键key:{key}'))
        if isinstance(key, str):
            key = keycontrol.find_ir_key_by_text(key)
        if key is None or not isinstance(key, keycontrol.Key):
            self.log(f'invalid key : {key}')
            return
        if wait is not None:
            self.device.mcu.press_ir(key, interval=wait, mode=keycontrol.MODE_LONG_PRESS)
        else:
            self.device.mcu.press_ir(key)
