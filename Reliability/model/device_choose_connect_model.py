import traceback
from view.device_choose import Ui_widget
from PyQt5.QtCore import Qt,pyqtSignal
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QAbstractItemView, QTableWidgetItem, \
    QLabel, QFrame, QComboBox, QCheckBox, QListView
import sys

from PyQt5.QtGui import QIcon
import constant
from utils.kkserial import KKSerialFactory

QComboBox_style = """
QComboBox {

    padding: 1px 18px 1px 12px;
    min-width: 6em;
	background: #FFFFFF;
	border: 1px solid rgba(0,0,0,0.15);
	border-radius: 4px;
	border-radius: 4px;
	font-family: PingFangSC-Regular;
	font-size: 21px;
	color: rgba(0,0,0,0.65);
}
QComboBox::drop-down {
	width: 30px;
border: 0px;border-left-width: 1px;
border-left-color: darkgray;
border-left-style: solid;
border-top-right-radius: 4px; 
border-bottom-right-radius: 4px;;
}
QComboBox::drop-down:!on {
    width: 30px;
border: 0px;border-left-width: 1px;
border-left-color: darkgray;
border-left-style: solid;
border-top-right-radius: 4px; 
border-bottom-right-radius: 4px;
}
QComboBox:on {
    padding-left: 4px;
}
QComboBox::down-arrow {
	image: url(:/img/down.png);
}
QComboBox::down-arrow:on {
	image: url(:/img/up.png);
}
QComboBox QAbstractItemView{
    border: 2px solid darkgray;
    selection-background-color: lightgray;
}
QAbstractItemView::item {
height: 32px;
font-family: PingFangSC-Regular;
font-size: 22px;
color: rgba(0,0,0,0.65);
border-radius: 4px;
}

"""
label_style = """font-family: PingFangSC-Regular;
font-size: 14px;
color: rgba(0,0,0,0.85);
text-align: right;
line-height: 22px;"""

checkbox_style = """QCheckBox{
	font-family: PingFangSC-Regular;
	font-size: 14px;
	color: rgba(0,0,0,0.65);
	letter-spacing: 0;
	text-align: left;
	line-height: 22px;
}
QCheckBox::indicator{
	background: #FFFFFF;
	border: 1px solid #40A9FF;
	border-radius: 2px;
	border-radius: 2px;
	width: 12px;
	height: 12px;
}
QCheckBox::indicator:checked{
	image: url(./src/qss/复选-已选.svg);
}"""


class device_chooose_connect(Ui_widget, QMainWindow):

    #定义一个信号用来界面刷新
    device_list_signal = pyqtSignal(list,str,int)

    def __init__(self, parent=None):
        super(device_chooose_connect, self).__init__(parent)
        self.setupUi(self)
        self.isScriptTest = True
        from model.model_scene_task_view import model_sence_task_view
        if not isinstance(parent, model_sence_task_view):
            self.pushButton_2.setVisible(False)
        from model.main_test_1 import Entrance_View
        if not isinstance(parent, Entrance_View):
            self.checkBox.setVisible(False)
            self.isScriptTest = False

        self.setFixedSize(self.width(), self.height())
        self._table_init()
        icon = QIcon(constant.all_icon)
        self.setWindowIcon(icon)
        self.add_row()
        self.pushButton_2.clicked.connect(self.add_row)
        self.pushButton.clicked.connect(self.complete)
        self.setWindowTitle('端口选择')

    def complete(self):
        try:
            check_list = []
            rowcount =self.tableWidget.rowCount()
            for i in range(0, rowcount, 2):
                if self.tableWidget.cellWidget(i, 6).isChecked():
                    check_list.append(i)
            if len(check_list) == 0:
                QMessageBox().information(self, "提示", "未勾选设备，请勾选设备", QMessageBox.Yes)
                return False
            device_list = []
            mcu_com_list = []
            for row in check_list:
                if self.tableWidget.cellWidget(row, 4).currentText() == '无':
                    mcu_com = ''
                else:
                    mcu_com = self.tableWidget.cellWidget(row, 4).currentText().upper()
                if mcu_com == '' or mcu_com not in mcu_com_list:
                    if mcu_com != '':
                        mcu_com_list.append(mcu_com)
                    device_list.append([self.tableWidget.cellWidget(row, 1).currentText().lower(), mcu_com])
                else:
                    QMessageBox().information(self, "提示", f"单片机端口号存在冲突请检测：{mcu_com}\n注意:每个设备对应一个单片机!!!", QMessageBox.Yes)
                    return
            if len(device_list) == 0:
                QMessageBox().information(self, "提示", "请输入合法的输入值，空值已经忽略！！！", QMessageBox.Yes)
                return False
            if self.isScriptTest == True:
                if self.checkBox.isChecked():
                    self.device_list_signal.emit(device_list, 'True', 1)
                else:
                    self.device_list_signal.emit(device_list, 'False', 1)

            else:
                self.device_list_signal.emit(device_list, 'test', 1)
            self.close()
        except:
            print(traceback.format_exc())


    def add_row(self):
        try:
            all_serial_list = KKSerialFactory.get_all_serial()
            ch340_com_list = KKSerialFactory.get_ch340_com_list()
            ch340_com_list.append('无')
            row = self.tableWidget.rowCount()
            if row != 0:
                self.tableWidget.insertRow(row)
                self.tableWidget.setItem(row, 0, QTableWidgetItem(""))
                self.tableWidget.setRowHeight(row, 10)
                row += 1
            self.tableWidget.insertRow(row)
            tv_tom_label = QLabel("      设备" + str(int(row/2 + 1)) + "端口:")
            tv_tom_label.setStyleSheet(label_style)
            self.tableWidget.setCellWidget(row, 0, tv_tom_label)
            ser_comBox = QComboBox()
            ser_comBox.setStyleSheet(QComboBox_style)
            ser_comBox.setView(QListView())
            for cur_serial in all_serial_list:
                if cur_serial not in ch340_com_list:
                    ser_comBox.addItem(cur_serial)
            self.tableWidget.setCellWidget(row, 1, ser_comBox)
            self.tableWidget.setItem(row, 2, QTableWidgetItem(""))
            muc_tom_label = QLabel(" 单片机端口:")
            muc_tom_label.setStyleSheet(label_style)
            self.tableWidget.setCellWidget(row, 3, muc_tom_label)
            comBox = QComboBox()
            comBox.setStyleSheet(QComboBox_style)
            comBox.setView(QListView())
            for ch340_com in ch340_com_list:
                comBox.addItem(ch340_com)
            self.tableWidget.setCellWidget(row, 4, comBox)
            self.tableWidget.setItem(row, 5, QTableWidgetItem(""))
            checkbox = QCheckBox()
            checkbox.setStyleSheet(checkbox_style)

            self.tableWidget.setCellWidget(row, 6, checkbox)
            self.tableWidget.setRowHeight(row, 32)

        except:
            print(traceback.format_exc())


    def _table_init(self):
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.tableWidget.setFrameShape(QFrame.NoFrame)
        self.tableWidget.setColumnWidth(0, 118)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 2)
        self.tableWidget.setColumnWidth(3, 98)
        self.tableWidget.setColumnWidth(4, 150)
        self.tableWidget.setColumnWidth(5, 2)
        self.tableWidget.setColumnWidth(6, 30)
        self.tableWidget.verticalHeader().setVisible(False)  # 隐藏垂直表头
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        # 设置表格内容不可编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 不会出现虚线框，设置点击后的颜色为白色
        self.tableWidget.setFocusPolicy(Qt.NoFocus)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = device_chooose_connect()
    win.show()
    sys.exit(app.exec_())

