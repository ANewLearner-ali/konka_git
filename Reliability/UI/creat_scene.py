# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'creat_scene.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_widget(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.setEnabled(True)
        widget.resize(506, 307)
        widget.setStyleSheet("backgroud-color:rgb(255, 255, 255);")
        self.pushButton = QtWidgets.QPushButton(widget)
        self.pushButton.setGeometry(QtCore.QRect(420, 250, 61, 41))
        self.pushButton.setStyleSheet("background-color: rgb(0, 112, 192);\n"
"color:rgb(255, 255, 255);\n"
"font: 75 11pt \"宋体\";")
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(widget)
        self.label.setGeometry(QtCore.QRect(0, 0, 501, 61))
        self.label.setStyleSheet("color:rgb(46,117,181);\n"
"background-color:rgb(255,255,255);\n"
"font-size:24px;\n"
"font-weight:Bold;\n"
"font-family:Arial;\n"
"")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(widget)
        self.label_2.setGeometry(QtCore.QRect(40, 110, 101, 41))
        self.label_2.setStyleSheet("color:rgb(0,0,0);\n"
"background-color:rgb(189,215,238);\n"
"font-size:18px;\n"
"font-weight:Bold;\n"
"font-family:Arial;")
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(widget)
        self.lineEdit.setGeometry(QtCore.QRect(170, 110, 271, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(widget)
        self.label_3.setGeometry(QtCore.QRect(40, 190, 101, 41))
        self.label_3.setStyleSheet("color:rgb(0,0,0);\n"
"background-color:rgb(189,215,238);\n"
"font-size:18px;\n"
"font-weight:Bold;\n"
"font-family:Arial;")
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(170, 190, 81, 41))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_4 = QtWidgets.QLabel(widget)
        self.label_4.setGeometry(QtCore.QRect(260, 200, 41, 31))
        self.label_4.setStyleSheet("color:rgb(0,0,0);\n"
"\n"
"font-size:18px;\n"
"")
        self.label_4.setObjectName("label_4")
        self.label.raise_()
        self.pushButton.raise_()
        self.label_2.raise_()
        self.lineEdit.raise_()
        self.label_3.raise_()
        self.lineEdit_2.raise_()
        self.label_4.raise_()

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "Form"))
        self.pushButton.setText(_translate("widget", "创建"))
        self.label.setText(_translate("widget", "创建场景>"))
        self.label_2.setText(_translate("widget", "场景名称:"))
        self.label_3.setText(_translate("widget", "执行次数:"))
        self.label_4.setText(_translate("widget", "次"))

