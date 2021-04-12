import os

from view.video import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QButtonGroup
import sys
from utils import log
from model.device_choose_connect_model import device_chooose_connect
from model.creat_scene_view import create_scene_view
import traceback
from utils.config_utils import read_config
import constant
from model.loading import loading
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal,QPoint
from model.toast import toast
from task import scene_media, checker as ck, device as dv, scene as sc, task_base
from model.ali_QThread import scene_test,sceneOneCheck
from model.debug_tootip import debug_tootip


class model_scene_media(Ui_MainWindow, QMainWindow):

    off_open_list = pyqtSignal()
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())
        self.default_config = read_config(constant.CONFIG_FILE)
        self.videomode = None
        self.attribute_init()
        self.online_list = [self.checkBox, self.checkBox_2, self.checkBox_3
                            , self.checkBox_4, self.checkBox_8, self.checkBox_9, self.checkBox_10, self.checkBox_11,
                            self.checkBox_12, self.checkBox_14, self.checkBox_17, self.checkBox_15, self.checkBox_20, self.checkBox_18]
        self.online_dict = {"腾讯视频": False, "爱奇艺": False, "酷喵": False, "QQ音乐MV": False,
                              "QQ音乐": False, "HDP": False, "电视家": False,
                              "本地视频_大码率": False, "信源": False, "本地视频_混合编解码": False, "遥控器是否回连成功": False, "近场唤醒是否成功": False
            , "蓝牙音箱是否回连成功": False, "远场唤醒是否成功": False}

        self.to_screen_list = [self.checkBox_19, self.checkBox_22, self.checkBox_23, self.checkBox_21, self.checkBox_16
            , self.checkBox_31, self.checkBox_32]
        self.to_screen_dict = {"乐播投屏": False, "dlna投屏": False, "miracast（无线投屏）": False, "遥控器是否回连成功  ": False,
                            "近场唤醒是否成功": False, "蓝牙音箱是否回连成功": False, "远场唤醒是否成功": False}
        self.buttton_init()
    def attribute_init(self):

        self.performance_interval = self.default_config['scene_media']['performance_interval']['val']

        self.performance_str = ''
        self.a2dp_mac = None
        self.local_video = {'本地视频_大码率': '', '本地视频_混合编解码': ''}
        self.device_choice_ui = None
        self.create_scene_view = None

    def open_scene_list(self):
        self.off_open_list.emit()
        self.close()

    def buttton_init(self):
        from PyQt5.QtGui import QFont
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.lineEdit_9.setFont(QFont("宋体", 10, QFont.Normal))
        self.lineEdit_2.setFont(QFont("宋体", 14, QFont.Normal))
        self.lineEdit_3.setFont(QFont("宋体", 14, QFont.Normal))
        # self.lineEdit_9.setPlaceholderText('如勾选，请输入蓝牙音箱mac地址.')
        self.lineEdit_9.setHidden(True)
        self.setWindowTitle('多媒体兼容')
        # icon = QIcon(constant.all_icon)
        # self.setWindowIcon(icon)
        self.setWindowIcon(QIcon(os.path.join(constant.SRC_ROOT, 'icon', '多媒体兼容.ico')))
        self.label_15.setHidden(True)
        self.pushButton_2.clicked.connect(lambda: self.jump_connect(self.pushButton_2.text()))
        self.lineEdit.setPlaceholderText('起播命令输入到命令模板，模板路径‘安装工具路径/src/video_brand.json')
        self.lineEdit_8.setPlaceholderText('路径输入顺序：大码率;混合编解码。两个路径以英文;分隔。选择大码率和混合编解码视频商必填')

        for clickbox in self.online_list:
            clickbox.stateChanged.connect(lambda: self.online_checkbox(self.sender(), self.sender().text()))
        for clickbox2 in self.to_screen_list:
            clickbox2.stateChanged.connect(lambda: self.toscreen_checkbox(self.sender(), self.sender().text()))
        self.pushButton_8.clicked.connect(lambda: self.online_video_scene(self.pushButton_8.text()))
        self.pushButton_7.clicked.connect(lambda: self.online_video_scene(self.pushButton_7.text()))

        self.pushButton_9.clicked.connect(lambda: self.to_screen_scene(self.pushButton_9.text()))
        self.pushButton_10.clicked.connect(lambda: self.to_screen_scene(self.pushButton_10.text()))

        self.video_choice = QButtonGroup()
        self.video_choice.addButton(self.radioButton_5, 0)
        self.video_choice.addButton(self.radioButton_6, 1)
        self.video_choice.buttonClicked[int].connect(self.set_video_mode)
    def set_video_mode(self,int):
        if int == 0:
            self.videomode = True
        else:
            self.videomode = False

    def message(self, title, text):
        newMessagebox = QMessageBox(self)
        newMessagebox.setText('\r\r\r'+text+'\r\r\r')
        newMessagebox.setWindowTitle(title)
        newMessagebox.setIcon(1)
        newMessagebox.setStyleSheet('QMessageBox{background-color:rgb(240,240,240)}')
        newMessagebox.setStandardButtons(QMessageBox.Yes)
        newMessagebox.exec()



    def online_checkbox(self, checkbox, text):
        if checkbox.isChecked():
            self.online_dict[text] = True
        else:
            self.online_dict[text] = False
    def toscreen_checkbox(self, checkbox, text):
        if checkbox.isChecked():
            self.to_screen_dict[text] = True
        else:
            self.to_screen_dict[text] = False

    def online_video_scene(self, value):
        if not True in list(self.online_dict.values())[0:10]:
            self.message('提示', '请勾选带*号的必选项：视频商')
            return

        if self.lineEdit_8.text() == "":
            if self.online_dict["本地视频_大码率"] == True or self.online_dict["本地视频_混合编解码"] == True:
                self.message('提示', '请填入已勾选的本地视频地址')
                return
        else:
            locat_video_list = self.lineEdit_8.text().split(';')
            len_locat_video_list = len(locat_video_list)
            if len_locat_video_list > 3:
                self.message('提示', '检查发现地址个数异常请先排查！')
                return
            for dir in  locat_video_list:
                len_locat_video_list = len_locat_video_list if dir != '' else len_locat_video_list - 1
            if len_locat_video_list == 1 and self.online_dict["本地视频_大码率"] == True and self.online_dict["本地视频_混合编解码"] == True:
                self.message('提示', '请填入正确的本地视频地址个数，根据已勾选本地视频！')
                return
            elif len_locat_video_list == 2 and self.online_dict["本地视频_大码率"] == True and self.online_dict["本地视频_混合编解码"] == True:
                self.local_video['本地视频_大码率'] = locat_video_list[0]
                self.local_video['本地视频_混合编解码'] = locat_video_list[1]
            else:
                if len_locat_video_list == 2:
                    self.message('提示', '请根据填入的地址数量，勾选本地视频项！')
                    return
                elif self.online_dict["本地视频_大码率"] == True:
                    self.local_video['本地视频_大码率'] = self.lineEdit_8.text()
                elif self.online_dict["本地视频_混合编解码"] == True:
                    self.local_video['本地视频_混合编解码'] = self.lineEdit_8.text()
                else:
                    self.message('提示', '检查发现已输入地址，请勾选对应的本地视频项')
                    return


        # if self.online_dict["蓝牙音箱是否回连成功"]:
        #     if not self.lineEdit_9.text():
        #         self.message('提示', '请输入蓝牙Mac地址！')
        #     else:
        #         self.a2dp_mac = self.lineEdit_9.text()
        if self.lineEdit_2.text() != "":
            try:
                self.performance_interval = float(self.lineEdit_2.text())*60
            except:
                self.lineEdit_2.clear()
                self.label_15.setHidden(False)
                return


        self.performance_str = self.lineEdit_3.text()
        if value == "一键调试":
            if self.view_close(self.device_choice_ui):
                return
            self.device_choice_ui = device_chooose_connect(self)
            self.device_choice_ui.device_list_signal.connect(self.create_online_scene)
            self.device_choice_ui.show()
        else:
            if self.view_close(self.create_scene_view):
                return
            self.create_scene_view = create_scene_view('time', parent=self)
            self.create_scene_view.scene_information.connect(self.create_online_scene)
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

    def to_screen_scene(self, value):
        if self.video_choice.checkedId() == -1:
            QMessageBox.information(None, '提示', '请勾选带*号的必选项：视频选择', QMessageBox.Yes)
            return
        if value == "一键调试":
            if self.view_close(self.device_choice_ui):
                return
            self.device_choice_ui = device_chooose_connect()
            self.device_choice_ui.device_list_signal.connect(self.create_toscreen_scene)
            self.device_choice_ui.show()
        else:
            if self.view_close(self.create_scene_view):
                return
            self.create_scene_view = create_scene_view()
            self.create_scene_view.scene_information.connect(self.create_toscreen_scene)
            self.create_scene_view.show()

    def create_online_scene(self,devices_list, scene_name,exec_times):
        this_checker = ck.Checker(
            blue_controller=self.online_dict["遥控器是否回连成功"],
            blue_speaker=self.online_dict["蓝牙音箱是否回连成功"],
            near=self.online_dict["近场唤醒是否成功"],
            far=self.online_dict["远场唤醒是否成功"],
        )
        brand_list = []
        for channel in ["腾讯视频", "爱奇艺", "酷喵", "QQ音乐MV",
                              "QQ音乐", "HDP", "电视家",
                              "本地视频_大码率", "本地视频_混合编解码", "信源"]:
            if self.online_dict[channel] == True:
                brand_list.append(channel)
        if len(devices_list) == 0:
            self.online_scene = scene_media.SceneMedia(
                name=scene_name,
                exec_time=exec_times,
                by=sc.BY_TIME,
                checker=this_checker,
                brand_list=brand_list,
                profile=self.lineEdit.text(),
                performance_str=self.performance_str,
                performance_interval=self.performance_interval,
                local_video=self.local_video

                # check_interval=self.lineEdit_2.text()
            )
            self.attribute_init()
            self.online_scene.save()
            self.creat_success_toast = toast(parent=self, text='视频煲机场景\n创建成功！')
            self.creat_success_toast.move(QPoint(self.geometry().left() + self.width() * 0.3, self.geometry().top() + self.height() * 0.3))
            self.creat_success_toast.ocl_signal.connect(self.open_scene_list)
            self.creat_success_toast.exec()
        else:
            self.online_scene = scene_media.SceneMedia(
                name="视频煲机",
                exec_time=1,
                checker=this_checker,
                brand_list=brand_list,
                profile=self.lineEdit.text(),
                performance_str=self.performance_str,
                performance_interval=self.performance_interval,
                local_video=self.local_video
            )
            self.attribute_init()
            self.online_scene.device = dv.Device(devices_list[0][0], devices_list[0][1])
            self.checkscene = sceneOneCheck(self.online_scene)
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
    def create_toscreen_scene(self,devices_list, scene_name,exec_times):
        this_checker = ck.Checker(
            launcher=True,
            # blue_controller=self.online_dict["遥控器是否回连成功"],
            # blue_speaker=self.online_dict["蓝牙音箱是否回连成功"],
            # near=self.online_dict["近场唤醒是否成功"],
            # far=self.online_dict["远场唤醒是否成功"],
        )
        # brand_list = []
        # for channel in ["腾讯视频", "爱奇艺", "酷喵", "QQ音乐MV",
        #                 "QQ音乐", "HDP", "电视家",
        #                 "本地视频", "信源"]:
        #     if self.online_dict[channel] == True:
        #         brand_list.append(channel)
        # print('brand_list', brand_list)
        if self.videomode == True:
            profile=''
        else:
            profile=''
        if len(devices_list) == 0:
            self.online_scene = scene_media.SceneMedia(
                name=scene_name,
                exec_time=exec_times,
                by=sc.BY_COUNT,
                profile=profile,
                checker=this_checker,
                brand_list=[],
                performance_str=self.lineEdit_7.text(),
                performance_interval=int(self.lineEdit_6.text()),
                # check_interval=self.lineEdit_2.text()
            )
            self.online_scene.save()
        else:
            self.online_scene = scene_media.SceneMedia(
                name="开机直达",
                exec_time=1,
                profile=profile,
                checker=this_checker,
                brand_list=[],
                performance_str=self.lineEdit_7.text(),
                performance_interval=int(self.lineEdit_6.text()),
                # check_interval=self.lineEdit_2.text()
            )
            task = task_base.TaskBase(name=scene_name,
                                      device=dv.Device(devices_list[0][0], devices_list[0][1]),
                                      scene_list=[self.online_scene])
            # task.start()
            try:
                self.test = scene_test(task)
                self.test.sig.connect(self.inform_text)
                self.test.start()
            except:
                print(traceback.format_exc())

    def jump_connect(self, str):
        if str == "内置在线视频":
            self.tabWidget.setCurrentIndex(0)
        elif str == "投屏轮播":
            self.tabWidget.setCurrentIndex(1)
        elif str == "本地视频":
            self.tabWidget.setCurrentIndex(2)
        else:
            pass

if __name__ == '__main__':
    log.init_logging("", output=True)
    app = QtWidgets.QApplication(sys.argv)  # 外部参数列表
    ui = model_scene_media()
    ui.show()
    sys.exit(app.exec_())