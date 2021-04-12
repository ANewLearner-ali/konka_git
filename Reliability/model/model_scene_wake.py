import os

from view.powerdown import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QButtonGroup
import sys
from utils import log
from model.device_choose_connect_model import device_chooose_connect
from model.creat_scene_view import create_scene_view

import constant
from PyQt5.QtGui import QIcon
from model.loading import loading

from task import scene_wake, checker as ck, dc_wake as dk, device as dv, scene as sc
from PyQt5.QtCore import Qt,pyqtSignal,QPoint
from model.toast import toast
from model.ali_QThread import scene_test,sceneOneCheck
from model.debug_tootip import debug_tootip


class model_scene_wake(Ui_MainWindow, QMainWindow):
    off_open_list = pyqtSignal()

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())
        self.mode = dk.MODE_NORMAL
        self.attribute_init()
        self.dc_list = [self.checkBox_18, self.checkBox_16, self.checkBox_21]
        self.dc_dict = {"待机是否正常": False, "副屏是否正常（外置摄像头保存图片）": False, "开机是否正常": False}

        self.aidc_list = [self.checkBox_19, self.checkBox_17, self.checkBox_22]
        self.aidc_dict = {"待机是否正常": False, "副屏是否正常（外置摄像头保存图片）": False, "开机是否正常": False}
        self.buttton_init()

    def open_scene_list(self):
        self.off_open_list.emit()
        self.close()

    def attribute_init(self):
        self.low_power_mode = False
        self.device_choice_ui = None
        self.create_scene_view = None

    def buttton_init(self):
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.label_2.setHidden(True)
        self.lineEdit.setHidden(True)
        self.setWindowTitle('待机压测')
        self.setWindowIcon(QIcon(os.path.join(constant.SRC_ROOT, 'icon', '待机检测.ico')))
        self.lineEdit.setPlaceholderText('请填写待机标志如:Power Down')
        self.pushButton_2.clicked.connect(lambda: self.jump_connect(self.pushButton_2.text()))
        self.pushButton_3.clicked.connect(lambda: self.jump_connect(self.pushButton_3.text()))

        for clickbox in self.dc_list:
            clickbox.stateChanged.connect(lambda: self.dc_checkbox(self.sender(), self.sender().text()))
        for clickbox2 in self.aidc_list:
            clickbox2.stateChanged.connect(lambda: self.aidc_checkbox(self.sender(), self.sender().text()))

        self.pushButton_8.clicked.connect(lambda: self.dc_scene(self.pushButton_8.text()))
        self.pushButton_7.clicked.connect(lambda: self.dc_scene(self.pushButton_7.text()))

        self.pushButton_10.clicked.connect(lambda: self.aidc_scene(self.pushButton_10.text()))
        self.pushButton_9.clicked.connect(lambda: self.aidc_scene(self.pushButton_9.text()))

        self.mode_choice = QButtonGroup()
        self.mode_choice.addButton(self.radioButton_5, 0)
        self.mode_choice.addButton(self.radioButton_6, 1)
        self.mode_choice.buttonClicked[int].connect(self.set_mode)
    def set_mode(self,int):
        if int == 0:
            self.low_power_mode = True
        else:
            self.low_power_mode = False

    def message(self, title, text):
        newMessagebox = QMessageBox(self)
        newMessagebox.setText('\r\r\r'+text+'\r\r\r')
        newMessagebox.setWindowTitle(title)
        newMessagebox.setIcon(1)
        newMessagebox.setStyleSheet('QMessageBox{background-color:rgb(240,240,240)}')
        newMessagebox.setStandardButtons(QMessageBox.Yes)
        newMessagebox.exec()


    def dc_checkbox(self, checkbox, text):
        if checkbox.isChecked():
            self.dc_dict[text] = True
        else:
            self.dc_dict[text] = False
    def aidc_checkbox(self, checkbox, text):
        if checkbox.isChecked():
            self.aidc_dict[text] = True
        else:
            self.aidc_dict[text] = False

    def dc_scene(self, value):
        if value == "一键调试":
            if self.view_close(self.device_choice_ui):
                return
            self.device_choice_ui = device_chooose_connect(self)
            self.device_choice_ui.device_list_signal.connect(self.create_dc_scene)
            self.device_choice_ui.show()
        else:
            if self.view_close(self.create_scene_view):
                return
            self.create_scene_view = create_scene_view('count',parent=self)
            self.create_scene_view.scene_information.connect(self.create_dc_scene)
            self.create_scene_view.show()

    def aidc_scene(self, value):
        if self.mode_choice.checkedId() == -1:
            self.message('提示', '请勾选带*号的必选项：低功耗')
            return
        if self.radioButton_5.isChecked():
            self.low_power_mode = True
        else:
            self.low_power_mode = False

        if value == "一键调试":
            if self.view_close(self.device_choice_ui):
                return
            self.device_choice_ui = device_chooose_connect(self)
            self.device_choice_ui.device_list_signal.connect(self.create_aidc_scene)
            self.device_choice_ui.show()
        else:
            if self.view_close(self.create_scene_view):
                return
            self.create_scene_view = create_scene_view('count', parent=self)
            self.create_scene_view.scene_information.connect(self.create_aidc_scene)
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

    def create_dc_scene(self,devices_list, scene_name,exec_times):
        this_checker = ck.Checker(
            power_off=self.dc_dict["待机是否正常"],
            sub_screen=self.dc_dict["副屏是否正常（外置摄像头保存图片）"],
            power_on=self.dc_dict["开机是否正常"],

        )
        if len(devices_list) == 0:
            self.scene_dcwake = scene_wake.SceneDCWake(
                name=scene_name,
                exec_time=exec_times,
                by=sc.BY_COUNT,
                checker=this_checker,
                mode=dk.MODE_QUICK
                )
            self.scene_dcwake.save()
            self.attribute_init()
            self.creat_success_toast = toast(parent=self, text='DC待机场景\n创建成功！')
            self.creat_success_toast.move(QPoint(self.geometry().left() + self.width() * 0.3, self.geometry().top() + self.height() * 0.3))
            self.creat_success_toast.ocl_signal.connect(self.open_scene_list)
            self.creat_success_toast.setModal(True)
            self.creat_success_toast.exec()
        else:
            self.scene_dcwake = scene_wake.SceneDCWake(
                name="DC待机",
                exec_time=1,
                checker=this_checker,
                mode=dk.MODE_QUICK
        )
            self.attribute_init()
            self.scene_dcwake.device = dv.Device(devices_list[0][0], devices_list[0][1])
            self.checkscene = sceneOneCheck(self.scene_dcwake)
            self.checkscene.reflash_sig.connect(self.showlog)
            self.checkscene.dependent_check_sig.connect(self.check_message)
            self.checkscene.start()
    def create_aidc_scene(self,devices_list, scene_name,exec_times):
        this_checker = ck.Checker(
            power_off=self.aidc_dict["待机是否正常"],
            sub_screen=self.aidc_dict["副屏是否正常（外置摄像头保存图片）"],
            power_on=self.aidc_dict["开机是否正常"],

        )
        if len(devices_list) == 0:
            self.scene_aiwake = scene_wake.SceneDCWake(
                name=scene_name,
                exec_time=exec_times,
                by=sc.BY_COUNT,
                checker=this_checker,
                mode=dk.MODE_AI,
                low_power_mode=self.low_power_mode
            )
            self.scene_aiwake.save()
            self.attribute_init()
            self.creat_success_toast = toast(parent=self, text='AI待机场景\n创建成功！')
            self.creat_success_toast.move(QPoint(self.geometry().left() + self.width() * 0.3, self.geometry().top() + self.height() * 0.3))
            self.creat_success_toast.ocl_signal.connect(self.open_scene_list)
            self.creat_success_toast.exec()
        else:
            self.scene_aiwake = scene_wake.SceneDCWake(
                name="AiDC待机",
                exec_time=1,
                by=sc.BY_COUNT,
                checker=this_checker,
                mode=dk.MODE_AI,
                low_power_mode=self.low_power_mode
            )
            self.attribute_init()
            self.scene_aiwake.device = dv.Device(devices_list[0][0], devices_list[0][1])
            self.checkscene = sceneOneCheck(self.scene_aiwake)
            self.checkscene.reflash_sig.connect(self.showlog)
            self.checkscene.dependent_check_sig.connect(self.check_message)
            self.checkscene.start()

    def showlog(self):
        self.debug_tootip = debug_tootip(self)
        self.debug_tootip.move(self.width()*0.3, self.height()*0.3)
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
    def jump_connect(self, str):
        if str.strip() == "待机唤醒":
            self.tabWidget.setCurrentIndex(0)
            self.mode = dk.MODE_NORMAL
            self.pushButton_2.setStyleSheet('background: #1890FF;')
            self.pushButton_3.setStyleSheet('background: #000C17;')
        elif str.strip() == "AI待机唤醒":
            self.tabWidget.setCurrentIndex(1)
            self.pushButton_3.setStyleSheet('background: #1890FF;')
            self.pushButton_2.setStyleSheet('background: #000C17;')
        else:
            pass

if __name__ == '__main__':
    log.init_logging("", output=True)
    app = QtWidgets.QApplication(sys.argv)  # 外部参数列表
    ui = model_scene_wake()
    ui.show()
    sys.exit(app.exec_())