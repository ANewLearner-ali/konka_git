from view.creat_scene import Ui_widget
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow
import sys
from PyQt5.QtGui import QIcon
import constant


class create_scene_view(Ui_widget, QMainWindow):
    #定义一个信号用来界面刷新
    scene_information = pyqtSignal(list, str, int)

    def __init__(self, text, parent=None):
        super(create_scene_view, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.setFixedSize(self.width(), self.height())
        self.setWindowTitle('创建场景')
        icon = QIcon(constant.all_icon)
        self.setWindowIcon(icon)
        if text == 'time':
            self.label_4.setText("H")
            self.label_3.setText('执行时间')
        self.pushButton.clicked.connect(self.complete)

    def complete(self):
        if self.lineEdit.text() == "":
            QMessageBox().information(self, "提示", "请输入场景名字！！！", QMessageBox.Yes)
            return
        try:
            str_number = self.lineEdit_2.text()
            if (str_number.split(".")[0]).isdigit() or str_number.isdigit() or str_number.split(".")[-1].isdigit():
                # print('str_number:', str_number)
                if self.label_4.text() == 'H':
                    times = float(str_number)*3600
                else:
                    times = float(str_number)
            else:
                raise Exception
        except :
            QMessageBox().information(self, "提示", "请输入正确的次数！！！", QMessageBox.Yes)
            return
        self.close()
        self.scene_information.emit([], self.lineEdit.text().replace(' ', ''), times)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = create_scene_view('time')
    win.show()
    sys.exit(app.exec_())

