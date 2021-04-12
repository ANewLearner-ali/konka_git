from PyQt5.QtCore import Qt,pyqtSignal,QPoint,QThread
from time import sleep

from task.msg_queue import ck_queue, TAG_EXCEPTION,TAG_END, TAG_START,TAG_MSG,error_queue,sk_queue
from task.scene_record import create_kk_record_scene
import logging
import time
import queue

from task.script_parser import ScriptHandler
from task.task_base import TaskBase
import traceback
from utils.shellcmd import close_kk_serial


STATE_TODO = 1
STATE_RUNNING = 2
STATE_DELETE = 3
STATE_FINISH = 4

class CreatTaskTread(QThread):
    error_signal = pyqtSignal(str, str)
    success_singal = pyqtSignal()
    over_signal = pyqtSignal()

    def __init__(self, device_list, scene_list, manager):
        super(QThread, self).__init__()
        self.device_list = list(device_list)
        self.scene_list = list(scene_list)
        self.manager = manager

    def run(self):
        self.run_main()

    def run_main(self):
        logging.debug('Add End Selected_scene_list')
        for devices in self.device_list:
            logging.debug('Devices: ' + " ".join(devices) + ' Add_Task_Start ')
            this_task = TaskBase(name='', device=None, scene_list= self.scene_list)
            result, msg = self.manager.add_task(this_task, tv_com=devices[0], mcu_com=devices[1])
            if result == False:
                logging.debug('Devices: ' + "".join(devices) + ' Add_fail ')
                self.error_signal.emit('添加异常', '添加任务失败，失败原因：'+msg)
                self.over_signal.emit()
                return
            logging.debug('Devices: ' + " ".join(devices) + ' Add_success ')

        for devices_check in self.device_list:
            logging.debug('Devices: ' + devices_check[0] + ' Check_Start... ')
            try:
                result, msg = self.manager.check(tv_com=devices_check[0])
                if result == False:
                    logging.debug('Devices: ' + devices_check[0] + 'Check_Fail... ')
                    self.error_signal.emit('检测异常', '端口' + devices_check[0] + '由于缺失环境：:' + msg+',请检查,不影响其他设备的任务执行')
                    self.device_list.remove(devices_check)
                    continue
            except:
                print(traceback.format_exc())
            logging.debug('Devices: ' + devices_check[0] + 'Check_Success... {}'.format(time.time()))
        start_task_num = 0
        if len(self.device_list) != 0:
            for devices_start in self.device_list:
                logging.debug('Devices: ' + devices_start[0] + 'Do start task... {}'.format(time.time()))
                result, msg = self.manager.start_task(tv_com=devices_start[0])
                time.sleep(0.3)
                if result is False:
                    logging.debug('Devices: ' + devices_start[0] + 'Fail to start task ... ')
                    self.error_signal.emit('执行异常', '启动任务失败，失败原因：' + msg)
                else:
                    start_task_num += 1
                logging.debug('Devices: ' + devices_start[0] + 'start task success... {}'.format(time.time()))
        if start_task_num >= 1:
            logging.debug('CreatTaskTread: success_signal emit... doing{}'.format(time.time()))
            self.success_singal.emit()
            logging.debug('CreatTaskTread: success_signal emit...done {}'.format(time.time()))
        self.over_signal.emit()


class LoopQThread(QThread):
    def __init__(self):
        QThread.__init__(self)
        self.flag = True
        self.stopped = False
        self.fist_flag = True

    def terminal(self):
        self.flag = False
        while not self.stopped:
            sleep(0.2)

    def run(self):
        while self.flag:
            self.my_loop()
        self.stopped = True

    def my_loop(self):
        raise NotImplementedError()


class script_run(LoopQThread):
    msg_signal = pyqtSignal()

    def __init__(self, file, device, isopen):
        super(script_run, self).__init__()
        self.file = file
        self.device = device
        self.isopen = True if isopen == 'True' else False

    def my_loop(self):
        logging.debug('script_run starting')
        try:
            self.msg_signal.emit()
            Script_run = ScriptHandler(self.file, self.device, self.isopen)
            Script_run.handle()
        except Exception as E:
            logging.debug('script_run: '+str(E))
        logging.debug('script_run complete')
        self.flag = False


class execMsgThread(LoopQThread):
    error_msg = pyqtSignal(tuple)

    def __init__(self):
        LoopQThread.__init__(self)

    def my_loop(self):
        if error_queue.qsize() != 0:
            text = error_queue.get()
            self.error_msg.emit(text)
        else:
            sleep(0.3)


class CreatRecorderScene(QThread):
    error_msg = pyqtSignal(str, str)
    script_list = pyqtSignal(list)
    def run(self):
        res, msg = create_kk_record_scene()
        if res == False:
            self.error_msg.emit('错误提示', msg)
        else:
            self.script_list.emit(msg)


class CreatTaskManagerScene(QThread):

    task_success = pyqtSignal(str)

    def __init__(self, manager, view_dict):
        super().__init__()
        self.manager = manager
        self.view_dict = view_dict

    def run(self):
        if len(self.manager.com_list) == 0:
            self.task_success.emit('任务未执行，无法打开！！')
        else:
            from model.model_task_manager_view import model_task_manager_view
            # if self.view_dict["task_manager_view"] is not None:
            #     self.view_dict["task_manager_view"].close()
            self.view_dict["task_manager_view"] = model_task_manager_view(self.manager)
            self.view_dict["task_manager_view"].show()
            self.task_success.emit("task_manager_view")




