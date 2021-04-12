import os

from view.source import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow
import sys
from utils import log
from model.device_choose_connect_model import device_chooose_connect
from model.creat_scene_view import create_scene_view
from model.ali_QThread import sceneOneCheck
from model.debug_tootip import debug_tootip
from utils.config_utils import read_config
import constant
from PyQt5.QtGui import QIcon

from task import scene_tv, checker as ck, device as dv, scene as sc
from model.loading import loading
from PyQt5.QtCore import Qt,pyqtSignal, QPoint
from model.toast import toast
class model_scene_ScenceTV(Ui_MainWindow, QMainWindow):
    off_open_list = pyqtSignal()
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())
        self.attribute_init()
        self.choice_list = [self.checkBox_8, self.checkBox, self.checkBox_2,
                            self.checkBox_3, self.checkBox_4, self.checkBox_20,
                            self.checkBox_15, self.checkBox_17, self.checkBox_18]
        self.choice_dict = {"HDMI1": False, "HDMI2": False, "HDMI3": False, "ATV": False,
                              "DTMB": False, "蓝牙音箱是否回连成功": False, "近场唤醒是否成功": False,
                              "遥控器是否回连成功": False, "远场唤醒是否成功": False}
        self.buttton_init()

    def open_scene_list(self):
        self.off_open_list.emit()
        self.close()

    def attribute_init(self):
        self.device_choice_ui = None
        self.create_scene_view = None
        self.a2dp_mac = None
        default_config = read_config(constant.CONFIG_FILE)
        self.channel_switch_interval = default_config['scene_tv']['channel_switch_interval']['val']*3600
        self.performance_interval = default_config['scene_tv']['performance_interval']['val']*3600
        self.performance_str = ''
        self.check_interval = default_config['scene_tv']['check_interval']['val']*3600

    def buttton_init(self):
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle('信源检测')
        # icon = QIcon(constant.all_icon)
        # self.setWindowIcon(icon)
        self.setWindowIcon(QIcon(os.path.join(constant.SRC_ROOT, 'icon', '信源检测.ico')))
        from PyQt5.QtGui import QFont
        self.lineEdit.setFont(QFont("宋体", 14, QFont.Normal))
        self.lineEdit_2.setFont(QFont("宋体", 14, QFont.Normal))
        self.lineEdit_3.setFont(QFont("宋体", 14, QFont.Normal))
        self.lineEdit_5.setFont(QFont("宋体", 9, QFont.Normal))
        self.lineEdit_4.setFont(QFont("宋体", 14, QFont.Normal))
        self.lineEdit_5.setHidden(True)
        self.lineEdit.setPlaceholderText(str(self.channel_switch_interval/3600))
        self.lineEdit_2.setPlaceholderText(str(self.performance_interval/3600))
        self.lineEdit_3.setPlaceholderText(str(self.check_interval/3600))
        self.label_11.setHidden(True)
        self.label_12.setHidden(True)
        self.label_13.setHidden(True)
        self.pushButton_2.clicked.connect(lambda: self.jump_connect(self.pushButton_2.text()))
        for clickbox in self.choice_list:
            clickbox.setStyleSheet('')
            clickbox.stateChanged.connect(lambda: self.choice_checkbox(self.sender(), self.sender().text()))
        self.pushButton_8.clicked.connect(lambda: self.check_TV_scene(self.pushButton_8.text()))
        self.pushButton_7.clicked.connect(lambda: self.check_TV_scene(self.pushButton_7.text()))

    def choice_checkbox(self, checkbox, text):
        if checkbox.isChecked():
            self.choice_dict[text] = True
        else:
            self.choice_dict[text] = False
    def message(self, title, text):
        newMessagebox = QMessageBox(self)
        newMessagebox.setText('\r\r\r'+text+'\r\r\r')
        newMessagebox.setWindowTitle(title)
        newMessagebox.setIcon(1)
        newMessagebox.setStyleSheet('QMessageBox{background-color:rgb(240,240,240)}')
        newMessagebox.setStandardButtons(QMessageBox.Yes)
        newMessagebox.exec()


    def check_TV_scene(self, value):
        if not True in list(self.choice_dict.values())[0:5]:
            self.message('提示', '请勾选带*号的必选项：信源选择')
            return
        # if self.choice_dict["蓝牙音箱是否回连成功"]:
        #     if not self.lineEdit_5.text():
        #         self.message('提示', '请输入蓝牙Mac地址！')
        #         return
        #     else:
        #         self.a2dp_mac = self.lineEdit_5.text()
        if self.lineEdit.text() != "":
            try:
                if self.lineEdit.text().isdigit():
                    self.channel_switch_interval = float(self.lineEdit.text())*3600
                else:
                    self.channel_switch_interval = float(self.lineEdit.text())*3600
            except:
                self.lineEdit.clear()
                self.label_11.setHidden(False)
                return

        if self.lineEdit_2.text() != "":
            try:
                self.performance_interval = float(self.lineEdit_2.text())*60
            except:
                self.lineEdit_2.clear()
                self.label_13.setHidden(False)
                return

        if self.lineEdit_3.text() != "":
            try:
                self.check_interval = float(self.lineEdit_3.text())*60
            except:
                self.lineEdit_3.clear()
                self.label_12.setHidden(False)
                return

        self.performance_str = self.lineEdit_4.text() if self.lineEdit_4.text() else ''
        if value == "一键调试":
            if self.view_close(self.device_choice_ui):
                return
            self.device_choice_ui = device_chooose_connect(self)
            self.device_choice_ui.device_list_signal.connect(self.create_scene_TV)
            self.device_choice_ui.show()
        else:
            if self.view_close(self.create_scene_view):
                return
            self.create_scene_view = create_scene_view('time', parent=self)
            self.create_scene_view.scene_information.connect(self.create_scene_TV)
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

    def create_scene_TV(self,devices_list, scene_name,exec_times):
        this_checker = ck.Checker(
            blue_controller=self.choice_dict["遥控器是否回连成功"],
            blue_speaker=self.choice_dict["蓝牙音箱是否回连成功"],
            near=self.choice_dict["近场唤醒是否成功"],
            far=self.choice_dict["远场唤醒是否成功"],
            # a2dp_mac=self.a2dp_mac
        )
        chanel_list = []
        for channel in ['HDMI1','HDMI2','HDMI3','ATV','DTMB']:
            if self.choice_dict[channel] == True:
                chanel_list.append(channel)

        if len(devices_list) == 0:
            self.SceneTV = scene_tv.SceneTV(
                name=scene_name,
                exec_time=exec_times,
                by=sc.BY_TIME,
                checker=this_checker,
                channel_list=chanel_list,
                channel_switch_interval=self.channel_switch_interval,
                performance_interval=self.performance_interval,
                check_interval=self.check_interval,
                performance_str=self.performance_str
            )
            self.SceneTV.save()
            self.attribute_init()
            self.creat_success_toast = toast(parent=self, text='信源压测场景\n创建成功！')
            self.creat_success_toast.move(QPoint(self.geometry().left() + self.width() * 0.3, self.geometry().top() + self.height() * 0.3))
            self.creat_success_toast.ocl_signal.connect(self.open_scene_list)
            self.creat_success_toast.exec()
        else:
            self.SceneTV = scene_tv.SceneTV(
                name="信源煲机",
                exec_time=1,
                checker=this_checker,
                channel_list=chanel_list,
                channel_switch_interval=self.channel_switch_interval,
                performance_interval=self.performance_interval,
                check_interval=self.check_interval,
                performance_str=self.performance_str
            )
            self.attribute_init()
            self.SceneTV.device = dv.Device(devices_list[0][0], devices_list[0][1])
            self.checkscene = sceneOneCheck(self.SceneTV)
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

    def jump_connect(self, text):
        if text == "信源煲机":
            self.tabWidget.setCurrentIndex(0)
        else:
            pass


if __name__ == '__main__':
    log.init_logging("", output=True)
    app = QtWidgets.QApplication(sys.argv)  # 外部参数列表
    ui = model_scene_ScenceTV()
    ui.show()
    sys.exit(app.exec_())