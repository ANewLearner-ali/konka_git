# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'choose_recorder.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_widget(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.setEnabled(True)
        widget.resize(656, 225)
        widget.setStyleSheet("backgroud-color:rgb(255, 255, 255);")
        self.pushButton = QtWidgets.QPushButton(widget)
        self.pushButton.setGeometry(QtCore.QRect(540, 100, 41, 41))
        self.pushButton.setStyleSheet("border-style:None")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(widget)
        self.label.setGeometry(QtCore.QRect(0, 0, 651, 61))
        self.label.setStyleSheet("color:rgb(46,117,181);\n"
"background-color:rgb(255,255,255);\n"
"font-size:24px;\n"
"font-weight:Bold;\n"
"font-family:Arial;\n"
"")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(widget)
        self.label_2.setGeometry(QtCore.QRect(10, 100, 131, 41))
        self.label_2.setStyleSheet("color:rgb(0,0,0);\n"
"background-color:rgb(189,215,238);\n"
"font-size:15px;\n"
"font-family:Arial;")
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(widget)
        self.lineEdit.setGeometry(QtCore.QRect(160, 100, 351, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(widget)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 170, 161, 41))
        self.pushButton_2.setStyleSheet("background-color: rgb(0, 112, 192);\n"
"color:rgb(255, 255, 255);\n"
"font: 75 11pt \"宋体\";")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label.raise_()
        self.pushButton.raise_()
        self.label_2.raise_()
        self.lineEdit.raise_()
        self.pushButton_2.raise_()

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "Form"))
        self.label.setText(_translate("widget", "录制脚本 >"))
        self.label_2.setText(_translate("widget", "脚本录制工具路径："))
        self.pushButton_2.setText(_translate("widget", "启动脚本录制工具"))

