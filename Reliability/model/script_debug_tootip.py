import time

from view.debug_tootip import Ui_Dialog
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon, QFont
import os
from PyQt5.QtCore import Qt
import constant
from task.msg_queue import TAG_EXCEPTION,TAG_END, TAG_START
from model.ali_QThread import script_debug_log


class script_debug_tootip(Ui_Dialog,QDialog):

    def __init__(self, parent=None):
        super(Ui_Dialog, self).__init__(parent)
        self.setupUi(self)
        self.m_flag = False
        self.showlog = None
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint| Qt.FramelessWindowHint)
        self.pushButton.clicked.connect(self.close)
        icon =QIcon(os.path.join(constant.SRC_ROOT, 'icon', 'close.ico'))
        self.pushButton.setIcon(icon)
        font = QFont()
        font.setBold(True)
        font.setPixelSize(30)
        self.textBrowser.setReadOnly(True)
        self.textBrowser.setCurrentFont(font)
        self.showlog = script_debug_log()
        self.showlog.reflash_sig.connect(self.add_information)
        self.showlog.close_sig.connect(self.reject)
        self.showlog.start()

    def add_information(self, text):
        print('start_text: ', text, ' time:', time.time())
        if text[0] == TAG_START:
            self.textBrowser.append('<pre><font color=black size=5>' + text[1] + '</font></pre>')
            self.changeUI()

        elif text[0] == TAG_EXCEPTION:
            self.textBrowser.append('<font color=red size=4>' + text[0] + ':'
                                    + '</font>' + '<font color=red size=4>' + text[1] + '</font>')
        elif text[0] == TAG_END:
            self.textBrowser.append('<font color=black size=3>' + text[0] + ':'
                                    + '</font>' + '<font color=red size=3>' + text[1] + '</font>')
            self.textBrowser.append('<font color=black size=3>' + '5秒后自动关闭调试界面' + '</font>')
        else:
            self.textBrowser.append('<font color=black size=3>' + text[0] + ':'
                                    + '</font>' + '<font color=red size=3>' + text[1] + '</font>')
        self.changeUI()
        print('end_text: ', text, ' time:', time.time())

    def changeUI(self):
        brow_line = self.textBrowser.document().lineCount()
        if self.textBrowser.size().width() - self.textBrowser.document().size().height() < 50:
            self.textBrowser.resize(
                self.textBrowser.size().width(),
                self.textBrowser.document().size().height() + 40)
        if self.textBrowser.size().width() - self.textBrowser.document().size().height() > 50:
            self.textBrowser.resize(
                self.textBrowser.size().width(),
                self.textBrowser.document().size().height() + 40)
        self.label.resize(self.label.size().width(), self.textBrowser.size().height() + 40)
        self.resize(self.size().width(), self.label.size().height() + 10)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()


    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False






if __name__ == '__main__':
    ...
