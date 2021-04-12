from view.toast import Ui_Dialog
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtWidgets import QDialog,QApplication
import sys

class toast(Ui_Dialog, QDialog):
    ocl_signal = pyqtSignal()

    def __init__(self, parent=None, text: str = ''):
        super(toast, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.label.setText(text)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.pushButton.clicked.connect(self.close)
        self.pushButton_2.clicked.connect(self.open_scene_list)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.WindowCloseButtonHint |
                            Qt.MSWindowsFixedSizeDialogHint | Qt.Tool | Qt.FramelessWindowHint)
        self.setWindowModality(Qt.ApplicationModal)

    def open_scene_list(self):
        self.ocl_signal.emit()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = toast(text='场景创建完毕！')
    win.exec()
    sys.exit(app.exec_())
