"""
简单的任务管理器实现
"""
import logging

from task import task_base, device as dv

#试验一下,在这个包外面能不能调用到这个类：__TaskManager
class __TaskManager:
    def __init__(self):
        self._task_set = dict()

    def start_task(self, tv_com) -> tuple:
        """
        开始指定任务
        :param tv_com:
        :return:
        """
        task = self._task_set.get(tv_com, None)
        if task is None:
            return False, '任务不存在'
        if task.state != task_base.STATE_PREPARE:
            return False, f'任务启动失败，当前任务状态是{task.state}'
        task.start()
        return True, 'pass'

    def check(self, tv_com):
        """
        指定任务的环境检测
        :param tv_com:
        :return:
        """
        _task = self._task_set.get(tv_com, None)
        if _task is None:
            return False, f'不存在串口{tv_com}的任务'
        ret = _task.check()
        if not ret[0]:
            self._task_set.pop(tv_com)
            return ret
        return True, ''

    def add_task(self, task: task_base.TaskBase, tv_com: str, mcu_com: str = '') -> tuple:
        """
        新增指定任务并指定设备串口号
        :param task:
        :param tv_com:
        :param mcu_com:
        :return:
        """
        _task = self._task_set.get(tv_com, None)
        if _task is not None:
            logging.debug(f'add_task , {tv_com} old device: {_task.device}')
            if _task.state in [task_base.STATE_FINISH, task_base.STATE_FAIL]:
                task.device = _task.device
                self._task_set[tv_com] = task
            elif _task.state == task_base.STATE_RUNNING:
                return False, f'串口{tv_com} 已有任务'
            else:
                task_base.merge_scene(_task, task)
                return False, f'已存在任务，场景已成功追加到{tv_com}任务中！'
        else:
            task.device = dv.Device(tv_com, mcu_com)
            self._task_set[tv_com] = task
            logging.debug(f'add_task , {task} {id(task)} new device: {task.device}')
        return True, f'pass'

    def get_cur_scene(self, tv_com):
        """
        获取指定任务的当前执行场景
        :param tv_com:
        :return:
        """
        return self._task_set[tv_com].cur_scene if self._task_set.get(tv_com, None) else None

    @property
    def task_set(self):
        """
        属性，获取任务列表
        :return:
        """
        return self._task_set

    @property
    def com_list(self):
        """
        获取任务列表中对应的电视串口号列表
        :return:
        """
        return list(self._task_set.keys())

# 任务管理器单例
manager = __TaskManager()
