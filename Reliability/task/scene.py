"""
场景基类，定义了场景所需的接口和默认的接口实现
"""

import logging
import time
import abc
import constant
import importlib

from utils import time_utils, config_utils, tv_utlils
from task import dependent as dp, checker as ck, excel as ex, device as dv, i_serializable as i_s, fd, msg_queue as mq


BY_TIME = 1
BY_COUNT = 2

STATE_TODO = 1
STATE_RUNNING = 2
STATE_DELETE = 3
STATE_FINISH = 4
STATE_FAIL = 5


class Scene(i_s.ISerializable, metaclass=abc.ABCMeta):
    def __init__(self,
                 name: str,
                 exec_time: int,
                 by: int,
                 checker: ck.Checker = None,
                 dependent: dp.Dependent = None):
        self.name = name
        self.exec_time = exec_time
        self.by = by
        self.create_time = time_utils.datetime_string(time_utils.TYPE2)
        self.checker = checker if checker else ck.Checker()
        if dependent:
            self.dependent = dependent
        else:
            if self.checker is None:
                raise AttributeError('check is None, scene create fail')
            self.dependent = checker.generate_dependent()
        self.details = dict()
        self.work_threads = list()
        self.start_time = None
        self.cur_count = None
        self.report = None
        self.start_row = None
        self.device = None
        self.fd: fd.FD = None
        self.save_in_usb = False
        self.config_list = [constant.CONFIG_FILE]
        if self.by not in [BY_COUNT, BY_TIME]:
            raise KeyError('illegal by : {}'.format(self.by))

    @abc.abstractmethod
    def work(self): ...
    """
    抽象方法，需子类实现，场景具体的工作流程
    """

    @abc.abstractmethod
    def init_main_sheet(self): ...
    """
    抽象方法，需子类实现，补充主sheet的报告内容输出
    """

    def base_serialize(self):
        """
        基本的序列化操作
        :return:
        """
        return {
            'name': self.name,
            'exec_time': self.exec_time,
            'by': self.by,
            'create_time': self.create_time,
            'checker': self.checker.serialize(),
            'dependent': self.dependent.serialize(),
            'module': self.__module__,
            'clazz': self.__class__.__name__
        }

    @staticmethod
    def base_deserialize(clazz: type, d: dict):
        """
        静态方法，基本的反序列化操作
        :param clazz:
        :param d:
        :return:
        """
        checker = ck.Checker(**d['checker'])
        dependent = checker.generate_dependent()
        d['checker'] = checker
        d['dependent'] = dependent
        return clazz(**d)

    def setup(self, fd_, device: dv.Device):
        """
        场景初始化操作，设置了设备，文件处理器，并生成对应的目录结构和获取蓝牙设备的mac地址
        :param fd_:
        :param device:
        :return:
        """
        for file in self.config_list:
            if not config_utils.config_check(file):
                raise AssertionError(f'parse config file failed : {file}')
        self.fd = fd_
        self.report = self.fd.excel
        self.device = device
        tv_utlils.close_kernel_print(self.device)
        self.dependent.setup(self.device)
        self.checker.setup(self.device, self.fd)
        self.start_row = ex.get_start_row(self.report)
        self.init_main_sheet()
        self.init_timer()
        if self.device is None or not isinstance(self.device, dv.Device):
            logging.warning('scene setup fail, device disable !')
            return False
        self.fd.create_scene_root(self.name, self.save_in_usb)
        self.auto_set_mac()
        return True

    def auto_set_mac(self):
        """
        获取蓝牙设备mac地址
        :return:
        """
        if self.checker.blue_controller:
            self.checker.bt_ct_mac = tv_utlils.get_bt_ct_mac(self.device)
        if self.checker.blue_speaker:
            self.checker.a2dp_mac = tv_utlils.get_a2dp_mac(self.device)
        logging.debug(f'mac: ct -- {self.checker.bt_ct_mac}  a2dp -- {self.checker.a2dp_mac}')

    def teardown(self):
        """
        场景测试结束后的处理，现在的处理只有合并测试报告的单元格
        :return:
        """
        ex.merge_summary(self.report, self.start_row)

    def upgrade_summary(self, count, summary, record_times=False):
        """
        通过传进来的检测结果，更新到测试报告中
        """
        count_text = ''
        if record_times:
            count_text = str(count) if self.by == BY_COUNT else time_utils.datetime_string(time_utils.TYPE2)
        count = str(count) + '次' if self.by == BY_COUNT else str(round(count / 3600.0, 2)) + 'H'
        ex.upgrade_summary(self.report, self.start_row, count, summary, record_times, count_text)

    def init_timer(self):
        """
        初始化定时器和当前循环次数，即测试超时机制的初始化
        :return:
        """
        self.start_time = time.time()
        self.cur_count = 0

    def wait_timeout_or_interval(self, interval):
        """
        等待超时或者是传入的时间间隔，一般用于BY_TIME的场景
        :param interval:
        :return:
        """
        start = time.time()
        while True:
            now = time.time()
            # logging.debug(f'*** {now - start}  {interval}  {now - self.start_time}  {self.exec_time} ***')
            if now - start >= interval or now - self.start_time >= self.exec_time:
                return
            time.sleep(1)

    def is_timeout(self):
        """
        判断是否超时或者执行次数达到设定值
        :return:
        """
        if self.by == BY_TIME:
            now = time.time()
            logging.debug('cur_exec_time:{}, max_exec_time:{}'.format(now - self.start_time, self.exec_time))
            if self.start_time is None or not isinstance(self.start_time, (float, int)):
                raise KeyError('start_time expect float or int, but {}'.format(self.start_time))
            ret = now - self.start_time >= self.exec_time
        else:
            logging.debug('cur_count:{}, max_count:{}'.format(self.cur_count + 1, self.exec_time))
            if self.cur_count is None or not isinstance(self.cur_count, int):
                raise KeyError('cur_count expect int, but {}'.format(self.cur_count))
            ret = self.cur_count >= self.exec_time
        self.cur_count += 1
        logging.debug('is_timeout : {}'.format(ret))
        return ret

    def wait_interval(self, interval) -> bool:
        """
        不用了
        :param interval:
        :return:
        """
        start = time.time()
        while time.time() - start < interval:
            time.sleep(1)
        if self.by == BY_TIME and self.is_timeout():
            return False
        return True

    def save(self):
        """
        保存场景到配置文件中
        :return:
        """
        d = self.serialize()
        logging.warning(f'save {d}')
        config_utils.append_config(constant.SCENE_FILE, d)

    @staticmethod
    def scene_list():
        """
        静态方法，获取场景列表
        :return:
        """
        return config_utils.read_config(constant.SCENE_FILE)

    def get_dependent_info(self):
        """
        不用了
        :return:
        """
        return self.dependent.get_dependent_info()

    def _get_base_detail(self) -> list:
        """
        获取基本的场景信息
        :return:
        """
        ret = list()
        ret.append('场景名称:' + self.name)
        ret.append('创建时间:' + self.create_time)
        return ret

    def _get_dependent_detail(self) -> list:
        """
        获取环境依赖信息
        :return:
        """
        return self.dependent.get_detail()

    # subclass need to implement this method
    @abc.abstractmethod
    def _get_config_detail(self):
        """
        抽象方法，需要子类实现，获取具体的场景配置信息
        :return:
        """
        return []

    def _get_config_detail0(self, indentation: str = '    '):
        """
        获取场景的配置信息模板
        :param indentation:
        :return:
        """
        ret = ['场景配置:']
        details = self._get_config_detail()
        for i in range(len(details)):
            details[i] = indentation + details[i]
        ret += details
        return ret

    def _get_check_detail(self) -> list:
        """
        获取检查项的配置信息
        :return:
        """
        return self.checker.get_detail()

    def get_detail(self) -> str:
        """
        获取所有的场景信息描述
        :return:
        """
        ret = list()
        ret += self._get_base_detail()
        ret += self._get_dependent_detail()
        ret += self._get_config_detail0()
        ret += self._get_check_detail()
        return '\n'.join(ret)

    def _body_catch(self, fun) -> bool:
        """
        一键检测中检测项的异常处理
        :param fun:
        :return:
        """
        try:
            return fun()
        except BaseException as e:
            mq.ck_queue.put((mq.TAG_EXCEPTION, '出现异常:' + str(e)))
            return False

    def base_env_check_body(self) -> bool:
        """
        默认的场景一键检测
        :return:
        """
        mq.ck_queue.put((mq.TAG_MSG, '发送 Android HOME 键'))
        if not tv_utlils.input_android_key(self.device, 3):
            mq.ck_queue.put((mq.TAG_EXCEPTION, '串口命令超时'))
            return False
        mq.ck_queue.put((mq.TAG_MSG, '等待3秒'))
        time.sleep(3)
        mq.ck_queue.put((mq.TAG_MSG, '拉起应用' + constant.DEFAULT_CMP[0]))
        if not tv_utlils.am_start(self.device, constant.DEFAULT_CMP[1]):
            mq.ck_queue.put((mq.TAG_EXCEPTION, '串口命令超时'))
            return False
        mq.ck_queue.put((mq.TAG_MSG, '等待3秒'))
        time.sleep(3)
        return True

    def env_check(self, start=True, end=True, body=True):
        """
        一键检测
        :param start:
        :param end:
        :param body:
        :return:
        """
        if start:
            mq.ck_queue.put((mq.TAG_START, mq.TAG_START))
        if body:
            if not self._body_catch(self.base_env_check_body):
                return
        if end:
            mq.ck_queue.put((mq.TAG_END, mq.TAG_END))

    # 退出场景，并结束所有子线程
    def quit_scene(self):
        """
        未使用，预留接口，用于场景到的退出操作，当前实现是将最大超时设置为0
        :return:
        """
        logging.debug(f'try to quit scene "{self.name}"')
        try:
            self.exec_time = 0
            # for thread in self.work_threads:
            #     thread.terminal()
        except BaseException as e:
            logging.warning('quit_scene fail , msg  : ' + str(e))


def scene_list():
    """
   获取场景列表
    :return:
    """
    return config_utils.read_config(constant.SCENE_FILE)


def remove_scene(index: int) -> bool:
    """
    通过索引移除场景
    :param index:
    :return:
    """
    scenes = config_utils.read_config(constant.SCENE_FILE)
    if 0 <= index < len(scenes):
        scenes.pop(index)
        config_utils.write_config(constant.SCENE_FILE, scenes)
        return True
    return False


def deserialize(d: dict):
    """
    默认的反序列化操作
    :param d:
    :return:
    """
    d = d.copy()
    m = importlib.import_module(d['module'])
    if not hasattr(m, d['clazz']):
        raise ValueError('deserialize fail !')
    d.pop('module')
    dependent = d.pop('dependent')
    clazz = d.pop('clazz')
    create_time = d.pop('create_time')
    d['checker'] = ck.Checker(**d['checker'])
    obj = m.__dict__[clazz](**d)
    obj.create_time = create_time
    for key, value in dependent.items():
        if value:
            setattr(obj.dependent, 'key', value)
    return obj


def get_scene_detail(d: dict) -> str:
    """
    获取所有的场景信息描述
    :param d:
    :return:
    """
    return deserialize(d).get_detail()