class get_debug_log(QThread):
    reflash_sig = pyqtSignal(tuple)
    close_sig = pyqtSignal()

    def run(self):
        while True:
            text = ck_queue.get()
            if text == '':
                sleep(0.3)
            else:
                self.reflash_sig.emit(text)
                if text[0] == TAG_END:
                    sleep(5)
                    self.close_sig.emit()
                    break
                if text[0] == TAG_EXCEPTION:
                    break

class script_debug_log(QThread):
    reflash_sig = pyqtSignal(tuple)
    close_sig = pyqtSignal()

    def run(self):
        while True:
            if sk_queue.qsize() != 0:
                text = sk_queue.get()
                self.reflash_sig.emit(text)
                logging.debug('script_debug_log reflash_sig emit, value: {}'.format(text))
                if text[0] == TAG_END:
                    sleep(5)
                    self.close_sig.emit()
                    break
                if text[0] == TAG_EXCEPTION:
                    logging.debug('script_debug_log happen an Error, value: {}'.format(text))
                    break
            else:
                sleep(0.1)

class sceneOneCheck(QThread):
    reflash_sig = pyqtSignal()
    dependent_check_sig = pyqtSignal(str)

    def __init__(self, scene):
        super(sceneOneCheck, self).__init__()
        self.scene = scene

    def run(self):
        self.scene.dependent.setup(self.scene.device)
        res, msg = self.scene.dependent.check()
        if not res:
            self.dependent_check_sig.emit(msg)
        else:
            self.reflash_sig.emit()
            self.scene.env_check()
            close_kk_serial(self.scene.device.tv_com)


class scene_test(QThread):
    sig = pyqtSignal(str)

    def __init__(self, task):
        super(scene_test, self).__init__()
        self.task = task

    def run(self):
        self.sig.emit('begin')
        self.task.start()
        while True:
            # logging.debug('task.name:' + self.task.name + 'task.state:'+ self.task.state)
            if self.task.state == 'RUNNING':
                sleep(0.5)
            else:
                self.sig.emit(self.task.state)
                break
        self.exit()

class manager_exec(LoopQThread):
    signal_change = pyqtSignal(str)

    def __init__(self, tast_set, com_list):
        LoopQThread.__init__(self)
        # super(manager_exec, self).__init__()
        self.tast_set = tast_set
        self.com_list = com_list
        self.com_id_dict = dict()
        self.monitor_com_list = list(self.com_list)

    def run(self):
        if self.fist_flag:
            self.begin()
        while self.flag:
            self.my_loop()
        self.stopped = True

    def begin(self):
        for com in self.com_list:
            while self.flag:
                if self.tast_set[com].state == 'FAIL' or self.tast_set[com].state == 'FINISH':
                    self.monitor_com_list.remove(com)
                    self.signal_change.emit(com)
                    if len(self.monitor_com_list) == 0:
                        self.stopped = True
                        self.flap = False

                    break
                elif self.tast_set[com].cur_scene == None:
                    sleep(0.3)
                else:
                    self.com_id_dict[com] = id(self.tast_set[com].cur_scene)
                    self.signal_change.emit(com)
                    break
        self.fist_flag = False

    def my_loop(self):
        for com in self.monitor_com_list:
            try:
                if self.com_id_dict[com] != id(self.tast_set[com].cur_scene):
                    self.signal_change.emit(com)
                    self.com_id_dict[com] = id(self.tast_set[com].cur_scene)
                else:
                    if self.tast_set[com].cur_scene == None:
                        self.signal_change.emit(com)
                        self.monitor_com_list.remove(com)
                        break
            except:
                self.monitor_com_list.remove(com)
                continue
        if len(self.monitor_com_list) == 0:
            self.flag = False
        else:
            sleep(0.3)



# class manager_exec(QThread):
#     signal_change = pyqtSignal(str)
#
#     def __init__(self, tast_set,com_list):
#         super(QThread, self).__init__()
#         self.tast_set = tast_set
#         self.com_list = com_list
#
#     def run(self):
#         state_dict = dict()
#         com_id_dict = dict()
#         com_list = list(self.com_list)
#         for com in self.com_list:
#             while True:
#                 if self.tast_set[com].cur_scene == None:
#                     sleep(0.3)
#                 else:
#                     break
#             state_dict[com] = self.tast_set[com].cur_scene.state
#             com_id_dict[com] = id(self.tast_set[com].cur_scene)
#             self.signal_change.emit(com)
#         while True:
#             # print('cur_scene_state:' + self.tast_set['com7'])
#             for com in com_list:
#                 try:
#                     # logging.debug('com:' + com + ',cur_scene_state:' + self.tast_set[com].cur_scene.state)
#                     if com_id_dict[com] != id(self.tast_set[com].cur_scene):
#                         self.signal_change.emit(com)
#                         com_id_dict[com] = id(self.tast_set[com].cur_scene)
#                     else:
#                         if self.tast_set[com].cur_scene == None:
#                             self.signal_change.emit(com)
#                             com_list.remove(com)
#                             break
#                 except:
#                     com_list.remove(com)
#                     break
#             if len(com_list) == 0:
#                 break
#             else:
#                 sleep(0.3)
#         self.exit()


