from view.choose_recorder import Ui_widget
from PyQt5.QtCore import Qt,pyqtSignal,QSize
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog,QMessageBox
from PyQt5.QtGui import QIcon
import sys
import os
import constant
from task import checker as ck
from task.scene_record import set_kk_record_path,SceneRecord
from model.ali_QThread import CreatRecorderScene

from model.creat_scene_view import create_scene_view
from model.toast import toast

class model_scene_recorder(Ui_widget,QMainWindow):
    off_open_list = pyqtSignal()
    def __init__(self, parent=None):
        super(model_scene_recorder, self).__init__(parent)

        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.script_list = None
        # self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.pushButton.setIcon(QIcon(os.path.join(constant.SRC_ROOT, 'icon','open_file.ico')))
        self.pushButton.setIconSize(QSize(30, 30))
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle('  ')
        self.pushButton.clicked.connect(self.find_rerorder_dir)
        self.pushButton_2.clicked.connect(self.open_recorder)
        with open(constant.RECORD_PATH, 'r', encoding='utf-8') as f:
            self.lineEdit.setPlaceholderText(f.read())

    def message(self, title, text):
        if self.isHidden():
            self.setHidden(False)
        newMessagebox = QMessageBox(self)
        newMessagebox.setText('\r\r\r'+text+'\r\r\r')
        newMessagebox.setWindowTitle(title)
        newMessagebox.setIcon(1)
        newMessagebox.setStyleSheet('QMessageBox{background-color:rgb(240,240,240)}')
        newMessagebox.setStandardButtons(QMessageBox.Yes)
        newMessagebox.exec()

    def find_rerorder_dir(self):
        self.lineEdit.setText("")
        kk = QFileDialog.getOpenFileName(self,'open file', '/')
        if kk[0] == '':
            return
        dir_name = os.path.dirname(kk[0])
        set_kk_record_path(dir_name)
        with open(constant.RECORD_PATH, 'r', encoding='utf-8') as f:
            self.lineEdit.setPlaceholderText(f.read())
        # self.lineEdit.setPlaceholderText(k)



    def open_recorder(self):
        if self.lineEdit.text() != "":
            set_kk_record_path(self.lineEdit.text())
        self.create_scene = CreatRecorderScene()
        self.create_scene.error_msg.connect(self.message)
        self.create_scene.script_list.connect(self.set_scene_information)
        self.create_scene.start()
        self.hide()

    def set_scene_information(self, script_list):
        if len(script_list) == 0:
            self.setHidden(False)
        else:
            self.script_list = script_list
            self.get_scene_information = create_scene_view('count', parent=self)
            self.get_scene_information.scene_information.connect(self.create_recorder_scene)
            self.get_scene_information.show()
            self.get_scene_information.move(self.geometry().left()*0.9+self.width()*0.1,
                                            self.geometry().top()-self.height()*0.1)
    def create_recorder_scene(self, device_list, curname, times):
        check = ck.Checker()
        self.recorder_scene = SceneRecord(
            name=curname,
            exec_time=times,
            checker=check,
            scripts=self.script_list
        )
        self.recorder_scene.save()
        self.creat_success_toast = toast(parent=self, text='录制脚本压测场景\n创建成功！')

        self.creat_success_toast.move(self.geometry().left() + self.width() * 0.2, self.geometry().top() + self.height() * 0.1)
        self.creat_success_toast.ocl_signal.connect(self.open_scene_list)
        self.creat_success_toast.exec()
    def open_scene_list(self):
        self.close()
        self.off_open_list.emit()





def start_recorder(exe_dir,args_string):
    if os.system(exe_dir+' '+args_string):
        return True
    return False

if __name__ == '__main__':
    from utils.log import init_logging
    init_logging(output=True)
    app = QApplication(sys.argv)
    win = model_scene_recorder()
    win.show()
    sys.exit(app.exec_())