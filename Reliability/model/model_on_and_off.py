from view.openAndclose import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,pyqtSignal,QPoint
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QButtonGroup
import sys,os
import constant
from utils import log
from model.device_choose_connect_model import device_chooose_connect
from model.creat_scene_view import create_scene_view
from task import scene_on_and_off, scene_boot_enter, checker as ck, switch as sw, device as dv, scene as sc, scene_recovery

from model.loading import loading
from model.toast import toast

from model.ali_QThread import sceneOneCheck
from model.debug_tootip import debug_tootip


class model_on_and_off(Ui_MainWindow, QMainWindow):
    off_open_list = pyqtSignal()

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())
        self.mode = None
        self.far = None
        self.is_open_Serial = None
        self.is_save_app = None
        self.attribute_init()
        # 定义属性
        self.onAndoff_list = [self.checkBox, self.checkBox_2, self.checkBox_3, self.checkBox_4
                              , self.checkBox_7, self.checkBox_15, self.checkBox_16, self.checkBox_17
            , self.checkBox_18, self.checkBox_20, self.checkBox_21, self.checkBox_19, self.checkBox_22, self.checkBox_23]
        self.onAndoff_list_dict = ["音量+-","频道+-", "五维键", "语音键",
                              "网络是否回连成功", "近场唤醒是否成功", "移动存储设备挂载是否成功,U盘个数：",
                              "遥控器是否回连成功", "远场唤醒是否成功", "蓝牙音箱是否回连成功",
                              "HDMI出图是否成功","内置应用", "第三方应用", "信源"]
        self.onAndoff_dict = {"音量+-": False, "频道+-": False, "五维键": False, "语音键": False,
                              "网络是否回连成功": False, "近场唤醒是否成功": False, "移动存储设备挂载是否成功,U盘个数：": False,
                              "遥控器是否回连成功": False, "远场唤醒是否成功": False, "蓝牙音箱是否回连成功": False,
                              "HDMI出图是否成功": False, "内置应用": False, "第三方应用": False, "信源": False}
        self.recover_list = [self.checkBox_24, self.checkBox_27, self.checkBox_25, self.checkBox_28,
                             self.checkBox_26, self.checkBox_29, self.checkBox_30]

        self.recover_dict = {"检测第三方应用是否存在": False, "launcher进入正常": False, "摄像头驱动是否正常，是否能升降": False, "WiFi驱动是否正常": False,
                              "移动存储设备是否能够成功挂载,U盘个数：": False, "远场语音是否能唤醒": False, "批量安装APK（APK路径：xxx）": False}
        self.buttton_init()

    def buttton_init(self):
        from PyQt5.QtGui import QFont
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.lineEdit.setFont(QFont("宋体", 14, QFont.Normal))
        self.lineEdit_4.setFont(QFont("宋体", 12, QFont.Normal))
        self.lineEdit_2.setFont(QFont("宋体", 14, QFont.Normal))
        self.lineEdit_3.setFont(QFont("宋体", 12, QFont.Normal))
        self.lineEdit_5.setFont(QFont("宋体", 12, QFont.Normal))
        self.lineEdit_6.setFont(QFont("宋体", 12, QFont.Normal))
        self.lineEdit_7.setFont(QFont("宋体", 14, QFont.Normal))
        self.label_10.setText('打开操作脚本路径：工具安装路径/src')
        self.label_18.setText('重置后串口\n是否打开')
        self.setWindowTitle('开关机压测')
        self.setWindowIcon(QIcon(os.path.join(constant.SRC_ROOT, 'icon', '开关机检测.ico')))
        # icon = QIcon(constant.all_icon)
        # self.setWindowIcon(icon)
        self.lineEdit.setPlaceholderText('未配置，请将广告资源放到U盘根目录下，否则不作广告资源替换.')
        # self.lineEdit_4.setPlaceholderText('如勾选，请输入mac地址')
        self.lineEdit_4.setHidden(True)
        self.label_9.setHidden(True)
        self.label_25.setHidden(True)
        self.pushButton_2.clicked.connect(lambda: self.jump_connect(self.pushButton_2.text()))
        self.pushButton_3.clicked.connect(lambda: self.jump_connect(self.pushButton_3.text()))
        self.pushButton_4.clicked.connect(lambda: self.jump_connect(self.pushButton_4.text()))

        self.onmode = QButtonGroup()
        self.onmode.addButton(self.radioButton, 0)
        self.onmode.addButton(self.radioButton_2, 1)
        self.onmode.buttonClicked[int].connect(self.set_onmode)

        self.farmode = QButtonGroup()
        self.farmode.addButton(self.radioButton_5, 0)
        self.farmode.addButton(self.radioButton_6, 1)
        self.farmode.buttonClicked[int].connect(self.set_farmode)

        self.save_app = QButtonGroup()
        self.save_app.addButton(self.radioButton_51, 0)
        self.save_app.addButton(self.radioButton_61, 1)
        self.save_app.buttonClicked[int].connect(self.set_saveapp)

        self.open_Serial = QButtonGroup()
        self.open_Serial.addButton(self.radioButton_8, 0)
        self.open_Serial.addButton(self.radioButton_7, 1)
        self.open_Serial.buttonClicked[int].connect(self.set_openSerial)

        for clickbox in self.onAndoff_list:
            clickbox.stateChanged.connect(lambda: self.onoff_checkbox(self.sender(), self.sender().text()))
        for clickbox2 in self.recover_list:
            clickbox2.stateChanged.connect(lambda: self.recovery_checkbox(self.sender(), self.sender().text()))

        self.pushButton_8.clicked.connect(lambda: self.check_onoff_scene(self.pushButton_8.text()))
        self.pushButton_7.clicked.connect(lambda: self.check_onoff_scene(self.pushButton_7.text()))

        self.pushButton_13.clicked.connect(lambda: self.check_scene_boot_enter(self.pushButton_13.text()))
        self.pushButton_14.clicked.connect(lambda: self.check_scene_boot_enter(self.pushButton_14.text()))

        self.pushButton_10.clicked.connect(lambda: self.check_scene_recovery(self.pushButton_10.text()))
        self.pushButton_9.clicked.connect(lambda: self.check_scene_recovery(self.pushButton_9.text()))

    def attribute_init(self):

        self.waittime = None
        self.boottime = None
        self.usb_count = 1
        self.a2dp_mac = None
        self.ad_root = ''
        self.apk_root = None
        self.device_choice_ui = None
        self.create_scene_view = None


    def onoff_checkbox(self, checkbox, text):
        if checkbox.isChecked():
            self.onAndoff_dict[text] = True
        else:
            self.onAndoff_dict[text] = False


    def recovery_checkbox(self, checkbox, text):
        if checkbox.isChecked():
            self.recover_dict[text] = True
        else:
            self.recover_dict[text] = False

    def message(self, title, text):
        newMessagebox = QMessageBox(self)
        # icon = QIcon(constant.all_icon)
        # newMessagebox.setWindowIcon(icon)
        newMessagebox.setText('\r\r\r'+text+'\r\r\r')
        newMessagebox.setWindowTitle(title)
        newMessagebox.setIcon(1)
        newMessagebox.setStyleSheet('QMessageBox{background-color:rgb(240,240,240)}')
        newMessagebox.setStandardButtons(QMessageBox.Yes)
        newMessagebox.exec()
        return newMessagebox.clickedButton()



    def check_onoff_scene(self, value):
        if self.mode == None:
            if self.message('提示', '请勾选带*号的必选项：开机模式') != QMessageBox.No:
                return

        if self.lineEdit_2.text() == "":
            if self.message('提示', '请填写带*号的必选项：待机等待时间') != QMessageBox.No:
                return
        if self.lineEdit_7.text() == "":
            if self.message('提示', '请填写带*号的必选项：开机等待时间') != QMessageBox.No:
                return
        else:
            if self.lineEdit_2.text().isdigit():
                self.waittime = int(self.lineEdit_2.text())
            else:
                self.lineEdit_2.clear()
                self.label_9.setHidden(False)
                return
            if self.lineEdit_7.text().isdigit():
                self.boottime = int(self.lineEdit_7.text())
            else:
                self.lineEdit_7.clear()
                self.label_25.setHidden(False)
                return
        self.ad_root = self.lineEdit.text() if self.lineEdit.text() else ''
        if self.onAndoff_dict["移动存储设备挂载是否成功,U盘个数："]:
            if not self.lineEdit_3.text().isdigit():
                if self.message('提示', 'U盘个数：请输入数字！') != QMessageBox.No:
                    return
            else:
                self.usb_count = int(self.lineEdit_3.text())

        if value == "一键调试":
            if self.view_close(self.device_choice_ui):
                return
            self.device_choice_ui = device_chooose_connect(self)
            self.device_choice_ui.device_list_signal.connect(self.create_onoff_scene)
            self.device_choice_ui.show()
        else:
            if self.view_close(self.create_scene_view):
                return
            self.create_scene_view = create_scene_view('count', parent=self)
            self.create_scene_view.scene_information.connect(self.create_onoff_scene)
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

    def check_scene_boot_enter(self, button_text):
        if self.onAndoff_dict["内置应用"] == False and self.onAndoff_dict["第三方应用"] == False and self.onAndoff_dict["信源"] == False:
            if self.message('提示', '请勾选一个开机直达应用') != QMessageBox.No:
                return

        if button_text == "一键调试":
            if self.view_close(self.device_choice_ui):
                return
            self.device_choice_ui = device_chooose_connect(self)
            self.device_choice_ui.device_list_signal.connect(self.create_scene_boot_enter)
            self.device_choice_ui.show()
        else:
            if self.view_close(self.create_scene_view):
                return
            self.create_scene_view = create_scene_view('count', parent=self)
            self.create_scene_view.scene_information.connect(self.create_scene_boot_enter)
            self.create_scene_view.show()

    def check_scene_recovery(self,button_text):
        if self.save_app.checkedId() == -1:
            if self.message('提示', '请勾选是否保留应用') != QMessageBox.No:
                return
        if self.recover_dict["批量安装APK（APK路径：xxx）"]:
            if self.lineEdit_6.text() == '':
                if self.message('提示', '请输入APK所在路径') != QMessageBox.No:
                    return
            else:
                self.apk_root = self.lineEdit_6.text()

        if self.recover_dict["移动存储设备是否能够成功挂载,U盘个数："]:
            if not self.lineEdit_5.text().isdigit():
                if self.message('提示', 'U盘个数：请输入数字！') != QMessageBox.No:
                    return
            else:
                self.usb_count = int(self.lineEdit_5.text())
        if button_text == "一键调试":
            if self.view_close(self.device_choice_ui):
                return
            self.device_choice_ui = device_chooose_connect(self)
            self.device_choice_ui.device_list_signal.connect(self.create_recovery_scene)
            self.device_choice_ui.show()
        else:
            if self.view_close(self.create_scene_view):
                return
            self.create_scene_view = create_scene_view('count', parent=self)
            self.create_scene_view.scene_information.connect(self.create_recovery_scene)
            self.create_scene_view.show()

    def open_scene_list(self):
        self.off_open_list.emit()
        self.close()

    def create_scene_boot_enter(self, devices_list, scene_name, exec_times):
        this_checker = ck.Checker()
        if len(devices_list) == 0:
            self.scene_boot_enter = scene_boot_enter.SceneBootEnter(
                name=scene_name,
                exec_time=exec_times,
                by=sc.BY_COUNT,
                checker=this_checker,
                inner=self.onAndoff_dict["内置应用"],
                third=self.onAndoff_dict["第三方应用"],
                tv=self.onAndoff_dict["信源"]
                )
            self.scene_boot_enter.save()
            self.attribute_init()
            self.creat_success_toast = toast(parent=self, text='开机直达场景\n创建成功！')
            self.creat_success_toast.move(QPoint(self.geometry().left() + self.width() * 0.3, self.geometry().top() + self.height() * 0.3))
            self.creat_success_toast.ocl_signal.connect(self.open_scene_list)
            self.creat_success_toast.exec()
        else:
            self.scene_boot_enter = scene_boot_enter.SceneBootEnter(
                name="开机直达",
                exec_time=1,
                checker=this_checker,
                inner=self.onAndoff_dict["内置应用"],
                third=self.onAndoff_dict["第三方应用"],
                tv=self.onAndoff_dict["信源"]
            )
            self.attribute_init()
            self.scene_boot_enter.device = dv.Device(devices_list[0][0], devices_list[0][1])
            self.checkscene = sceneOneCheck(self.scene_boot_enter)
            self.checkscene.reflash_sig.connect(self.showlog)
            self.checkscene.dependent_check_sig.connect(self.check_message)
            self.checkscene.start()

    def create_onoff_scene(self, devices_list, scene_name, exec_times):
        this_checker = ck.Checker(
                net=self.onAndoff_dict["网络是否回连成功"],
                usb=self.onAndoff_dict["移动存储设备挂载是否成功,U盘个数："],
                hdmi=self.onAndoff_dict["HDMI出图是否成功"],
                blue_controller=self.onAndoff_dict["遥控器是否回连成功"],
                blue_speaker=self.onAndoff_dict["蓝牙音箱是否回连成功"],
                near=self.onAndoff_dict["近场唤醒是否成功"],
                far=self.onAndoff_dict["远场唤醒是否成功"],
                usb_count=self.usb_count,
                # a2dp_mac=self.a2dp_mac
        )
        if len(devices_list) == 0:
            self.scene_onoff = scene_on_and_off.SceneOnAndOff(
                name=scene_name,
                exec_time=exec_times,
                by=sc.BY_COUNT,
                checker=this_checker,
                mode=self.mode,
                key_set=dict(volume=self.onAndoff_dict["音量+-"], channel=self.onAndoff_dict["频道+-"],pad=self.onAndoff_dict["五维键"],voice=self.onAndoff_dict['语音键']),
                dc_off_interval=self.waittime,
                on2check_interval=self.boottime,
                ad_root=self.ad_root,
                far=self.far)
            self.scene_onoff.save()
            self.attribute_init()
            self.creat_success_toast = toast(parent=self, text='开关机场景\n创建成功！')
            self.creat_success_toast.move(QPoint(self.geometry().left() + self.width() * 0.3, self.geometry().top() + self.height() * 0.3))
            self.creat_success_toast.ocl_signal.connect(self.open_scene_list)
            self.creat_success_toast.exec()
        else:
            self.scene_onoff = scene_on_and_off.SceneOnAndOff(
                name="开机压测",
                exec_time=1,
                checker=this_checker,
                mode=self.mode,
                key_set=dict(volume=self.onAndoff_dict["音量+-"], channel=self.onAndoff_dict["频道+-"],pad=self.onAndoff_dict["五维键"],voice=self.onAndoff_dict['语音键']),
                dc_off_interval=self.waittime,
                on2check_interval=self.boottime,
                ad_root=self.ad_root,
                far=self.far)

            self.attribute_init()
            self.scene_onoff.device = dv.Device(devices_list[0][0], devices_list[0][1])
            self.checkscene = sceneOneCheck(self.scene_onoff)
            self.checkscene.reflash_sig.connect(self.showlog)
            self.checkscene.dependent_check_sig.connect(self.check_message)
            self.checkscene.start()


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

    def create_recovery_scene(self, devices_list, scene_name, exec_times):
        this_checker = ck.Checker(
            launcher=self.recover_dict["launcher进入正常"],
            camera=self.recover_dict["摄像头驱动是否正常，是否能升降"],
            usb=self.recover_dict["移动存储设备是否能够成功挂载,U盘个数："],
            wifi_driver=self.recover_dict["WiFi驱动是否正常"],
            far=self.recover_dict["远场语音是否能唤醒"],
            check_apk=self.recover_dict["检测第三方应用是否存在"],
            install_apk=self.recover_dict["批量安装APK（APK路径：xxx）"],
            usb_count=self.usb_count,
            apk_root=self.apk_root
        )
        if len(devices_list) == 0:
            self.recovery_scene = scene_recovery.SceneRecovery(
                name=scene_name,
                exec_time=exec_times,
                by=sc.BY_COUNT,
                checker=this_checker,
                retain_app=self.is_save_app,
                serial_open=self.is_open_Serial
            )
            self.recovery_scene.save()
            self.attribute_init()
            self.creat_success_toast = toast(parent=self, text='系统重置场景\n创建成功！')
            self.creat_success_toast.move(QPoint(self.geometry().left() + self.width() * 0.3, self.geometry().top() + self.height() * 0.3))
            self.creat_success_toast.ocl_signal.connect(self.open_scene_list)
            self.creat_success_toast.exec()
        else:
            self.recovery_scene = scene_recovery.SceneRecovery(
                name="恢复出厂设置",
                exec_time=1,
                checker=this_checker,
                retain_app=self.is_save_app,
                serial_open=self.is_open_Serial
            )
            self.attribute_init()
            self.recovery_scene.device = dv.Device(devices_list[0][0], devices_list[0][1])
            self.checkscene = sceneOneCheck(self.recovery_scene)
            self.checkscene.reflash_sig.connect(self.showlog)
            self.checkscene.dependent_check_sig.connect(self.check_message)
            self.checkscene.start()


    def showlog(self):
        self.debug_tootip = debug_tootip(self)
        self.debug_tootip.move(self.width() * 0.3, self.height() * 0.3)
        self.debug_tootip.exec()

    def check_message(self, check):
        self.message('依赖检查', check)





    def set_farmode(self, int):
        if int == 0:
            self.far = True
        else:
            self.far = False

    def set_saveapp(self, int):
        if int == 0:
            self.is_save_app = True
        else:
            self.is_save_app = False

    def set_openSerial(self, int):
        if int == 0:
            self.is_open_Serial = True
        else:
            self.is_open_Serial = False

    def set_onmode(self, int):
        if int == 0:
            self.mode = sw.MODE_AC
        else:
            self.mode = sw.MODE_DC

    def jump_connect(self, str):
        if str.strip() == "开关机流程检测":
            self.tabWidget.setCurrentIndex(0)
            self.pushButton_2.setStyleSheet('background: #1890FF;')
            self.pushButton_3.setStyleSheet('background: #000C17;')
            self.pushButton_4.setStyleSheet('background: #000C17;')
        elif str == "开机直达轮询":
            self.tabWidget.setCurrentIndex(1)
            self.pushButton_3.setStyleSheet('background: #1890FF;')
            self.pushButton_4.setStyleSheet('background: #000C17;')
            self.pushButton_2.setStyleSheet('background: #000C17;')
        elif str == "恢复出厂设置":
            self.tabWidget.setCurrentIndex(2)
            self.pushButton_4.setStyleSheet('background: #1890FF;')
            self.pushButton_2.setStyleSheet('background: #000C17;')
            self.pushButton_3.setStyleSheet('background: #000C17;')
        else:
            pass

if __name__ == '__main__':
    log.init_logging(output=True)
    app = QtWidgets.QApplication(sys.argv)  # 外部参数列表
    ui = model_on_and_off()
    ui.show()
    sys.exit(app.exec_())