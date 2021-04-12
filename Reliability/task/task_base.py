"""
单个任务，一台电视执行若干场景定义为一个任务
"""
import logging
import os
import threading

import constant

from typing import List
from task import device as dv, scene as sc, excel as ex, dependent as dp, fd, msg_queue as mq
from utils import time_utils, file_utils, shellcmd

STATE_PREPARE = 'PREPARE'
STATE_RUNNING = 'RUNNING'
STATE_FINISH = 'FINISH'
STATE_FAIL = 'FAIL'


class TaskBase(threading.Thread):
    def __init__(self,
                 name: str,
                 device: dv.Device = None,
                 scene_list: List[sc.Scene] = None):
        super(TaskBase, self).__init__()
        self.name = name
        self.device = device
        self.scene_list = list(scene_list)
        self.cur_scene = None
        self.create_time2, self.create_time = time_utils.datetime_string_set([time_utils.TYPE1, time_utils.TYPE2])
        self.fd = None
        self.excel = None
        self.state = STATE_PREPARE
        self._scene_init()

    def _scene_init(self):
        """
        场景初始化，即反序列化场景生成具体的场景对象
        :return:
        """
        if len(self.scene_list) > 0 and not isinstance(self.scene_list[0], sc.Scene):
            for i in range(len(self.scene_list)):
                try:
                    self.scene_list[i] = sc.deserialize(self.scene_list[i])
                except BaseException as e:
                    mq.error_queue.put((self.device.tv_com, '实例化场景 "' + self.scene_list[i].name + '" 失败，原因：' + str(e)))
                    self.scene_list[i] = None
        self.scene_list = [i for i in self.scene_list if i is not None]
        for scene in self.scene_list:
            setattr(scene, 'state', sc.STATE_TODO)

    def set_device(self, device: dv.Device):
        self.device = device

    def check(self) -> tuple:
        """
        以任务为单位的环境检测，会遍历所有场景列表所需环境依赖做并集，生成新的环境依赖队形进行环境检测
        :return:
        """
        logging.debug(f'task_base check, device : {self.device}')
        config = {}
        for scene in self.scene_list:
            for key, value in scene.dependent.serialize().items():
                if value:
                    config[key] = True
        config['tv'] = True
        new_dp = dp.Dependent(**config)
        new_dp.device = self.device
        ret = new_dp.check()
        shellcmd.close_kk_serial(self.device.tv_com)
        return ret

    def setup(self):
        """
        任务初始化，任务目录和报告创建
        :return:
        """
        logging.debug('task setup')
        self.fd = fd.FD(self.name, self.device, self.create_time2)
        self.fd.init(self.device)
        self.fd.create_root()
        self.excel = self.fd.create_excel()

    def teardown(self):
        """
        任务收尾工作，关闭串口，优化测试报告展示
        :return:
        """
        logging.debug('task teardown')
        shellcmd.close_kk_serial(self.device.tv_com)
        self.fd.optimize()

    def run(self):
        """
        任务执行流程
        :return:
        """
        # 开始
        self.state = STATE_RUNNING
        try:
            # 任务初始化
            self.setup()
            # 遍历场景
            for scene in self.scene_list:
                # 忽略已删除的场景
                if scene.state == sc.STATE_DELETE:
                    continue
                setattr(scene, 'state', sc.STATE_RUNNING)
                self.cur_scene = scene
                try:
                    # 场景的初始化，执行，收尾
                    if scene.setup(self.fd, self.device):
                        scene.work()
                        scene.teardown()
                except BaseException as e:
                    # 场景执行异常处理
                    logging.exception(e)
                    mq.error_queue.put((self.device.tv_com, '执行场景 "' + scene.name + '" 失败，原因：' + str(e)))
                    setattr(scene, 'state', sc.STATE_FAIL)
                    continue
                if getattr(scene, 'state') != sc.STATE_FAIL:
                    setattr(scene, 'state', sc.STATE_FINISH)
            self.cur_scene = None
            # 任务收尾
            self.teardown()
        except BaseException as e:
            # 任务异常处理
            logging.exception(e)
            # 任务失败
            self.state = STATE_FAIL
            return
        # 任务完成
        self.state = STATE_FINISH

    def delete_scene(self, index) -> tuple:
        """
        删除场景
        :param index:
        :return:
        """
        if 0 > index or index >= len(self.scene_list):
            return False, 'invalid index'
        scene = self.scene_list[index]
        if getattr(scene, 'state') in (sc.STATE_RUNNING, sc.STATE_FINISH, sc.STATE_DELETE):
            return False, '只允许删除待执行的场景'
        setattr(scene, 'state', sc.STATE_DELETE)
        return True, '删除成功'

    def stop(self):
        ...

    def pause(self):
        ...

    def resume(self):
        ...


