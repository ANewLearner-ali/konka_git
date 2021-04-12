import traceback

from constant import QSS_FILE
from utils import log
from utils.config_utils import qss_read
from view.sence_task import Ui_Form
from PyQt5 import QtWidgets
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget, QMessageBox, QMainWindow, QTableWidgetItem, QPushButton, QHBoxLayout, \
    QAbstractItemView, QCheckBox
import sys
from task.dependent import get_detail
import constant
from PyQt5.QtGui import QIcon
import time
from task.scene import Scene, remove_scene, get_scene_detail
from task.task_manager import manager
from model.device_choose_connect_model import device_chooose_connect
from model._tootip import scene_tootop
import logging
from task.scene_record import SceneRecord
checkbox_style = """QCheckBox{
    background-color: rgb(255,255,255);
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


class model_sence_task_view(Ui_Form, QMainWindow):

    #定义一个信号用来界面刷新
    task_reflash = pyqtSignal()
    open_task_signal = pyqtSignal()

    def __init__(self):
        super(model_sence_task_view, self).__init__()
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet(qss_read(QSS_FILE))
        icon = QIcon(constant.all_icon)
        self.setWindowIcon(icon)
        self.cur_scene_list = Scene.scene_list()
        self.setupUi(self)
        self.device_choice_ui = None
        self.init_task = None
        # 绘制界面的表头、表格用于界面显示
        self.headr_review()
        self.table_init()
        # 加载内容
        self.reflash()
        self.task_reflash.connect(self.reflash)
        self.tableWidget.clicked.connect(self._select)
        self.pushButton_3.clicked.connect(self.devices_choice)
        self.setFixedSize(self.width(), self.height())

    def table_init(self):

        self.tableWidget.setColumnCount(6)
        self.tableWidget.setColumnWidth(0, 25)
        self.tableWidget.setColumnWidth(1, 250)
        self.tableWidget.setColumnWidth(2, 120)
        self.tableWidget.setColumnWidth(3, 80)
        self.tableWidget.setColumnWidth(4, 230)
        self.tableWidget.setColumnWidth(5, 70)
        self.tableWidget.horizontalHeaderItem(1)
        self.tableWidget.verticalHeader().setVisible(False)  # 隐藏垂直表头
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        #self.tableWidget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        # 设置表格内容不可编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 不会出现虚线框，设置点击后的颜色为白色
        self.tableWidget.setFocusPolicy(Qt.NoFocus)
        self.tableWidget.setStyleSheet("""
                font-family: PingFangSC-Regular;
                font-size: 15px;
                color: rgba(0,0,0,0.65);
                text-align: left;
                line-height: 14.67px;
        """)

    def headr_review(self):
        self.setWindowTitle('场景列表')
        self.pushButton_3.setIcon(QIcon(constant.BASE_ROOT+'/src/icon/add.ico'))
        self.pushButton_3.setToolTip('勾选场景后，点击打开任务创建界面')
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.tableWidget_2.setColumnCount(6)
        self.tableWidget_2.setColumnWidth(0, 25)
        self.tableWidget_2.setColumnWidth(1, 250)
        self.tableWidget_2.setColumnWidth(2, 120)
        self.tableWidget_2.setColumnWidth(3, 80)
        self.tableWidget_2.setColumnWidth(4, 230)
        self.tableWidget_2.setColumnWidth(5, 70)
        self.tableWidget_2.horizontalHeaderItem(1)
        self.tableWidget_2.verticalHeader().setVisible(False)  # 隐藏垂直表头
        self.tableWidget_2.horizontalHeader().setVisible(False)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        # 设置表格内容不可编辑
        self.tableWidget_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 不会出现虚线框，设置点击后的颜色为白色
        self.tableWidget_2.setFocusPolicy(Qt.NoFocus)
        self.tableWidget_2.setStyleSheet("""
        font-family: PingFangSC-Medium;
