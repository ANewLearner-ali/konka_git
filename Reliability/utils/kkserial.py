import logging
import threading
import traceback

import serial
import serial.tools.list_ports
import time
import sys

class KKSerialFactory:
    kk_serials = dict()

    @classmethod
    def get_kk_serial(cls, com, baudrate=115200, timeout=None) -> '_KKSerial':
        """
        通过com口获取串口对象
        """
        if com in cls.kk_serials:
            # TODO check baudrate and timeout
            return cls.kk_serials[com]
        cls.kk_serials[com] = _KKSerial(com, baudrate=baudrate, timeout=timeout)
        return cls.kk_serials[com]

    @classmethod
    def is_com_in_kk_serial(cls, com) -> bool:
        """
        判断是否已存在指定com口的串口对象
        """
        return com in cls.kk_serials

    @classmethod
    def close_kk_serial(cls, com) -> bool:
        """
        关闭指定com口的串口对象，并移除出串口对象集
        """
        if com in cls.kk_serials:
            if cls.kk_serials[com]:
                cls.kk_serials[com].close()
                cls.kk_serials.pop(com)
                return True
            else:
                cls.kk_serials.pop(com)
                return False
        else:
            return False

    @staticmethod
    def get_all_serial() -> list:
        """
        获取所有的com口
        """
        port_list = list(serial.tools.list_ports.comports())
        logging.debug(port_list)
        if len(port_list) == 0:
            logging.debug('not found any serial com')
            return []
        else:
            logging.debug('serial list:')
            port_device_list = []
            for i in range(0, len(port_list)):
                logging.debug(port_list[i])
                port_device_list.append(port_list[i].device)
            port_device_list.sort()
            return port_device_list

    @classmethod
    def get_ch340_com(cls) -> str:
        """
        获取第一个单片机com口，没有返回None
        """
        port_list = list(serial.tools.list_ports.comports())
        if port_list:
            for i in range(0, len(port_list)):
                if 'CH340' in port_list[i].description:
                    return port_list[i].device

    @classmethod
    def get_ch340_com_list(cls) -> list:
        """
        获取单片机com列表
        """
        com_list = list()
        port_list = list(serial.tools.list_ports.comports())
        if port_list:
            for i in range(0, len(port_list)):
                if 'CH340' in port_list[i].description:
                    com_list.append(port_list[i].device)
        return com_list

    @classmethod
    def is_ch340_com_exist(cls, com) -> bool:
        """
        判断是否已存在指定单片机com口
        """
        if com in cls.get_ch340_com_list():
            return True
        return False


error_dict = dict()


