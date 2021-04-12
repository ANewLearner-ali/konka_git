import os
import time
import traceback

from PyQt5.QtCore import QSize

from model.new_base import RUNQPushButton, SpecificQHLayout, SpecificQVLayout
from model.script_debug_tootip import script_debug_tootip
from model.ali_QThread import script_run
from task.device import Device

from view.main_ui2 import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QHBoxLayout, QWidget, QSizePolicy, QSpacerItem
import sys
from model.model_on_and_off import model_on_and_off
from model.model_scene_media import model_scene_media
from model.model_scene_monkey import model_scene_monkey
from model.model_scene_wake import model_scene_wake
from model.model_scene_SceneTV import model_scene_ScenceTV
from model.model_scene_task_view import model_sence_task_view
from model.model_task_manager_view import model_task_manager_view
from model.model_scene_recorder import model_scene_recorder
from task.task_manager import manager
from PyQt5.QtGui import QIcon
import constant
import logging
from PyQt5.Qt import Qt


class Entrance_View(Ui_MainWindow, QMainWindow):
    view_title_list = ['task_manager_view']

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self._setup_my_style()
        self._view_init()
        self.setWindowTitle('平台可靠性压测工具')
        icon = QIcon(constant.all_icon)
        self.setWindowIcon(icon)
        self.centralWidget().setAutoFillBackground(True)
        # self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        # self.setFixedSize(self.width(), self.height())
        self._text_init()
        self._signal_init()

        self.view_dict = dict()
        for view in self.view_title_list:
            self.view_dict[view] = None

    def _setup_my_style(self):

        def get_layout(button_list):
            row_layout = SpecificQHLayout()
            if len(button_list) == 1:
                row_layout.addSpacerItem(QSpacerItem(333, 0, QSizePolicy.Preferred))
                row_layout.addWidget(button_list[0])
                row_layout.addSpacerItem(QSpacerItem(331, 0, QSizePolicy.Preferred))
                return row_layout
            row_layout.addSpacerItem(QSpacerItem(81, 0, QSizePolicy.Preferred))
            for button in button_list:
                row_layout.addWidget(button)
                row_layout.addSpacerItem(QSpacerItem(72, 0, QSizePolicy.Preferred))
            return row_layout
        self.btn_switch = RUNQPushButton("开关机检测", min_size=(180, 100), max_size=(360, 202),
                                         style=2, shadow=1, my_policy=QSizePolicy.Expanding)
        self.btn_source = RUNQPushButton("信源检测", min_size=(180, 100), max_size=(360, 202),
                                         style=2, shadow=1, my_policy=QSizePolicy.Expanding)
        self.btn_wake = RUNQPushButton("待机检测", min_size=(180, 100), max_size=(360, 202),
                                         style=2, shadow=1, my_policy=QSizePolicy.Expanding)
        self.btn_media = RUNQPushButton("多媒体兼容", min_size=(180, 100), max_size=(360, 202),
                                         style=2, shadow=1, my_policy=QSizePolicy.Expanding)
        self.btn_monkey = RUNQPushButton("Monkey压测", min_size=(180, 100), max_size=(360, 202),
                                         style=2, shadow=1, my_policy=QSizePolicy.Expanding)
        self.btn_recorder = RUNQPushButton("脚本录制", min_size=(180, 100), max_size=(360, 202),
                                         style=2, shadow=1, my_policy=QSizePolicy.Expanding)
        self.btn_switch_pressure = RUNQPushButton("开关机压测", min_size=(180, 100), max_size=(360, 202),
                                         style=2, shadow=1, my_policy=QSizePolicy.Expanding)
        for button in [self.btn_switch, self.btn_source, self.btn_wake, self.btn_media, self.btn_monkey, self.btn_recorder, self.btn_switch_pressure]:
            button.setIcon(QIcon(os.path.join(constant.SRC_ROOT, 'icon', button.text() + '.svg')))
            button.setIconSize(QSize(40, 40))
            button.setText('  ' + button.text())
        top_layout = SpecificQHLayout()
        top_layout.addSpacerItem(QSpacerItem(19, 0, QSizePolicy.Preferred))
        top_layout.addWidget(self.lb_effectanalysis)
        top_layout.addSpacerItem(QSpacerItem(303, 0, QSizePolicy.Preferred))
        top_layout.addWidget(self.btn_script)
        self.btn_script.setFixedSize(80, 30)
        self.btn_scene_list.setFixedSize(80, 30)
        self.btn_task_list.setFixedSize(80, 30)
        top_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Preferred))
        top_layout.addWidget(self.btn_scene_list)
        top_layout.addSpacerItem(QSpacerItem(20, 0, QSizePolicy.Preferred))
        top_layout.addWidget(self.btn_task_list)
        top_layout.addSpacerItem(QSpacerItem(31, 0, QSizePolicy.Preferred))
        top_widget = QWidget()
        top_widget.setObjectName('main_top_widget')
        top_widget.setStyleSheet("QWidget#main_top_widget { border-image:url(:/img/4.svg)}")
        top_widget.setLayout(top_layout)
        top_widget.setFixedHeight(105)
        help_layout = SpecificQHLayout()
        help_layout.addStretch()
        help_layout.addWidget(self.btn_help)
        self.btn_help.setIcon(QIcon(os.path.join(constant.SRC_ROOT, 'icon', '使用指引.svg')))
        self.btn_help.setIconSize(QSize(13, 13))
        help_layout.addSpacerItem(QSpacerItem(25, 0, QSizePolicy.Preferred))
        down_layout = QHBoxLayout()
        down_layout.addStretch()
        down_layout.addWidget(self.label_version)
        down_layout.addSpacing(20)
        all_layout = SpecificQVLayout()
        all_layout.addWidget(top_widget)
        all_layout.addSpacerItem(QSpacerItem(0, 12, vPolicy=QSizePolicy.Maximum))
        all_layout.addLayout(help_layout)
        all_layout.addSpacerItem(QSpacerItem(0, 45, QSizePolicy.Preferred))
        all_layout.addLayout(get_layout([self.btn_switch, self.btn_wake, self.btn_monkey]))
        all_layout.addSpacerItem(QSpacerItem(0, 32, QSizePolicy.Preferred))
        all_layout.addLayout(get_layout([self.btn_media, self.btn_source, self.btn_recorder]))
        all_layout.addSpacerItem(QSpacerItem(0, 32, QSizePolicy.Preferred))
        all_layout.addLayout(get_layout([self.btn_switch_pressure]))
        all_layout.addSpacerItem(QSpacerItem(0, 32, QSizePolicy.Preferred))
        all_layout.addLayout(down_layout)
        all_layout.addSpacerItem(QSpacerItem(0, 20, QSizePolicy.Preferred))
        self.centralWidget().setLayout(all_layout)
        # singnal
        self.btn_help.clicked.connect(self._new_button_click)
        self.btn_switch_pressure.clicked.connect(self._new_button_click)

    def _new_button_click(self):
        if self.sender().text() == '使用指引':
            from utils.thread_utils import RunExeThread
            import os
            self.thread = RunExeThread(os.path.join(constant.SRC_ROOT, '可靠性工具.docx'))
            self.thread.start()
        else:
            from utils.thread_utils import RemindThread
            from model.loading import loading
            import os
            exe_path = os.path.join(constant.BASE_ROOT.rsplit('\\', 1)[0], 'SwitchTool', 'SwitchTool.exe')
            exe_path = exe_path.rsplit('\\', 1)
            if not self.loading:
                self.loading = loading(self)
                self.loading.label_2.setText('开关机工具启动中...')
                self.loading.move(self.width() * 0.45, self.height() * 0.45)
            else:
                self.loading.setText('开关机工具启动中...')
                self.loading.setVisible(True)
            cmd = 'cd /d ' + exe_path[0] + ' & start ' + exe_path[1] + ' &'
            self.remind_thread = RemindThread(cmd, 'success', exe_path[1])
            self.remind_thread.exec_down.connect(self.show_debug)
            self.remind_thread.start()
            self.loading.exec()


    def _text_init(self):
        self.label_version.setText(constant.VERSION)
        self.btn_script.setToolTip('请确认工具目录/src/test.txt文件存在再点击')

    def _signal_init(self):
        # self.btn_task_list.setText('任务列表')
        self.btn_switch.clicked.connect(self.open_model_on_and_off)
        self.btn_source.clicked.connect(self.open_model_scene_ScenceTV)
        self.btn_media.clicked.connect(self.open_model_scene_media)
        self.btn_wake.clicked.connect(self.open_model_scene_wake)
        self.btn_monkey.clicked.connect(self.open_model_scene_monkey)
        self.btn_scene_list.clicked.connect(self.open_model_scene_list)
        self.btn_task_list.clicked.connect(self.open_mode_task)
        self.btn_recorder.clicked.connect(self.open_model_scene_recorder)
        self.btn_script.clicked.connect(self.script_devices_connect)

    def _view_init(self):
        self.model_on_and_off = None
        self.model_scene_ScenceTV = None
        self.model_scene_media = None
        self.model_scene_wake = None
        self.model_scene_monkey = None
        self.model_scene_recorder = None
        self.model_scene_list = None
        self.model_task_manager = None
        self.model_device_connect = None
        self.loading = None

    def script_devices_connect(self):
        self.view_close(self.model_device_connect)
        from model.device_choose_connect_model import device_chooose_connect
        self.model_device_connect = device_chooose_connect(self)
        self.model_device_connect.device_list_signal.connect(self.script_run)
        self.model_device_connect.show()

    def script_run(self, devices_list, isopen, msg1):
        file_name = os.path.join(constant.SRC_ROOT, 'test.txt')
        if not os.path.isfile(file_name):
            self.message('提示', 'src目录下不存在test.txt文件，请检查')
            return
        if isopen == 'True':
            if devices_list[0][0] in manager.com_list:
                state = manager.task_set[devices_list[0][0]].state
                if state == "RUNNING" or state == "PREPARE":
                    self.message('提示', f'该电视已经有任务正在执行，请更换其它电视调试')
                    return
            from utils.tv_utlils import check_tv_com
            res, msg = check_tv_com(devices_list[0][0])
            if res is False:
                self.message('提示', f'{msg}，请检查')
                return
        device = Device(tv_com=devices_list[0][0], mcu_com=devices_list[0][1])
        self.script_thread = script_run(file_name, device, isopen)
        self.script_thread.msg_signal.connect(self.showlog)
        self.script_thread.start()

    def showlog(self):
        self.debug_tootip = script_debug_tootip()
        self.debug_tootip.move(self.width()*0.5, self.height()*0.5)
        self.debug_tootip.exec()

    def show_debug(self, msg):
        if msg == 'success':
            self.loading.close()
            self.loading = None
        elif msg == '脚本调试中...' or msg == '脚本调试成功':
            if self.loading != None:
                self.loading.label_2.setText(msg)
            else:
                from model.loading import loading
                self.loading = loading(self)
                self.loading.label_2.setText(msg)
                self.loading.move(self.width() * 0.45, self.height() * 0.45)
                self.loading.exec()
        else:
            self.loading.close()
            self.loading = None
            self.message('脚本异常提示', msg)

    def message(self, title, text):
        newMessagebox = QMessageBox(self)
        newMessagebox.setStyleSheet('background-image: url();')
        newMessagebox.setText('\r\r\r' + text + '\r\r\r')
        newMessagebox.setWindowTitle(title)
        newMessagebox.setStyleSheet('QMessageBox{background-color:rgb(240,240,240)}')
        newMessagebox.setStandardButtons(QMessageBox.Yes)
        newMessagebox.exec()

    def open_mode_task(self):
        try:
            logging.debug('open_model_task: check start-----{}'.format(time.time()))
            if len(manager.com_list) == 0:
                self.message('提示', '任务未执行，无法打开！！')
                return
            self.view_close(self.model_task_manager)
            self.model_task_manager = model_task_manager_view(manager)
            self.model_task_manager.show()
        except:
            print(traceback.format_exc())

    def open_model_scene_list(self):
        self.view_close(self.model_scene_list)
        self.model_scene_list = model_sence_task_view()
        self.model_scene_list.open_task_signal.connect(self.open_mode_task)
        self.model_scene_list.show()

    def open_model_on_and_off(self):
        self.view_close(self.model_on_and_off)
        self.model_on_and_off = model_on_and_off()
        self.model_on_and_off.off_open_list.connect(self.open_model_scene_list)
        self.model_on_and_off.show()

    def open_model_scene_ScenceTV(self):
        self.view_close(self.model_scene_ScenceTV)
        self.model_scene_ScenceTV = model_scene_ScenceTV()
        self.model_scene_ScenceTV.off_open_list.connect(self.open_model_scene_list)
        self.model_scene_ScenceTV.show()

    def open_model_scene_media(self):
        self.view_close(self.model_scene_media)
        self.model_scene_media = model_scene_media()
        self.model_scene_media.off_open_list.connect(self.open_model_scene_list)
        self.model_scene_media.show()

    def open_model_scene_wake(self):
        self.view_close(self.model_scene_wake)
        self.model_scene_wake = model_scene_wake()
        self.model_scene_wake.off_open_list.connect(self.open_model_scene_list)
        self.model_scene_wake.show()

    def open_model_scene_monkey(self):
        self.view_close(self.model_scene_monkey)
        self.model_scene_monkey = model_scene_monkey()
        self.model_scene_monkey.off_open_list.connect(self.open_model_scene_list)
        self.model_scene_monkey.show()

    def view_close(self, view):
        try:
            if view != None:
                view.close()
        except:
            pass

    def open_model_scene_recorder(self):
        self.view_close(self.model_scene_recorder)
        self.model_scene_recorder = model_scene_recorder(self)
        self.model_scene_recorder.off_open_list.connect(self.open_model_scene_list)
        self.model_scene_recorder.show()


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)  # 外部参数列表
    ui = Entrance_View()
    ui.show()
    sys.exit(app.exec_())