font-size: 15px;
color: rgba(0,0,0,0.85);
line-height: 14.67px;
        """)
        #初始化第一行
        self.tableWidget_2.insertRow(0)
        self.tableWidget_2.setRowHeight(0, 41)
        # checkbox = QCheckBox()
        # checkbox.setStyleSheet(checkbox_style)
        # _checkbox
        self.tableWidget_2.setCellWidget(0, 0, self._checkbox())
        self.tableWidget_2.setItem(0, 1, QTableWidgetItem("场景名称"))
        self.tableWidget_2.setItem(0, 2, QTableWidgetItem("创建日期"))
        self.tableWidget_2.setItem(0, 3, QTableWidgetItem("执行时长"))
        self.tableWidget_2.setItem(0, 4, QTableWidgetItem("环境依赖"))
        self.tableWidget_2.setItem(0, 5, QTableWidgetItem("操作"))

        #居中显示
        for i in range(1, 6):

            self.tableWidget_2.item(0, i).setTextAlignment(Qt.AlignCenter)
            self.tableWidget_2.item(0, i).setFlags(Qt.ItemIsEnabled)
        self.tableWidget_2.clicked.connect(self.all_select)

    def message(self, title, text):
        newMessagebox = QMessageBox(self)
        newMessagebox.setText('\r\r\r'+text+'\r\r\r')
        newMessagebox.setWindowTitle(title)
        newMessagebox.setIcon(1)
        newMessagebox.setStyleSheet('QMessageBox{background-color:rgb(240,240,240)}')
        newMessagebox.setStandardButtons(QMessageBox.Yes)
        newMessagebox.exec()

    def _checkbox(self):
        widget = QWidget()
        checkbox = QCheckBox()
        checkbox.setStyleSheet(checkbox_style)
        layout = QHBoxLayout()
        layout.addWidget(checkbox)
        layout.setAlignment(widget, Qt.AlignCenter)
        # 左边间隔4个像素，以至于不会贴边
        layout.setContentsMargins(4, 0, 0, 0)
        widget.setLayout(layout)
        return widget

    def _get_checkbox_state(self, cellwidget):
        checkbox = cellwidget.findChildren(QCheckBox)[0]
        return checkbox.isChecked()

    def _set_checkbox_state(self, cellwidget, state):
        checkbox = cellwidget.findChildren(QCheckBox)[0]
        checkbox.setChecked(state)

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

    def devices_choice(self):
        if len(self.get_checked_list()) == 0:
            self.message('提示', '请勾选需执行的场景')
            return
        if self.view_close(self.device_choice_ui):
            return
        self.device_choice_ui = device_chooose_connect(self)
        self.device_choice_ui.device_list_signal.connect(self.create_task)
        self.device_choice_ui.show()

    def closeEvent(self, event):
        for i in list(self.timer_list.keys()):
            self.timer_list[i]['QTimer'].stop()
        event.accept()

    def open_manager_view(self):
        try:
            logging.debug('open_manager_task_view, emit the signal, doing...{}'.format(time.time()))
            self.open_task_signal.emit()
            logging.debug('open_manager_task_view, has emit the signal ,doing1...{}'.format(time.time()))
        except:
            logging.debug('open_manager_view has fail')
            print(traceback.format_exc())


    def _init_task(self):
        self.init_task = None

    def create_task(self, devices_list, null, test):
        if self.init_task is not None:
            self.message('提示', '请稍等存在任务正在初始化中...')
            return
        scene_list = []
        logging.debug('add_selected_scene  Start: ')
        for choice_scene in self.get_checked_list():
            scene_list.append(self.cur_scene_list[choice_scene])
        from model.ali_QThread import CreatTaskTread
        self.init_task = CreatTaskTread(devices_list, scene_list, manager)
        self.init_task.error_signal.connect(self.message)
        self.init_task.over_signal.connect(self._init_task)
        self.init_task.success_singal.connect(self.open_manager_view)
        self.init_task.start()

    def _select(self, index):
        row = index.row()
        if self._get_checkbox_state(self.tableWidget.cellWidget(row, 0)):
            self._set_checkbox_state(self.tableWidget.cellWidget(row, 0), False)
        else:
            self._set_checkbox_state(self.tableWidget.cellWidget(row, 0), True)
    def all_select(self, index):
        row = index.row()
        if row == 0:
            if self._get_checkbox_state(self.tableWidget_2.cellWidget(row, 0)):
                for i in range(self.tableWidget.rowCount()):
                    self._set_checkbox_state(self.tableWidget.cellWidget(i, 0), False)
                self._set_checkbox_state(self.tableWidget_2.cellWidget(row, 0), False)
            else:
                for i in range(self.tableWidget.rowCount()):
                    self._set_checkbox_state(self.tableWidget.cellWidget(i, 0), True)
                self._set_checkbox_state(self.tableWidget_2.cellWidget(row, 0), True)

    def get_checked_list(self):
        check_list = []
        rowcount = self.tableWidget.rowCount()
        for i in range(0, rowcount):
            if self._get_checkbox_state(self.tableWidget.cellWidget(i, 0)):
                check_list.append(i)
        return check_list

    def add_buttongroup(self, index,cur_sence):
        StyleSheet = """QPushButton{
        background-color:rgb(255, 255, 255);
        border:none;
        height:40px;
        text-align: right;
        border-radius:3px;
        font-family: PingFangSC-Regular;
        font-size: 14.33px;
        color: #1890FF;
        line-height: 14.67px;
        }
        QPushButton:hover{
        background-color:rgb(250, 250, 250);
        margin: 1px;
        }
        """

        StyleSheet2 = """QPushButton{
                background-color:rgb(255, 255, 255);
                border:none;
                height:40px;
                text-align: left;
                border-radius:3px;
                font-family: PingFangSC-Regular;
                font-size: 14.33px;
                color: #1890FF;
                 line-height: 14.67px;
                }
                QPushButton:hover{
                background-color:rgb(250, 250, 250);
                margin: 1px;
                }
                """
        del_button = QPushButton("删除")
        del_button.setStyleSheet(StyleSheet2)
        cat_button = QPushButton('查看')
        cat_button.setStyleSheet(StyleSheet)
        del_button.clicked.connect(lambda: self._delete_scene(index))
        cat_button.clicked.connect(lambda: self._cat_scene(cur_sence))
        cat_button.setToolTip(get_scene_detail(cur_sence))

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        layout.addWidget(cat_button)
        layout.addWidget(del_button)
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def _delete_scene(self, index):
        remove_scene(index)
        if index in self.timer_list.keys():
            self.timer_list[index]['QTimer'].stop()
        self.task_reflash.emit()

    def _cat_scene(self, cur_sence):
        self.detial = scene_tootop(self, get_scene_detail(cur_sence))
        self.detial.move(self.width() * 0.3, self.height() * 0.3)
        self.detial.exec()

    def text_scroll(self, i):
        dep_len = len(self.timer_list[i]['dependents'])
        count = self.timer_list[i]['QTimer'].count
        if count < dep_len - 14:
            self.tableWidget.item(i, 4).setText(self.timer_list[i]['dependents'][count: count+14])
        else:
            self.tableWidget.item(i, 4).setText(self.timer_list[i]['dependents'][dep_len-14:])
            self.timer_list[i]['QTimer'].count = -1
        self.timer_list[i]['QTimer'].count += 1

    def reflash(self):
        self.cur_scene_list = Scene.scene_list()
        rowcount = self.tableWidget.rowCount()
        #清除界面
        if rowcount != 0:
            for i in range(0, rowcount):
                self.tableWidget.removeRow(rowcount-i-1)
        i = 0
        self.timer_list = dict()
        for cur_sence in self.cur_scene_list:
            name = cur_sence['name']
            creatime = time.strftime("%Y-%m-%d", time.strptime(cur_sence['create_time'], "%Y-%m-%d %H:%M:%S"))
            by = cur_sence['by']
            if by == 1:
                exec_time = str(cur_sence['exec_time']/3600)+'H'
            else:
                exec_time = str(cur_sence['exec_time'])+'次'

            dependents = get_detail(cur_sence['dependent'])[0].split(':')[1]

            from task.scene import deserialize
            kk = deserialize(dict(cur_sence))
            if isinstance(kk, SceneRecord):
                dependents = '请到脚本录制工具列表中查看'
            # test 滚动
            if len(dependents) > 14:
                self.item_scroll(dependents, i)
            self.tableWidget.insertRow(i)
            # checkbox = QCheckBox()
            # checkbox.setStyleSheet(checkbox_style)
            self.tableWidget.setCellWidget(i, 0, self._checkbox())
            self.tableWidget.setItem(i, 1, QTableWidgetItem(name))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(creatime))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(exec_time))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(dependents))
            self.tableWidget.setCellWidget(i, 5, self.add_buttongroup(int(i), cur_sence))
            i = i + 1
        for i in range(0, len(self.cur_scene_list)):
            for j in range(1, 6):
                if j == 5:
                    self.tableWidget.cellWidget(i, j).setStyleSheet('background-color: rgb(255,255,255);')
                else:
                    self.tableWidget.item(i, j).setBackground(QBrush(QColor(255, 255, 255)))
                    self.tableWidget.item(i, j).setTextAlignment(Qt.AlignCenter)
                    self.tableWidget.item(i, j).setFlags(Qt.ItemIsEnabled)

    def item_scroll(self, dependents, i):
        self.timer_list[i] = dict()
        self.timer_list[i]['dependents'] = dependents
        self.timer_list[i]['QTimer'] = QTimer()
        self.timer_list[i]['QTimer'].count = 0
        self.timer_list[i]['QTimer'].timeout.connect(lambda: self.text_scroll(i))
        self.timer_list[i]['QTimer'].start(500)


if __name__ == '__main__':
    log.init_logging(output=True)
    app = QtWidgets.QApplication(sys.argv)  # 外部参数列表
    ui = model_sence_task_view()
    ui.show()
    sys.exit(app.exec_())
