import logging
import threading
import time
from time import sleep

from PyQt5.QtCore import QThread, pyqtSignal

from utils.common import run_command, run_command_stdout


class LoopThread(threading.Thread):
    def __init__(self, daemon=True):
        threading.Thread.__init__(self, daemon=daemon)
        self.flag = True
        self.stopped = False

    def terminal(self):
        logging.debug('LoopThread {}, terminal !'.format(self.name))
        self.flag = False
        while not self.stopped:
            time.sleep(0.5)
        logging.debug('LoopThread {}, terminal complete !'.format(self.name))

    def run(self):
        while self.flag:
            self.my_loop()
        self.stopped = True

    def my_loop(self):
        raise NotImplementedError()


class LoopQThread(QThread):

    def __init__(self):
        QThread.__init__(self)
        self.flag = True
        self.stopped = False

    def terminal(self):
        self.flag = False
        while not self.stopped:
            sleep(0.01)

    def run(self):
        while self.flag:
            self.my_loop()
        self.stopped = True

    def my_loop(self):
        raise NotImplementedError()


class RunExeThread(LoopQThread):
    def __init__(self, cmd):
        LoopQThread.__init__(self)
        self.cmd = cmd

    def run(self):
        try:
            self.my_loop()
        except Exception as E:
            logging.debug(f'RunExeThread:  {E}')
            ...

    def my_loop(self):
        run_command(self.cmd)


class RemindThread(LoopQThread):
    exec_down = pyqtSignal(str)

    def __init__(self, cmd, click_text, start_exe_name):
        LoopQThread.__init__(self)
        self.cmd = cmd
        self.click_text = click_text
        self.start_exe_name = start_exe_name
        self.process_num = self._get_process_num()

    def run(self):
        run_command(self.cmd, get_return_value=False)
        while self.flag:
            self.my_loop()

    def my_loop(self):
        cur_process_num = self._get_process_num()
        if cur_process_num > self.process_num:
            self.exec_down.emit(self.click_text)
            self.flag = False
        sleep(0.2)

    def _get_process_num(self):
        result = run_command_stdout('tasklist |find /C "' + self.start_exe_name + '"')
        if result:
            return int(result)
        return 0
