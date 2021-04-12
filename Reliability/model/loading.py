from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QApplication
import sys
import os
import constant
from view.loading import Ui_Dialog


class loading(Ui_Dialog,QDialog):
    def __init__(self, parent=None):
        super(loading, self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        movie = QMovie(os.path.join(constant.SRC_ROOT, 'icon', 'loading.gif'))
        self.label.setMovie(movie)
        self.setWindowFlags(Qt.FramelessWindowHint)
        movie.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = loading()
    win.exec()
    sys.exit(app.exec_())


