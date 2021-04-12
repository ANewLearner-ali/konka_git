# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'toast.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(364, 263)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(50, 220, 101, 41))
        self.pushButton.setStyleSheet("background-color:rgb(85, 170, 255);\n"
"border-radius: 6px;\n"
"color:rgb(255,255,255);\n"
"font: 15px")
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 0, 361, 241))
        self.label.setStyleSheet("background-color:rgb(248, 248, 248);\n"
"border-radius: 6px;\n"
"color:rgb(0,0,0);\n"
"border:2px rgb(117,174,138);\n"
"font: 75 16pt \"新宋体\";\n"
"border-style: solid;")
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(210, 220, 101, 41))
        self.pushButton_2.setStyleSheet("background-color:rgb(85, 170, 255);\n"
"border-radius: 6px;\n"
"color:rgb(255,255,255);\n"
"font:15px")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label.raise_()
        self.pushButton_2.raise_()
        self.pushButton.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "继续创建"))
        self.label.setText(_translate("Dialog", "TextLabel"))
        self.pushButton_2.setText(_translate("Dialog", "场景列表"))

