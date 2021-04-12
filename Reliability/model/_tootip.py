from view.tootip import Ui_Dialog
from PyQt5.QtWidgets import QDialog,QApplication
from PyQt5.QtGui import QIcon, QFont, QPalette,QColor,QCursor
import os
import sys
from PyQt5.QtCore import Qt, QSize
import constant
class scene_tootop(Ui_Dialog,QDialog):
    def __init__(self, parent=None,strMsg:str=''):
        super(Ui_Dialog,self).__init__(parent)
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.m_flag = False
        self.strMsg = strMsg if strMsg else None
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint| Qt.FramelessWindowHint)
        self.pushButton.clicked.connect(self.close)
        icon =QIcon(os.path.join(constant.SRC_ROOT, 'icon', 'close.ico'))
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QSize(13, 13))
        self.setStyleSheet('font: 18px rgb(0,255,0);')
        font = QFont()
        font.setBold(True)
        font.setPixelSize(30)
        self.textBrowser.setCurrentFont(font)
        qpalette = QPalette()
        qpalette.setColor(QPalette.Text, QColor(0, 255, 0))
        self.textBrowser.setPalette(qpalette)
        self.textBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.textBrowser.setTextInteractionFlags(Qt.NoTextInteraction)
        if self.strMsg == None:
            return
        msg_list = self.strMsg.split('\n')
        mark_overline = 1
        for curmsg in msg_list:
            try:
                msg = curmsg.split(':')
                if len(msg) == 2:
                    if msg[1] == '':
                        self.textBrowser.append('<pre><font color=black size=1>' + msg[0] + '</font></pre>')
                    else:
                        if len(msg[1]) > 15:
                            mark_overline -= 1
                        self.textBrowser.append('<pre><font color=black size=1>' + msg[0] + ':'
                                                + '</font>' + '<font color=red size=1>' + msg[1] + '</font></pre>')
                else:
                    self.textBrowser.append('<font color=black size=1>' + msg[0] + ':'
                                            + '</font>' + '<font color=red size=1>' + msg[1] + ':'+msg[2] + ':' + msg[3] + '</font>')
            except:
                self.textBrowser.append('<pre><font color=black size=1>' + curmsg
                                        + '</font></pre>')
        brow_line = self.textBrowser.document().lineCount()
        self.textBrowser.resize(
            self.textBrowser.size().width()-20,
            self.textBrowser.document().size().height()*brow_line + (brow_line-mark_overline) * 10)
        self.label.resize(self.textBrowser.size().width()+41, self.textBrowser.size().height()+40)
        self.resize(self.label.size().width()+10, self.label.size().height()+20)


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
    app = QApplication(sys.argv)
    win = scene_tootop()
    win.exec()
