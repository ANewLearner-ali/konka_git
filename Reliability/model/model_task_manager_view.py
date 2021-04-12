
from utils import log
from view.task_manager import Ui_Form
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget, QMessageBox, QMainWindow,QAbstractItemView,QTableWidgetItem,QPushButton,QHBoxLayout,QTableWidget
import sys
import os
import time
from model.ali_QThread import manager_exec,execMsgThread
import constant
from PyQt5.QtGui import QIcon
from task.scene_record import SceneRecord

import logging
STATE_TODO = 1
STATE_RUNNING = 2
STATE_DELETE = 3
STATE_FINISH = 4
STATE_FAIL = 5
start_dict = {1: '待执行', 2: '执行中', 3: '删除', 4: '已完成', 5: '失败'}


class model_task_manager_view(Ui_Form, QMainWindow):
    #定义一个信号用来界面刷新
    com_task_reflash = pyqtSignal(str)

    def __init__(self, manager):
        super(model_task_manager_view, self).__init__()
        self.manager = manager
        self.com_list = self.manager.com_list
        self.task_set = self.manager.task_set
        self.timer_list = dict()
        self.setupUi(self)
        icon = QIcon(constant.all_icon)
        self.setWindowIcon(icon)
        self.setWindowTitle('任务列表')
        self.pushButton.clicked.connect(self.open_report)
        self.com_task_reflash.connect(self.com_flash)
        self.setFixedSize(self.width(), self.height())
        self.create_tab()
        self.all_flash()
        self.monitor()
        self.msg_thread()

    def msg_thread(self):
        self.exec_msg_thread = execMsgThread()
        self.exec_msg_thread.error_msg.connect(self.message)
        self.exec_msg_thread.start()

    def message(self,text):
        self.com_task_reflash.emit(text[0])
        self.newMessagebox = QMessageBox(self)
        self.newMessagebox.setText('当前端口' + text[0] + '在' + text[1] + '; 且当前场景任务执行失败，不影响下个场景的执行.')
        self.newMessagebox.setWindowTitle('任务提示')
        self.newMessagebox.setIcon(1)
        self.newMessagebox.setStyleSheet('QMessageBox{background-color:rgb(240,240,240)}')
        self.newMessagebox.setStandardButtons(QMessageBox.Yes)
        self.newMessagebox.exec()

    def closeEvent(self, event):
        self.exec_msg_thread.terminal()
        self.monitor_thread.terminal()
        for tv_com in list(self.timer_list.keys()):
            for index in self.timer_list[tv_com].keys():
                self.timer_list[tv_com][index]['QTimer'].stop()
        event.accept()

    def open_report(self):
        os.system('explorer.exe ' + constant.REPORTS_ROOT)

    def monitor(self):
        logging.debug('start --------manager_exec ----------')
        self.monitor_thread = manager_exec(self.task_set, self.com_list)
        self.monitor_thread.signal_change.connect(self.com_flash)
        self.monitor_thread.start()

    def create_tab(self):
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.tabWidget.removeTab(0)
        self.tabWidget.removeTab(0)
        self.tab_list = dict()
        for kk in self.com_list:
            self.tab_list[kk] = 'self.tab_'+kk
        for test in self.com_list:
            self.tab_list[test] = QWidget()
            this_table = QTableWidget()
            self.init_QTablewidget(this_table,test)
            sex = QHBoxLayout()
            sex.addWidget(this_table)
            sex.setSpacing(0)
            sex.setContentsMargins(0, 0, 0, 0)
            self.tab_list[test].setLayout(sex)
            self.tabWidget.addTab(self.tab_list[test], test)

    def init_QTablewidget(self, table, name):
        table.setObjectName(name)
        table.setColumnCount(5)
        table.setColumnWidth(0, 270)
        table.setColumnWidth(1, 120)
        table.setColumnWidth(2, 80)
        table.setColumnWidth(3, 230)
        table.setColumnWidth(4, 70)

        table.horizontalHeaderItem(1)
        table.verticalHeader().setVisible(False)  # 隐藏垂直表头
        table.horizontalHeader().setVisible(False)
        table.horizontalHeader().setStretchLastSection(True)
        # 设置表格内容不可编辑
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 不会出现虚线框，设置点击后的颜色为白色
        table.setFocusPolicy(Qt.NoFocus)
        table.setStyleSheet("""
                            font-family: PingFangSC-Medium;
                    font-size: 9.33px;
                    color: rgba(0,0,0,0.85);
                    line-height: 14.67px;
                            """)
        #初始化第一行
        table.insertRow(0)
        table.setItem(0, 0, QTableWidgetItem("场景名称"))
        table.setItem(0, 1, QTableWidgetItem("创建日期"))
        table.setItem(0, 2, QTableWidgetItem("执行时长"))
        table.setItem(0, 3, QTableWidgetItem("环境依赖"))
        table.setItem(0, 4, QTableWidgetItem("执行状态"))
        table.setRowHeight(0, 50)
        #居中显示
        for i in range(0, 5):
            table.item(0, i).setTextAlignment(Qt.AlignCenter)
            table.item(0, i).setFlags(Qt.ItemIsEnabled)

    def getindex(self, index):
        row =index.row()
        col = index.column()
        if row == 0:
            if self.tableWidget.item(row, 0).checkState() == 0:
                for i in range(self.tableWidget.rowCount()):
                    self.tableWidget.item(i, 0).setCheckState(Qt.Checked)

            else:
                for i in range(self.tableWidget.rowCount()):
                    self.tableWidget.item(i, 0).setCheckState(Qt.Unchecked)
        else:
            if col == 0:
                return
            if self.tableWidget.item(row, 0).checkState() == 0:
                self.tableWidget.item(row, 0).setCheckState(Qt.Checked)
            else:
                self.tableWidget.item(row, 0).setCheckState(Qt.Unchecked)

    def get_checked_list(self):
        check_list = []
        rowcount = self.tableWidget.rowCount()
        for i in range(1, rowcount):
            if self.tableWidget.item(i, 0).checkState():
                check_list.append(i)
        return check_list

    def com_flash(self, tv_com):
        cur_table = self.findChild(QTableWidget, tv_com)
        rowcount = cur_table.rowCount()
        if rowcount != 0:
            for i in range(1, rowcount):
                cur_table.removeRow(rowcount - i)
        task_list = self.task_set[tv_com].scene_list
        cur_list_len = len(task_list)
        # 用于记录场景的index
        mark_index = 0
        # 用于记录当前的行数，方便增加行数
        i = 1
        logging.debug(f'Com:{tv_com},task_list_length:{cur_list_len}')
        for cur_sence in task_list:
            try:
                logging.debug(f'Scene_name:{cur_sence.name}_GetInformation   Start:------------------')
                logging.debug(f'Scene_exec_time:{cur_sence.exec_time},Scene_state{cur_sence.state}')
            except BaseException as E:
                print('Exception:', E)
                pass
            logging.debug(f'cur_scenc:{cur_sence.name}')
            cur_table.insertRow(i)
            name = cur_sence.name
            creatime = time.strftime("%Y-%m-%d", time.strptime(cur_sence.create_time, "%Y-%m-%d %H:%M:%S"))
            by = cur_sence.by
            if by == 1:
                exec_time = str(cur_sence.exec_time / 3600) + 'H'
            else:
                exec_time = str(cur_sence.exec_time) + '次'
            dependents = cur_sence.dependent.get_detail()[0].split(':')[1]
            if isinstance(cur_sence, SceneRecord):
                dependents = '请到脚本录制工具列表中查看'
            logging.debug(f'scence_dependents: {dependents}')
            if len(dependents) > 14:
                self.item_scroll(tv_com, cur_table, dependents, i)
            if cur_sence.state == 3:
                cur_table.removeRow(i)
                mark_index += 1
                cur_list_len = cur_list_len - 1
                continue
            elif cur_sence.state == 1:
                widget = self.add_buttongroup(tv_com, mark_index)
                widget.setContentsMargins(0, 0, 0, 0)
                cur_table.setCellWidget(i, 4, widget)
            else:
                state = start_dict[cur_sence.state]
                cur_table.setItem(i, 4, QTableWidgetItem(state))
                cur_table.item(i, 4).setTextAlignment(Qt.AlignCenter)
                cur_table.item(i, 4).setFlags(Qt.ItemIsEnabled)
                cur_table.item(i, 4).setForeground(QColor(0, 0, 0, 165))
            mark_index += 1
            cur_table.setItem(i, 0, QTableWidgetItem(name))
            cur_table.setItem(i, 1, QTableWidgetItem(creatime))
            cur_table.setItem(i, 2, QTableWidgetItem(exec_time))
            cur_table.setItem(i, 3, QTableWidgetItem(dependents))
            i = i + 1
            logging.debug('Cur_Scene__End:------------------')
        for i in range(1, cur_list_len + 1):
            for j in range(0, 4):
                cur_table.item(i, j).setTextAlignment(Qt.AlignCenter)
                cur_table.item(i, j).setFlags(Qt.ItemIsEnabled)
                cur_table.item(i, j).setForeground(QColor(0, 0, 0, 165))

    def all_flash(self):
        for tv_com in self.com_list:
            self.com_flash(tv_com)

    def item_scroll(self, tv_com, cur_table, dependents, i):
        self.timer_list[tv_com] = dict()
        self.timer_list[tv_com][i] = dict()
        self.timer_list[tv_com][i]['dependents'] = dependents
        self.timer_list[tv_com][i]['cur_table'] = cur_table
        self.timer_list[tv_com][i]['QTimer'] = QTimer()
        self.timer_list[tv_com][i]['QTimer'].count = 0
        self.timer_list[tv_com][i]['QTimer'].timeout.connect(lambda: self.text_scroll(tv_com, i))
        self.timer_list[tv_com][i]['QTimer'].start(500)

    def text_scroll(self, tv_com, i):
        dep_len = len(self.timer_list[tv_com][i]['dependents'])
        count = int(self.timer_list[tv_com][i]['QTimer'].count)
        if count < dep_len - 14:
            self.timer_list[tv_com][i]['cur_table'].item(i, 3).setText(self.timer_list[tv_com][i]['dependents'][count: count+14])
        else:
            self.timer_list[tv_com][i]['cur_table'].item(i, 3).setText(self.timer_list[tv_com][i]['dependents'][dep_len-14:])
            self.timer_list[tv_com][i]['QTimer'].count = -1
        self.timer_list[tv_com][i]['QTimer'].count += 1

    def add_buttongroup(self, tv_com, index):
        del_button = QPushButton("待执行/单击删除任务")
        del_button.setStyleSheet("""QPushButton{
background-color:rgb(255, 255, 255);
border:none;
height:40px;
text-align: center;
border-radius:3px;
font-family: PingFangSC-Regular;
font-size: 9.33px;
color: #1890FF;
line-height: 14.67px;
}
QPushButton:hover{
background-color:rgb(245, 245, 245);
margin: 1px;
}
""")

        del_button.clicked.connect(lambda: self._delete_scene(tv_com, index))
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(del_button)
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def _delete_scene(self, tv_com, index):
        self.task_set[tv_com].delete_scene(index)
        if tv_com in self.timer_list.keys():
            if index in self.timer_list[tv_com].keys():
                self.timer_list[tv_com][index]['QTimer'].stop()
        self.com_task_reflash.emit(tv_com)


if __name__ == '__main__':
    log.init_logging("Test", output=False)
    app = QtWidgets.QApplication(sys.argv)  # 外部参数列表
    ui = model_task_manager_view()
    ui.show()
    sys.exit(app.exec_())

