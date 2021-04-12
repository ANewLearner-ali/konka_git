# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Entrance_View.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1001, 575)
        MainWindow.setAcceptDrops(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 1001, 91))
        self.label.setStyleSheet("color:rgb(255,255,255);\n"
"background-color:rgb(91,155,213);\n"
"font-size:30px;\n"
"font-weight:normal;\n"
"font-family:Arial;")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByKeyboard)
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(90, 180, 171, 91))
        self.pushButton_2.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"font: 75 18pt \"新宋体\";\n"
"background-color: rgb(90, 155, 213);\n"
"border: 2px solid rgb(65, 133, 156);\n"
"border-radius:12px\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(410, 180, 171, 91))
        self.pushButton_3.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"font: 75 18pt \"新宋体\";\n"
"background-color: rgb(90, 155, 213);\n"
"border: 2px solid rgb(65, 133, 156);\n"
"border-radius:12px\n"
"}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(730, 180, 171, 91))
        self.pushButton_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pushButton_4.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"font: 75 18pt \"新宋体\";\n"
"background-color: rgb(90, 155, 213);\n"
"border: 2px solid rgb(65, 133, 156);\n"
"border-radius:12px\n"
"}")
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(90, 360, 171, 91))
        self.pushButton_5.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"font: 75 18pt \"新宋体\";\n"
"background-color: rgb(90, 155, 213);\n"
"border: 2px solid rgb(65, 133, 156);\n"
"border-radius:12px\n"
"}")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(410, 360, 171, 91))
        self.pushButton_6.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"font: 75 18pt \"新宋体\";\n"
"background-color: rgb(90, 155, 213);\n"
"border: 2px solid rgb(65, 133, 156);\n"
"border-radius:12px\n"
"}")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_7 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_7.setGeometry(QtCore.QRect(730, 360, 171, 91))
        self.pushButton_7.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"font: 75 18pt \"新宋体\";\n"
"background-color: rgb(90, 155, 213);\n"
"border: 2px solid rgb(65, 133, 156);\n"
"border-radius:12px\n"
"}")
        self.pushButton_7.setObjectName("pushButton_7")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(890, 530, 61, 16))
        self.label_2.setStyleSheet("font: 75 15pt \"Calibri\";")
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(790, 50, 101, 41))
        self.pushButton.setStyleSheet("QPushButton{\n"
"color: rgb(0, 50, 0);\n"
"font: 15pt \"新宋体\";\n"
"background-color: rgb(85, 142, 213);\n"
"border: 1px solid rgb(0, 0, 0);\n"
"\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(900, 50, 91, 41))
        self.pushButton_8.setStyleSheet("QPushButton{\n"
"color: rgb(0, 50, 0);\n"
"font: 15pt \"新宋体\";\n"
"background-color: rgb(85, 142, 213);\n"
"border: 1px solid rgb(0, 0, 0);\n"
"\n"
"}")
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(690, 60, 91, 31))
        self.pushButton_9.setStyleSheet("QPushButton{\n"
"color: rgb(0, 0, 0);\n"
"font: 13pt \"新宋体\";\n"
"background-color: rgb(85, 142, 213);\n"
"border: 1px solid rgb(0, 0, 0);\n"
"}\n"
"QPushButton:hover{\n"
"background-color: rgb(10, 169, 255);\n"
"}")
        self.pushButton_9.setObjectName("pushButton_9")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "可靠性煲机工具"))
        self.label.setText(_translate("MainWindow", "平台可靠性自动化压测工具"))
        self.pushButton_2.setText(_translate("MainWindow", "开关机压测"))
        self.pushButton_3.setText(_translate("MainWindow", "信源煲机"))
        self.pushButton_4.setText(_translate("MainWindow", "视频类压测"))
        self.pushButton_5.setText(_translate("MainWindow", "待机压测"))
        self.pushButton_6.setText(_translate("MainWindow", "Monkey压测"))
        self.pushButton_7.setText(_translate("MainWindow", "录制脚本"))
        self.label_2.setText(_translate("MainWindow", "V1.0.0"))
        self.pushButton.setText(_translate("MainWindow", "场景列表"))
        self.pushButton_8.setText(_translate("MainWindow", "脚本列表"))
        self.pushButton_9.setText(_translate("MainWindow", "脚本调试"))

