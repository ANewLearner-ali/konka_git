import os

from view.monkey import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QButtonGroup
import sys
from utils import log
from model.device_choose_connect_model import device_chooose_connect
from model.creat_scene_view import create_scene_view
from utils.config_utils import read_config
import constant
from PyQt5.QtGui import QIcon
from model.loading import loading
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from model.toast import toast
from task import scene_monkey, checker as ck, device as dv, scene as sc
from model.ali_QThread import sceneOneCheck
from model.debug_tootip import debug_tootip


class model_scene_monkey(Ui_MainWindow, QMainWindow):
    off_open_list = pyqtSignal()

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())
        self.default_config = read_config(constant.CONFIG_FILE)
        self.mode = 0
        self.attribute_init()
        self.monkeyGlobal_list = [self.checkBox_23, self.checkBox_18, self.checkBox_15, self.checkBox_24
                              , self.checkBox_16, self.checkBox_21, self.checkBox_20]
        self.monkeyGlobal_dict = {"远场唤醒是否成功": False, "网络连接是否正常": False, "近场唤醒是否成功": False, "蓝牙音箱是否回连成功": False,
                              "USB挂载正常,U盘个数：": False, "摄像头是否正常": False, "遥控器是否回连成功": False}


        self.monkeyLogic_list = [self.checkBox_19, self.checkBox_17, self.checkBox_22, self.checkBox_35
            , self.checkBox_36, self.checkBox_37, self.checkBox_38]
        self.monkeyLogic_dict = {"近场语音是否唤醒正常": False, "网络连接是否正常": False, "远场语音是否唤醒正常": False, "摄像头是否正常": False,
                                  "蓝牙遥控器是否回连成功": False, "蓝牙音箱是否回连成功": False, "USB挂载正常,U盘个数：": False}

        self.buttton_init()

    def open_scene_list(self):
        self.off_open_list.emit()
        self.close()

    def message(self, title, text):
        newMessagebox = QMessageBox(self)
        newMessagebox.setText('\r\r\r'+text+'\r\r\r')
        newMessagebox.setWindowTitle(title)
        newMessagebox.setIcon(1)
        newMessagebox.setStyleSheet('QMessageBox{background-color:rgb(240,240,240)}')
        newMessagebox.setStandardButtons(QMessageBox.Yes)
        newMessagebox.exec()

    def attribute_init(self):
        self.usb_count = 1
        self.a2dp_mac = None
        self.packages = ''
        self.global_check_interval = self.default_config['scene_monkey_global']['check_interval']['val']
        self.check_interval = self.default_config['scene_monkey_logic']['check_interval']['val']
        self.switch_interval = self.default_config['scene_monkey_logic']['switch_interval']['val']
        self.device_choice_ui = None
        self.create_scene_view = None


    def buttton_init(self):
        self.radioButton_5.setText('固定逻辑：launcher-电视家-全网搜索-在线音乐-本地音乐视频图片混播（30s）-内置在线视频')
        self.setAttribute(Qt.WA_DeleteOnClose)
        from PyQt5.QtGui import QFont
        self.lineEdit_7.setFont(QFont("宋体", 11, QFont.Normal))
        self.lineEdit_4.setFont(QFont("宋体", 14, QFont.Normal))
        self.lineEdit_3.setFont(QFont("宋体", 14, QFont.Normal))
        self.lineEdit_5.setFont(QFont("宋体", 14, QFont.Normal))
        self.lineEdit_9.setFont(QFont("宋体", 14, QFont.Normal))
        self.lineEdit_8.setFont(QFont("宋体", 14, QFont.Normal))
        self.lineEdit_8.setHidden(True)
        self.lineEdit_3.setHidden(True)
        self.setWindowTitle('Monkey压测')
        # icon = QIcon(constant.all_icon)
        # self.setWindowIcon(icon)
        self.setWindowIcon(QIcon(os.path.join(constant.SRC_ROOT, 'icon', '系统可靠性.ico')))
        self.label_12.setHidden(True)

        self.lineEdit_7.setPlaceholderText('有启动图标的应用输入包名,无启动图标的输入mainActivty,多个应用用;分割')
        self.pushButton_2.clicked.connect(lambda: self.jump_connect(self.pushButton_2.text()))
        self.pushButton_3.clicked.connect(lambda: self.jump_connect(self.pushButton_3.text()))
        for clickbox in self.monkeyGlobal_list:
            clickbox.stateChanged.connect(lambda: self.monkeyGlobal_checkbox(self.sender(), self.sender().text()))
        for clickbox2 in self.monkeyLogic_list:
            clickbox2.stateChanged.connect(lambda: self.monkeyLogic_checkbox(self.sender(), self.sender().text()))

        self.pushButton_8.clicked.connect(lambda: self.check_monkeyglobal_scene(self.pushButton_8.text()))
        self.pushButton_7.clicked.connect(lambda: self.check_monkeyglobal_scene(self.pushButton_7.text()))

        self.pushButton_10.clicked.connect(lambda: self.check_monkeylogic_scene(self.pushButton_10.text()))
        self.pushButton_9.clicked.connect(lambda: self.check_monkeylogic_scene(self.pushButton_9.text()))

        self.monkeymode = QButtonGroup()
        self.monkeymode.addButton(self.radioButton_5, 0)
        self.monkeymode.addButton(self.radioButton_6, 1)
        self.monkeymode.buttonClicked[int].connect(self.set_mode)

    def set_mode(self, int):
        if int == 0:
            self.mode = 1
        else:
            self.mode = 2


    def monkeyGlobal_checkbox(self, checkbox, text):
        if checkbox.isChecked():
            self.monkeyGlobal_dict[text] = True
        else:
            self.monkeyGlobal_dict[text] = False
    def monkeyLogic_checkbox(self, checkbox, text):
        if checkbox.isChecked():
            self.monkeyLogic_dict[text] = True
        else:
            self.monkeyLogic_dict[text] = False

    def check_monkeyglobal_scene(self, value):
        if self.lineEdit.text() == '':
            QMessageBox.information(None, '提示', '请填写带*号的必选项：压测命令', QMessageBox.Yes)
            return
        else:
            if self.lineEdit.text().split(' ')[0] != 'monkey':
                QMessageBox.information(None, '提示', '请填写正确的monkey压测命令:monkey开头的xxxxxx', QMessageBox.Yes)
                return

        if self.monkeyGlobal_dict["USB挂载正常,U盘个数："]:
            if not self.lineEdit_4.text().isdigit():
                self.message('提示', 'U盘个数：请输入数字！')
                return
            else:
                self.usb_count = int(self.lineEdit_4.text())


        if value == "一键调试":
            if self.view_close(self.device_choice_ui):
                return
            self.device_choice_ui = device_chooose_connect(self)
            self.device_choice_ui.device_list_signal.connect(self.create_monkeyglobal_scene)
            self.device_choice_ui.show()
        else:
            if self.view_close(self.create_scene_view):
                return
            self.create_scene_view = create_scene_view('time', parent=self)
            self.create_scene_view.scene_information.connect(self.create_monkeyglobal_scene)
            self.create_scene_view.show()

    def view_close(self, view):
        try:
            if view != None:
                if view.isVisible():
                    return True
                else:
                    view.close()
                    return False
        except:
            return False

    def check_monkeylogic_scene(self, value):
        if self.monkeymode.checkedId() == -1:
            QMessageBox.information(None, '提示', '请勾选逻辑测试的模式：固定/自定义：', QMessageBox.Yes)
            return
        else:
            if self.monkeymode.checkedId() == 1:
                if self.lineEdit_7.text() == '':
                    QMessageBox.information(None, '提示', '请输入需执行的包名，以分号;区分', QMessageBox.Yes)
                    return
                else:
                    self.packages = self.lineEdit_7.text()
        if self.lineEdit_5.text() != "":
            try:
                self.switch_interval = float(self.lineEdit_5.text())*3600
            except:
                self.lineEdit_5.clear()
                self.label_12.setHidden(False)
                return

        if self.monkeyLogic_dict["USB挂载正常,U盘个数："]:
            if not self.lineEdit_9.text().isdigit():
                self.message('提示', 'U盘个数：请输入数字！')
                return
            else:
                self.usb_count = int(self.lineEdit_9.text())

        if value == "一键调试":
            if self.view_close(self.device_choice_ui):
                return
            self.device_choice_ui = device_chooose_connect(self)
            self.device_choice_ui.device_list_signal.connect(self.create_monkeylogic_scene)
            self.device_choice_ui.show()
        else:
            if self.view_close(self.create_scene_view):
                return
            self.create_scene_view = create_scene_view('time',parent=self)
            self.create_scene_view.scene_information.connect(self.create_monkeylogic_scene)
            self.create_scene_view.show()
    def create_monkeyglobal_scene(self,devices_list, scene_name,exec_times):
        this_checker = ck.Checker(
            camera=self.monkeyGlobal_dict["摄像头是否正常"],
            usb=self.monkeyGlobal_dict["USB挂载正常,U盘个数："],
            far=self.monkeyGlobal_dict["远场唤醒是否成功"],
            net=self.monkeyGlobal_dict['网络连接是否正常'],
            near=self.monkeyGlobal_dict["近场唤醒是否成功"],
            blue_speaker=self.monkeyGlobal_dict['蓝牙音箱是否回连成功'],
            blue_controller=self.monkeyGlobal_dict['遥控器是否回连成功'],
            usb_count=self.usb_count,
            # a2dp_mac=self.a2dp_mac
        )
        if len(devices_list) == 0:
            self.monkeyglobal_scene = scene_monkey.SceneMonkeyGlobal(
                name=scene_name,
                exec_time=exec_times,
                by=sc.BY_TIME,
                checker=this_checker,
                cmd=self.lineEdit.text(),
                check_interval=self.global_check_interval,

            )
            self.monkeyglobal_scene.save()
            self.attribute_init()
            self.creat_success_toast = toast(parent=self, text='全局Monkey场景\n创建成功！')

            self.creat_success_toast.move(QPoint(self.geometry().left() + self.width() * 0.3, self.geometry().top() + self.height() * 0.3))
            self.creat_success_toast.ocl_signal.connect(self.open_scene_list)
            self.creat_success_toast.exec()
        else:
            self.monkeyglobal_scene = scene_monkey.SceneMonkeyGlobal(
                name="全局monkey",
                exec_time=1,
                checker=this_checker,
                cmd=self.lineEdit.text(),
                check_interval=self.global_check_interval
            )
            self.attribute_init()
            self.monkeyglobal_scene.device = dv.Device(devices_list[0][0], devices_list[0][1])
            self.checkscene = sceneOneCheck(self.monkeyglobal_scene)
            self.checkscene.reflash_sig.connect(self.showlog)
            self.checkscene.dependent_check_sig.connect(self.check_message)
            self.checkscene.start()


    def showlog(self):
        self.debug_tootip = debug_tootip(self)
        self.debug_tootip.move(self.width() * 0.3, self.height() * 0.3)
        self.debug_tootip.exec()


    def check_message(self, check):
        self.message('依赖检查', check)

    def inform_text(self, string):
        if string == 'begin':
            self.loading = loading(self)
            self.loading.label_2.setText('调试中，请等待')
            self.loading.move(self.width()*0.45, self.height()*0.45)
            self.loading.exec()
        if string == 'FAIL':
            self.loading.label_2.setText('执行失败')
            self.loading.close()
            QMessageBox.information(self, '提示', '执行失败', QMessageBox.Yes)
            return
        if string == 'FINISH':
            self.loading.label_2.setText('执行成功')
            self.loading.close()
            QMessageBox.information(self, '提示', '执行完成', QMessageBox.Yes)
            return
    def create_monkeylogic_scene(self,devices_list, scene_name,exec_times):
        this_checker = ck.Checker(
            camera=self.monkeyLogic_dict["摄像头是否正常"],
            usb=self.monkeyLogic_dict["USB挂载正常,U盘个数："],
            far=self.monkeyLogic_dict["远场语音是否唤醒正常"],
            net=self.monkeyLogic_dict['网络连接是否正常'],
            near=self.monkeyLogic_dict["近场语音是否唤醒正常"],
            blue_speaker=self.monkeyLogic_dict['蓝牙音箱是否回连成功'],
            blue_controller=self.monkeyLogic_dict['蓝牙遥控器是否回连成功'],
            usb_count=self.usb_count,
            # a2dp_mac=self.a2dp_mac
        )
        if len(devices_list) == 0:
            self.monkeylogic_scene = scene_monkey.SceneMonkeyLogic(
                name=scene_name,
                exec_time=exec_times,
                by=sc.BY_TIME,
                mode=self.mode,
                checker=this_checker,
                switch_interval=self.switch_interval,
                check_interval=self.check_interval,
                packages=self.packages
            )
            self.monkeylogic_scene.save()
            self.attribute_init()
            self.creat_success_toast = toast(parent=self, text='逻辑Monkey场景\n创建成功！')
            self.creat_success_toast.move(QPoint(self.geometry().left() + self.width() * 0.3, self.geometry().top() + self.height() * 0.3))
            self.creat_success_toast.ocl_signal.connect(self.open_scene_list)
            self.creat_success_toast.exec()
        else:
            self.monkeylogic_scene = scene_monkey.SceneMonkeyLogic(
                name="逻辑monkey",
                exec_time=1,
                mode=self.mode,
                checker=this_checker,
                switch_interval=self.switch_interval,
                check_interval=self.check_interval,
                packages=self.packages
            )
            self.attribute_init()
            self.monkeylogic_scene.device = dv.Device(devices_list[0][0], devices_list[0][1])
            self.checkscene = sceneOneCheck(self.monkeylogic_scene)
            self.checkscene.reflash_sig.connect(self.showlog)
            self.checkscene.dependent_check_sig.connect(self.check_message)
            self.checkscene.start()

    def jump_connect(self, str):
        if str.strip() == "Monkey全局测试":
            self.tabWidget.setCurrentIndex(0)
            self.pushButton_2.setStyleSheet("background: #1890FF;")
            self.pushButton_3.setStyleSheet("background: #000C17;")
            self.label_12.setHidden(True)
        elif str.strip() == "Monkey逻辑测试":
            self.pushButton_3.setStyleSheet("background: #1890FF;")
            self.pushButton_2.setStyleSheet("background: #000C17;")
            self.tabWidget.setCurrentIndex(1)
            self.label_12.setHidden(True)
        else:
            pass

if __name__ == '__main__':
    log.init_logging("", output=True)
    app = QtWidgets.QApplication(sys.argv)  # 外部参数列表
    ui = model_scene_monkey()
    ui.show()
    sys.exit(app.exec_())