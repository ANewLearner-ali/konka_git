# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'device_choose.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_widget(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(622, 293)
        widget.setStyleSheet("background: #FFFFFF;")
        self.pushButton = QtWidgets.QPushButton(widget)
        self.pushButton.setGeometry(QtCore.QRect(480, 240, 90, 32))
        self.pushButton.setStyleSheet("background: #1890FF;\n"
"border-radius: 4px;\n"
"border-radius: 4px;\n"
"font-size: 14px;\n"
"color: #FFFFFF;\n"
"line-height: 22px;")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(widget)
        self.pushButton_2.setGeometry(QtCore.QRect(510, 10, 41, 23))
        self.pushButton_2.setStyleSheet("background: #1890FF;\n"
"border-radius: 4px;\n"
"border-radius: 4px;\n"
"font-size: 14px;\n"
"color: #FFFFFF;\n"
"line-height: 22px;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.tableWidget = QtWidgets.QTableWidget(widget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 60, 621, 161))
        self.tableWidget.setStyleSheet("QTableView {\n"
"    border:none;\n"
"}\n"
"QTableWidget::item:selected { background-color: rgb(255,255,255) }")
        self.tableWidget.setShowGrid(False)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.label = QtWidgets.QLabel(widget)
        self.label.setGeometry(QtCore.QRect(0, 0, 621, 51))
        self.label.setStyleSheet("border: 1px solid #666666;\n"
"font-family: PingFangSC-Medium;\n"
"font-size: 16px;\n"
"color: rgba(0,0,0,0.85);\n"
"line-height: 21px;\n"
"border: none;\n"
"border-bottom:1px solid rgba(0,0,0,0.15);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.checkBox = QtWidgets.QCheckBox(widget)
        self.checkBox.setGeometry(QtCore.QRect(320, 240, 171, 31))
        self.checkBox.setStyleSheet("font-family: PingFangSC-Regular;\n"
"font-size: 12px;\n"
"color: #F5222D;\n"
"letter-spacing: 0;\n"
"line-height: 18px;\n"
"")
        self.checkBox.setTristate(False)
        self.checkBox.setObjectName("checkBox")
        self.label.raise_()
        self.pushButton_2.raise_()
        self.tableWidget.raise_()
        self.checkBox.raise_()
        self.pushButton.raise_()

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "Form"))
        self.pushButton.setText(_translate("widget", "创建"))
        self.pushButton_2.setText(_translate("widget", "+"))
        self.label.setText(_translate("widget", "创建任务"))
        self.checkBox.setText(_translate("widget", "有串口命令且已连接串口"))

from view import main_rc