class _KKSerial:
    """
    串口库
    """
    def __init__(self, com: str, baudrate=115200, timeout=None):
        self._cache = b''
        self._com = com
        self._baudrate = baudrate
        self._timeout = timeout
        self.serial = None

        # try:
        #     self.serial = serial.Serial(com, baudrate=baudrate, timeout=timeout)
        # except SerialException:
        #     self.serial = None

        self.read_thread = None
        self._lock = None
        self._write_lock = None
        self._is_reading = False
        self.switch = True
        self._is_init = False
        self.init()

    @property
    def cache(self):
        return self._cache

    def init(self):
        self.serial = serial.Serial(self._com, baudrate=self._baudrate, timeout=self._timeout)
        if self.is_serial_valid():
            if self._is_init:
                return
            self._is_init = True
            self._is_reading = True
            self._lock = threading.Lock()
            self._write_lock = threading.Lock()
            self.read_thread = threading.Thread(target=self._reading)
            self.read_thread.start()
        else:
            raise AssertionError('serial init fail, is the serial {!r} opening ?'.format(self._com))

    def is_serial_valid(self):
        if self.serial and self.serial.is_open:
            return True
        return False

    def clear_cache(self):
        self._lock.acquire()
        self._cache = b''
        self._lock.release()

    def read_all_quick(self, wait=0.2):
        """
        读取串口缓存数据
        """
        time.sleep(wait)
        self.serial.flushInput()
        try:
            return self._cache.decode()
        except:
            logging.debug('_reading decode fail !!!')
        return ''

    def read_all(self, wait=0.5):
        """
        读取串口缓存数据，同上，慢点而已
        """
        time.sleep(wait)
        self.serial.flushInput()
        time.sleep(wait)
        try:
            return self._cache.decode()
        except:
            logging.debug('_reading decode fail !!!')
        return ''

    # def write(self, text: str):
    #     """
    #     往串口写数据
    #     """
    #     # logging.debug(self._com + ' write :' + text.replace('\r', '\\r'))
    #     self._write_lock.acquire()
    #     self.serial.flushOutput()
    #     now = 0
    #     step = 10
    #     for i in range(len(text) // step):
    #         # strip_str = text[now:now + step].encode('utf-8')
    #         # logging.debug('strip_str: {}'.format(strip_str))
    #         # logging.debug('write_len: {}'.format(strip_str))
    #         self.serial.write(text[now:now + step].encode('utf-8'))
    #         time.sleep(0.01)
    #         self.serial.flushOutput()
    #         now = now + step
    #     # strip_str = text[now:now + step].encode('utf-8')
    #     # logging.debug('strip_str: {}'.format(strip_str))
    #     self.serial.write(text[now:now + step].encode('utf-8'))
    #     time.sleep(0.05)
    #     self.serial.flushOutput()
    #     self._write_lock.release()
    #     return 1

    def write(self, text: str):
        """
        往串口写数据,时间增加0.005s
        """
        # logging.debug(self._com + ' write :' + text.replace('\r', '\\r'))
        self._write_lock.acquire()
        self.serial.flushOutput()
        now = 0
        step = 10
        for i in range(len(text) // step):
            self.serial.write(text[now:now + step].encode('utf-8'))
            time.sleep(0.015)
            self.serial.flushOutput()
            now = now + step
        self.serial.write(text[now:now + step].encode('utf-8'))
        time.sleep(0.05)
        self.serial.flushOutput()
        self._write_lock.release()
        return 1

    def _reading(self):
        global error_dict
        while self._is_reading:
            try:
                if self.serial.in_waiting and self.switch:
                    text = self.serial.read(self.serial.in_waiting)
                    self._cache += text
            except:
                # logging.warning(traceback.format_exc())
                # 计数10次串口断掉就做抛出关闭串口
                _error = sys.exc_info()[0]
                if _error not in error_dict.keys():
                    logging.warning('Fist times,mark this error')
                    logging.warning(traceback.format_exc())
                    error_dict[_error] = 0
                else:
                    if error_dict[_error] >= 10:
                        logging.warning(traceback.format_exc())
                        KKSerialFactory.close_kk_serial(self._com)
                        logging.warning('More than 10 times, close the serial')
                        error_dict = dict()
                        self._cache = 'No such file or directory'
                    else:
                        error_dict[_error] += 1

    def _reading_old(self):
        while self._is_reading:
            if self.serial.in_waiting and self.switch:
                text = self.serial.read(self.serial.in_waiting)
                try:
                    self._cache += text.decode('utf-8')
                except:
                    logging.debug('_reading decode fail !!!')

    def wait_for_string(self, string: str, timeout=None):
        """
        等待串口出现指定字段
        """
        if timeout is not None and timeout >= 0.0:
            spent = 0.0
            string = string.encode()
            while spent <= timeout * 5.0:
                if string in self._cache:
                    return True
                time.sleep(0.2)
                spent += 1.0
            return False
        while True:
            if string.encode() in self._cache:
                return True
            time.sleep(0.2)

    def wait_for_strings(self, strings, timeout=None):
        """
        等待串口出现strings列表中任意字符，出现则返回对应的index
        """
        string_enum = dict(enumerate(strings))
        for key in string_enum:
            string_enum[key] = string_enum[key].encode()
        if timeout is not None and timeout >= 0.0:
            spent = 0.0
            while spent <= timeout * 5.0:
                for key in string_enum:
                    if string_enum[key] in self._cache:
                        return key
                time.sleep(0.2)
                spent += 1.0
            return False
        while True:
            for key in string_enum:
                if string_enum[key] in self._cache:
                    return key
            time.sleep(0.2)

    def close(self):
        """
        关闭串口
        """
        logging.debug(f'{self._com} close...')
        self._is_reading = False
        self.serial.close()

    def set_read_switch(self, on: bool):
        self.switch = on


if __name__ == '__main__':
    ...