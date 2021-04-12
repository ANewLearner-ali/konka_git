# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tootip.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(299, 396)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 0, 291, 391))
        self.label.setStyleSheet("background-color: rgb(250,250,250);\n"
"border:2px rgb(0,162,219);\n"
"border-style:solid;\n"
"border-radius:10px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setGeometry(QtCore.QRect(10, 20, 271, 361))
        self.textBrowser.setStyleSheet("background-color: rgb(250,250,250);\n"
"border:none;\n"
"")
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(270, 0, 21, 21))
        self.pushButton.setStyleSheet("border:2px rgb(0,162,219);\n"
"border-style:solid;\n"
"border-radius:10px;")
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))

