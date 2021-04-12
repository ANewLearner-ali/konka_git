# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from view import main_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1024, 633)
        MainWindow.setAcceptDrops(False)
        MainWindow.setStyleSheet("QWidget#centralwidget {\n"
"background-image: url(:/img/bg.png)\n"
"}\n"
"QPushButton {\n"
"background: #FFFFFF;\n"
"box-shadow: 0 1px 7px 0 rgba(0,0,0,0.09);\n"
"font-family: PingFangSC-Medium;\n"
"font-size: 16px rgba(0,0,0,0.85);\n"
"}\n"
"QLabel {\n"
"background-image:url();\n"
"}\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btn_switch = QtWidgets.QPushButton(self.centralwidget)
        self.btn_switch.setGeometry(QtCore.QRect(125, 152, 241, 137))
        self.btn_switch.setStyleSheet("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/icon_开关机压测.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_switch.setIcon(icon)
        self.btn_switch.setIconSize(QtCore.QSize(56, 56))
        self.btn_switch.setObjectName("btn_switch")
        self.btn_source = QtWidgets.QPushButton(self.centralwidget)
        self.btn_source.setGeometry(QtCore.QRect(390, 150, 241, 137))
        self.btn_source.setStyleSheet("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/img/icon_信源煲机.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_source.setIcon(icon1)
        self.btn_source.setIconSize(QtCore.QSize(56, 56))
        self.btn_source.setObjectName("btn_source")
        self.btn_media = QtWidgets.QPushButton(self.centralwidget)
        self.btn_media.setGeometry(QtCore.QRect(126, 314, 241, 137))
        self.btn_media.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.btn_media.setStyleSheet("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/img/icon_视频类压测.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_media.setIcon(icon2)
        self.btn_media.setIconSize(QtCore.QSize(56, 56))
        self.btn_media.setObjectName("btn_media")
        self.btn_wake = QtWidgets.QPushButton(self.centralwidget)
        self.btn_wake.setGeometry(QtCore.QRect(657, 152, 241, 137))
        self.btn_wake.setStyleSheet("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/img/icon_待机压测.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_wake.setIcon(icon3)
        self.btn_wake.setIconSize(QtCore.QSize(56, 56))
        self.btn_wake.setObjectName("btn_wake")
        self.btn_monkey = QtWidgets.QPushButton(self.centralwidget)
        self.btn_monkey.setGeometry(QtCore.QRect(390, 315, 241, 137))
        self.btn_monkey.setStyleSheet("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/img/icon_monkey压测.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_monkey.setIcon(icon4)
        self.btn_monkey.setIconSize(QtCore.QSize(56, 56))
        self.btn_monkey.setObjectName("btn_monkey")
        self.btn_recorder = QtWidgets.QPushButton(self.centralwidget)
        self.btn_recorder.setGeometry(QtCore.QRect(657, 314, 241, 137))
        self.btn_recorder.setStyleSheet("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/img/icon_录制脚本.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_recorder.setIcon(icon5)
        self.btn_recorder.setIconSize(QtCore.QSize(56, 56))
        self.btn_recorder.setObjectName("btn_recorder")
        self.label_version = QtWidgets.QLabel(self.centralwidget)
        self.label_version.setGeometry(QtCore.QRect(840, 590, 171, 20))
        self.label_version.setStyleSheet("font-family: PingFangSC-Regular;\n"
"font-size: 12pt;\n"
"color: rgb(0,0,0);\n"
"")
        self.label_version.setObjectName("label_version")
        self.btn_scene_list = QtWidgets.QPushButton(self.centralwidget)
        self.btn_scene_list.setGeometry(QtCore.QRect(392, 475, 241, 65))
        self.btn_scene_list.setStyleSheet("QPushButton{\n"
"background: #FFFFFF;\n"
"box-shadow: 0 2px 12px 0 rgba(0,0,0,0.09);\n"
"}")
        self.btn_scene_list.setObjectName("btn_scene_list")
        self.btn_task_list = QtWidgets.QPushButton(self.centralwidget)
        self.btn_task_list.setGeometry(QtCore.QRect(658, 475, 241, 65))
        self.btn_task_list.setStyleSheet("")
        self.btn_task_list.setObjectName("btn_task_list")
        self.btn_script = QtWidgets.QPushButton(self.centralwidget)
        self.btn_script.setGeometry(QtCore.QRect(126, 475, 241, 65))
        self.btn_script.setStyleSheet("QPushButton{\n"
"color:  rgb(24,144,255)\n"
"font: 13pt \"新宋体\";\n"
"background-color: rgb(24,144,255)\n"
"border: 1px solid rgb(0, 0, 0);\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgb(10, 169, 255);\n"
"}")
        self.btn_script.setObjectName("btn_script")
        self.lb_name = QtWidgets.QLabel(self.centralwidget)
        self.lb_name.setGeometry(QtCore.QRect(172, 63, 161, 24))
        self.lb_name.setStyleSheet("font-family: PingFangSC-Semibold;\n"
"font-size: 23px;\n"
"color: rgba(0,0,0,0.85);\n"
"line-height: 23.61px;")
        self.lb_name.setObjectName("lb_name")
        self.lb_e_nane = QtWidgets.QLabel(self.centralwidget)
        self.lb_e_nane.setGeometry(QtCore.QRect(173, 88, 141, 16))
        self.lb_e_nane.setStyleSheet("font-family: PingFangSC-Regular;\n"
"font-size: 10.01px;\n"
"color: rgba(0,0,0,0.45);\n"
"line-height: 15.74px;")
        self.lb_e_nane.setObjectName("lb_e_nane")
        self.lb_logo = QtWidgets.QLabel(self.centralwidget)
        self.lb_logo.setGeometry(QtCore.QRect(109, 45, 63, 63))
        self.lb_logo.setStyleSheet("background-image:url();\n"
"")
        self.lb_logo.setText("")
        self.lb_logo.setPixmap(QtGui.QPixmap(":/img/首页图标.svg"))
        self.lb_logo.setObjectName("lb_logo")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "自动化测试平台"))
        self.btn_switch.setText(_translate("MainWindow", "开关机检测"))
        self.btn_source.setText(_translate("MainWindow", "信源检测"))
        self.btn_media.setText(_translate("MainWindow", "多媒体兼容性"))
        self.btn_wake.setText(_translate("MainWindow", "待机检测"))
        self.btn_monkey.setText(_translate("MainWindow", "系统可靠性"))
        self.btn_recorder.setText(_translate("MainWindow", "脚本开发"))
        self.label_version.setText(_translate("MainWindow", "V1.0.0 2020-06-18"))
        self.btn_scene_list.setText(_translate("MainWindow", "场景管理"))
        self.btn_task_list.setText(_translate("MainWindow", "任务管理"))
        self.btn_script.setText(_translate("MainWindow", "脚本管理"))
        self.lb_name.setText(_translate("MainWindow", "自动化测试平台"))
        self.lb_e_nane.setText(_translate("MainWindow", "Automated test platform"))

