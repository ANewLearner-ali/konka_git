# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'powerdown.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 633)
        MainWindow.setStyleSheet("QPushButton#pushButton_3 {\n"
"background: #000C17;\n"
"box-shadow: inset 0 2px 8px 0 rgba(0,0,0,0.45);\n"
"opacity: 0.65;\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: #FFFFFF;\n"
"line-height: 22px;\n"
"}\n"
"QPushButton#pushButton_2 {\n"
"background: #1890FF;\n"
"box-shadow: inset 0 2px 8px 0 rgba(0,0,0,0.45);\n"
"opacity: 0.65;\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: #FFFFFF;\n"
"line-height: 22px;\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(180, -20, 951, 671))
        self.tabWidget.setStyleSheet("QLabel {\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: rgba(0,0,0);\n"
"text-align: right;\n"
"line-height: 22px;\n"
"}\n"
"QCheckBox{\n"
"    font-family: PingFangSC-Regular;\n"
"    font-size: 14px;\n"
"    color: rgba(0,0,0,0.65);\n"
"    letter-spacing: 0;\n"
"    text-align: left;\n"
"    line-height: 22px;\n"
"}\n"
"QCheckBox::indicator{\n"
"    background: #FFFFFF;\n"
"    border: 1px solid #40A9FF;\n"
"    border-radius: 2px;\n"
"    border-radius: 2px;\n"
"    width: 12px;\n"
"    height: 12px;\n"
"}\n"
"QCheckBox::indicator:checked{\n"
"    image: url(./src/qss/复选-已选.svg);\n"
"}\n"
"QRadioButton {\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: rgba(0,0,0,0.65);\n"
"text-align: left;\n"
"line-height: 22px;}\n"
"QPushButton#pushButton_7,#pushButton_9 {\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: #FFFFFF;\n"
"line-height: 22px;\n"
"background: #1890FF;\n"
"border-radius: 4px;\n"
"border-radius: 4px;\n"
"}\n"
"QPushButton#pushButton_8,#pushButton_10 {\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: rgba(0,0,0,0.65);\n"
"line-height: 22px;\n"
"background: #FFFFFF;\n"
"border: 1px solid #D9D9D9;\n"
"border-radius: 4px;\n"
"border-radius: 4px;\n"
"}\n"
"QLineEdit{\n"
"background: #FFFFFF;\n"
"border: 1px solid rgba(0,0,0,0.15);\n"
"border-radius: 4px;\n"
"border-radius: 4px;\n"
"}")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(90, 110, 121, 51))
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setStyleSheet("")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setGeometry(QtCore.QRect(210, 120, 591, 32))
        self.lineEdit.setStyleSheet("")
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_7 = QtWidgets.QPushButton(self.tab)
        self.pushButton_7.setGeometry(QtCore.QRect(589, 550, 90, 32))
        self.pushButton_7.setStyleSheet("")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.tab)
        self.pushButton_8.setGeometry(QtCore.QRect(469, 550, 90, 32))
        self.pushButton_8.setStyleSheet("")
        self.pushButton_8.setObjectName("pushButton_8")
        self.checkBox_18 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_18.setGeometry(QtCore.QRect(210, 200, 161, 31))
        self.checkBox_18.setObjectName("checkBox_18")
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(100, 170, 111, 51))
        self.label_7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_7.setStyleSheet("")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.checkBox_21 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_21.setGeometry(QtCore.QRect(210, 250, 181, 31))
        self.checkBox_21.setObjectName("checkBox_21")
        self.checkBox_16 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_16.setGeometry(QtCore.QRect(360, 200, 281, 31))
        self.checkBox_16.setObjectName("checkBox_16")
        self.label_20 = QtWidgets.QLabel(self.tab)
        self.label_20.setGeometry(QtCore.QRect(110, 30, 71, 21))
        self.label_20.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_20.setStyleSheet("QLabel {\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: rgba(0,0,0,0.50);\n"
"line-height: 22px;}")
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName("label_20")
        self.label_14 = QtWidgets.QLabel(self.tab)
        self.label_14.setGeometry(QtCore.QRect(24, 30, 91, 21))
        self.label_14.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_14.setStyleSheet("QLabel {\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: rgba(0,0,0,0.65);\n"
"line-height: 22px;}")
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.tab)
        self.label_15.setGeometry(QtCore.QRect(95, 30, 21, 21))
        self.label_15.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_15.setStyleSheet("QLabel {\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: rgba(0,0,0,0.45);\n"
"line-height: 22px;}")
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_17 = QtWidgets.QLabel(self.tab_2)
        self.label_17.setGeometry(QtCore.QRect(90, 80, 121, 51))
        self.label_17.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_17.setStyleSheet("")
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.radioButton_5 = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_5.setGeometry(QtCore.QRect(200, 90, 61, 31))
        self.radioButton_5.setStyleSheet("QAbstractButton\n"
"{\n"
"font: 75 11pt \"新宋体\";\n"
"}")
        self.radioButton_5.setObjectName("radioButton_5")
        self.radioButton_6 = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_6.setGeometry(QtCore.QRect(280, 90, 71, 31))
        self.radioButton_6.setStyleSheet("QAbstractButton\n"
"{\n"
"font: 75 11pt \"新宋体\";\n"
"}")
        self.radioButton_6.setObjectName("radioButton_6")
        self.pushButton_9 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_9.setGeometry(QtCore.QRect(589, 550, 90, 32))
        self.pushButton_9.setStyleSheet("")
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_10.setGeometry(QtCore.QRect(469, 550, 90, 32))
        self.pushButton_10.setStyleSheet("")
        self.pushButton_10.setObjectName("pushButton_10")
        self.label_8 = QtWidgets.QLabel(self.tab_2)
        self.label_8.setGeometry(QtCore.QRect(90, 150, 111, 51))
        self.label_8.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_8.setStyleSheet("")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.checkBox_19 = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_19.setGeometry(QtCore.QRect(200, 190, 161, 31))
        self.checkBox_19.setObjectName("checkBox_19")
        self.checkBox_17 = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_17.setGeometry(QtCore.QRect(410, 190, 291, 31))
        self.checkBox_17.setObjectName("checkBox_17")
        self.checkBox_22 = QtWidgets.QCheckBox(self.tab_2)
        self.checkBox_22.setGeometry(QtCore.QRect(200, 240, 181, 31))
        self.checkBox_22.setObjectName("checkBox_22")
        self.label_16 = QtWidgets.QLabel(self.tab_2)
        self.label_16.setGeometry(QtCore.QRect(34, 30, 71, 21))
        self.label_16.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_16.setStyleSheet("QLabel {\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: rgba(0,0,0,0.65);\n"
"line-height: 22px;}")
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.label_18 = QtWidgets.QLabel(self.tab_2)
        self.label_18.setGeometry(QtCore.QRect(95, 30, 21, 21))
        self.label_18.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_18.setStyleSheet("QLabel {\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: rgba(0,0,0,0.45);\n"
"line-height: 22px;}")
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.label_21 = QtWidgets.QLabel(self.tab_2)
        self.label_21.setGeometry(QtCore.QRect(110, 30, 81, 21))
        self.label_21.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_21.setStyleSheet("QLabel {\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: rgba(0,0,0,0.50);\n"
"line-height: 22px;}")
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName("label_21")
        self.tabWidget.addTab(self.tab_2, "")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(0, 180, 181, 51))
        self.pushButton_3.setStyleSheet("")
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(0, 90, 180, 571))
        self.label_11.setStyleSheet("background: #001529;\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: #FFFFFF;\n"
"line-height: 22px;")
        self.label_11.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_11.setObjectName("label_11")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 180, 91))
        self.label.setStyleSheet("font-family: PingFangSC-Medium;\n"
"font-size: 23px;\n"
"color: #FFFFFF;\n"
"text-align: left;\n"
"background: #002140;\n"
"box-shadow: 2px 0 6px 0 rgba(0,21,41,0.35);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 130, 181, 51))
        self.pushButton_2.setStyleSheet("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.tabWidget.raise_()
        self.label_11.raise_()
        self.label.raise_()
        self.pushButton_2.raise_()
        self.pushButton_3.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "*待机标志:"))
        self.pushButton_7.setText(_translate("MainWindow", "创建场景"))
        self.pushButton_8.setText(_translate("MainWindow", "一键调试"))
        self.checkBox_18.setText(_translate("MainWindow", "待机是否正常"))
        self.label_7.setText(_translate("MainWindow", "检测内容:"))
        self.checkBox_21.setText(_translate("MainWindow", "开机是否正常"))
        self.checkBox_16.setText(_translate("MainWindow", "副屏是否正常（外置摄像头保存图片）"))
        self.label_20.setText(_translate("MainWindow", "待机唤醒"))
        self.label_14.setText(_translate("MainWindow", "待机压测"))
        self.label_15.setText(_translate("MainWindow", " / "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.label_17.setText(_translate("MainWindow", "*低功耗："))
        self.radioButton_5.setText(_translate("MainWindow", "是"))
        self.radioButton_6.setText(_translate("MainWindow", "否"))
        self.pushButton_9.setText(_translate("MainWindow", "创建场景"))
        self.pushButton_10.setText(_translate("MainWindow", "一键调试"))
        self.label_8.setText(_translate("MainWindow", "检测内容:"))
        self.checkBox_19.setText(_translate("MainWindow", "待机是否正常"))
        self.checkBox_17.setText(_translate("MainWindow", "副屏是否正常（外置摄像头保存图片）"))
        self.checkBox_22.setText(_translate("MainWindow", "开机是否正常"))
        self.label_16.setText(_translate("MainWindow", "待机压测"))
        self.label_18.setText(_translate("MainWindow", " / "))
        self.label_21.setText(_translate("MainWindow", "  AI待机唤醒"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.pushButton_3.setText(_translate("MainWindow", "  AI待机唤醒"))
        self.label_11.setText(_translate("MainWindow", "\n"
"      待机压测"))
        self.label.setText(_translate("MainWindow", "自动化测试"))
        self.pushButton_2.setText(_translate("MainWindow", "待机唤醒"))