def merge_scene(old_task: TaskBase, new_task: TaskBase):
    """
    合并新旧任务，即新任务额场景列表追加到旧的场景列表中
    :param old_task:
    :param new_task:
    :return:
    """
    for scene in new_task.scene_list:
        old_task.scene_list.append(scene)


if __name__ == '__main__':
    from task import scene_on_and_off, scene_boot_enter, scene_tv, scene_media, scene_monkey, scene_wake, checker as ck, switch as sw, dc_wake as dk
    from utils import log

    log.init_logging("", output=False)

    scene1 = scene_on_and_off.SceneOnAndOff(
        name='开机压测',
        exec_time=2,
        by=sc.BY_COUNT,
        checker=ck.Checker(
            launcher=True,
            net=True,
            usb=True),
        mode=sw.MODE_DC,
        key_set=dict(volume=True, voice=True),
        on2check_interval=40,
        far=False
    )

    scene2 = scene_boot_enter.SceneBootEnter(
        name='开机直达',
        exec_time=1,
        by=sc.BY_COUNT,
        checker=ck.Checker(),
        inner=True,
        third=True,
        tv=True
    )

    scene3 = scene_tv.SceneTV(
        name='信源压测',
        exec_time=30,
        by=sc.BY_TIME,
        checker=ck.Checker(),
        channel_list=['DTMB', 'ATV'],
        channel_switch_interval=1,
        performance_interval=2,
        check_interval=60,
        performance_str='com.konka.tvsettings;com.konka.livelauncher',
    )

    scene4 = scene_media.SceneMedia(
        name='视频压测',
        exec_time=30,
        by=sc.BY_TIME,
        checker=ck.Checker(),
        brand_list=['腾讯视频', 'QQ音乐'],
        profile='',
        performance_interval=5,
        performance_str='com.konka.tvsettings;com.konka.livelauncher',
    )

    scene5 = scene_monkey.SceneMonkeyGlobal(
        name='全局monkey压测',
        exec_time=30,
        by=sc.BY_TIME,
        checker=ck.Checker(),
        cmd='monkey -p com.konka.tvmanager 100000&',
    )

    scene6 = scene_monkey.SceneMonkeyLogic(
        name='逻辑MONKEY',
        exec_time=30,
        by=sc.BY_TIME,
        checker=ck.Checker(),
        mode=scene_monkey.MODE_CUSTOMIZATION,
        packages='com.konka.tvmanager;com.tencent.qqmusictv',
        switch_interval=10,
    )

    scene7 = scene_monkey.SceneMonkeyLogic(
        name='逻辑MONKEY',
        exec_time=30,
        by=sc.BY_TIME,
        checker=ck.Checker(),
        mode=scene_monkey.MODE_DEFAULT,
        switch_interval=10,
    )

    scene8 = scene_wake.SceneDCWake(
        name='开机压测',
        exec_time=3,
        by=sc.BY_COUNT,
        checker=ck.Checker(),
        mode=dk.MODE_QUICK,
    )

    scene9 = scene_wake.SceneDCWake(
        name='开机压测',
        exec_time=2,
        by=sc.BY_COUNT,
        checker=ck.Checker(),
        mode=dk.MODE_NORMAL,
        dc_off_tag='Waiting for Powerkey'
    )
    task = TaskBase(name='task1',
                    device=dv.Device('com32', ''),
                    scene_list=[scene3])
    ck_ret = task.check()
    task.start()

