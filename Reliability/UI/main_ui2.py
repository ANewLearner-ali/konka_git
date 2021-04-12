# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui2.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(845, 633)
        MainWindow.setAcceptDrops(False)
        MainWindow.setStyleSheet("QWidget#centralwidget {\n"
"background:rgb(255, 255, 255);\n"
"}\n"
"QPushButton {\n"
"background: #FFFFFF;\n"
"box-shadow: 0 1px 7px 0 rgba(0,0,0,0.09);\n"
"font-family: PingFangSC-Medium;\n"
"font-size: 16px rgba(0,0,0,0.85);\n"
"}\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_version = QtWidgets.QLabel(self.centralwidget)
        self.label_version.setGeometry(QtCore.QRect(660, 580, 171, 20))
        self.label_version.setStyleSheet("QLabel{\n"
"    font:  12pt;\n"
"    color: #565E6C;\n"
"}")
        self.label_version.setObjectName("label_version")
        self.btn_scene_list = QtWidgets.QPushButton(self.centralwidget)
        self.btn_scene_list.setGeometry(QtCore.QRect(640, 40, 80, 30))
        self.btn_scene_list.setStyleSheet("QPushButton{\n"
"background: #FFFFFF;\n"
"border-radius: 5px;\n"
"border-radius: 5px;\n"
"font-family: \"微软雅黑\";\n"
"font-size: 14px;\n"
"color: #2C2E3A;\n"
"text-align: center;\n"
"}\n"
"QPushButton:hover{\n"
"color:rgb(255, 193, 7);\n"
"}")
        self.btn_scene_list.setObjectName("btn_scene_list")
        self.btn_task_list = QtWidgets.QPushButton(self.centralwidget)
        self.btn_task_list.setGeometry(QtCore.QRect(750, 40, 80, 30))
        self.btn_task_list.setStyleSheet("QPushButton{\n"
"background: #FFFFFF;\n"
"border-radius: 5px;\n"
"border-radius: 5px;\n"
"font-family: \"微软雅黑\";\n"
"font-size: 14px;\n"
"color: #2C2E3A;\n"
"text-align: center;\n"
"}\n"
"QPushButton:hover{\n"
"color:rgb(255, 193, 7);\n"
"}")
        self.btn_task_list.setObjectName("btn_task_list")
        self.btn_script = QtWidgets.QPushButton(self.centralwidget)
        self.btn_script.setGeometry(QtCore.QRect(530, 40, 80, 30))
        self.btn_script.setStyleSheet("QPushButton{\n"
"background: #FFFFFF;\n"
"border-radius: 5px;\n"
"border-radius: 5px;\n"
"font-family: \"微软雅黑\";\n"
"font-size: 14px;\n"
"color: #2C2E3A;\n"
"text-align: center;\n"
"}\n"
"QPushButton:hover{\n"
"color:rgb(255, 193, 7);\n"
"}")
        self.btn_script.setObjectName("btn_script")
        self.lb_effectanalysis = QtWidgets.QLabel(self.centralwidget)
        self.lb_effectanalysis.setGeometry(QtCore.QRect(50, 40, 211, 29))
        self.lb_effectanalysis.setStyleSheet("font: 75 24pt \"微软雅黑\";\n"
"font-size: 18px;\n"
"color: #FFFFFF;\n"
"")
        self.lb_effectanalysis.setObjectName("lb_effectanalysis")
        self.btn_help = QtWidgets.QPushButton(self.centralwidget)
        self.btn_help.setGeometry(QtCore.QRect(700, 80, 92, 31))
        self.btn_help.setStyleSheet("font-family: \"微软雅黑\";\n"
"font-size: 14px;\n"
"color: #000000;\n"
"min-width: 90px;\n"
"min-height: 29px;\n"
"border: 0px;\n"
"icon: url(:/icon/指引.ico)")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../src/icon/使用指引.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_help.setIcon(icon)
        self.btn_help.setIconSize(QtCore.QSize(13, 13))
        self.btn_help.setObjectName("btn_help")
        self.lb_effectanalysis.raise_()
        self.label_version.raise_()
        self.btn_scene_list.raise_()
        self.btn_task_list.raise_()
        self.btn_script.raise_()
        self.btn_help.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "自动化测试平台"))
        self.label_version.setText(_translate("MainWindow", "V1.0.0 2020-06-18"))
        self.btn_scene_list.setText(_translate("MainWindow", "场景管理"))
        self.btn_task_list.setText(_translate("MainWindow", "任务管理"))
        self.btn_script.setText(_translate("MainWindow", "脚本管理"))
        self.lb_effectanalysis.setText(_translate("MainWindow", "    系统可靠性"))
        self.btn_help.setText(_translate("MainWindow", "使用指引"))

