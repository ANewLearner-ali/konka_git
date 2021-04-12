# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'debug_tootip.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(432, 396)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 0, 381, 331))
        self.label.setStyleSheet("background-color: rgb(250,250,250);\n"
"border:3px rgb(90,155,213);\n"
"border-style:solid;\n"
"border-radius:10px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(30, 30, 321, 281))
        self.textBrowser.setStyleSheet("background-color: rgb(250,250,250);\n"
"border:none;\n"
"")
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(360, 0, 21, 21))
        self.pushButton.setStyleSheet("border:3px rgb(90,155,213);\n"
"border-style:solid;\n"
"border-radius:10px;")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

