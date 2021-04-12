# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'source.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 633)
        MainWindow.setStyleSheet("QPushButton#pushButton_2{\n"
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
        self.tabWidget.setGeometry(QtCore.QRect(180, -20, 941, 661))
        self.tabWidget.setStyleSheet("QLabel {\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: rgba(0,0,0);\n"
"text-align: right;\n"
"line-height: 22px;\n"
"}\n"
"QLabel#label_11,#label_12,#label_13{\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 12px;\n"
"color: rgba(255,0,0);\n"
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
"QPushButton#pushButton_13,#pushButton_7,#pushButton_9{\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: #FFFFFF;\n"
"line-height: 22px;\n"
"background: #1890FF;\n"
"border-radius: 4px;\n"
"border-radius: 4px;\n"
"}\n"
"QPushButton#pushButton_8,#pushButton_10,#pushButton_14{\n"
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
"height: 32px;\n"
"}")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(90, 80, 121, 41))
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setStyleSheet("")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(90, 140, 121, 51))
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setStyleSheet("")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(90, 210, 121, 51))
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setStyleSheet("")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setGeometry(QtCore.QRect(90, 270, 121, 51))
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setStyleSheet("")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setGeometry(QtCore.QRect(400, 140, 121, 51))
        self.label_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_6.setStyleSheet("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setGeometry(QtCore.QRect(200, 150, 51, 32))
        self.lineEdit.setStyleSheet("")
        self.lineEdit.setObjectName("lineEdit")
        self.checkBox = QtWidgets.QCheckBox(self.tab)
        self.checkBox.setGeometry(QtCore.QRect(290, 80, 81, 41))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_2.setGeometry(QtCore.QRect(380, 80, 81, 41))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_3.setGeometry(QtCore.QRect(470, 80, 81, 41))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_4.setGeometry(QtCore.QRect(540, 80, 81, 41))
        self.checkBox_4.setObjectName("checkBox_4")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_2.setGeometry(QtCore.QRect(500, 150, 51, 32))
        self.lineEdit_2.setStyleSheet("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(560, 150, 31, 31))
        self.label_7.setStyleSheet("font: 75 12pt \"新宋体\";")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setGeometry(QtCore.QRect(400, 210, 121, 51))
        self.label_8.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_8.setStyleSheet("")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.checkBox_15 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_15.setGeometry(QtCore.QRect(200, 310, 161, 31))
        self.checkBox_15.setObjectName("checkBox_15")
        self.checkBox_17 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_17.setGeometry(QtCore.QRect(200, 350, 161, 31))
        self.checkBox_17.setObjectName("checkBox_17")
        self.checkBox_18 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_18.setGeometry(QtCore.QRect(380, 310, 161, 31))
        self.checkBox_18.setObjectName("checkBox_18")
        self.checkBox_20 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_20.setGeometry(QtCore.QRect(200, 390, 181, 31))
        self.checkBox_20.setObjectName("checkBox_20")
        self.checkBox_8 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_8.setGeometry(QtCore.QRect(200, 80, 81, 41))
        self.checkBox_8.setObjectName("checkBox_8")
        self.label_9 = QtWidgets.QLabel(self.tab)
        self.label_9.setGeometry(QtCore.QRect(250, 150, 21, 31))
        self.label_9.setStyleSheet("font: 75 12pt \"新宋体\";")
        self.label_9.setObjectName("label_9")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_3.setGeometry(QtCore.QRect(200, 220, 51, 32))
        self.lineEdit_3.setStyleSheet("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_10 = QtWidgets.QLabel(self.tab)
        self.label_10.setGeometry(QtCore.QRect(260, 220, 41, 31))
        self.label_10.setStyleSheet("font: 75 12pt \"新宋体\";")
        self.label_10.setObjectName("label_10")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_4.setGeometry(QtCore.QRect(500, 220, 311, 32))
        self.lineEdit_4.setStyleSheet("")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.pushButton_7 = QtWidgets.QPushButton(self.tab)
        self.pushButton_7.setGeometry(QtCore.QRect(589, 550, 90, 32))
        self.pushButton_7.setStyleSheet("")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.tab)
        self.pushButton_8.setGeometry(QtCore.QRect(469, 550, 90, 32))
        self.pushButton_8.setStyleSheet("")
        self.pushButton_8.setObjectName("pushButton_8")
        self.label_11 = QtWidgets.QLabel(self.tab)
        self.label_11.setGeometry(QtCore.QRect(280, 160, 111, 16))
        self.label_11.setStyleSheet("")
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.tab)
        self.label_12.setGeometry(QtCore.QRect(300, 230, 111, 16))
        self.label_12.setStyleSheet("")
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.tab)
        self.label_13.setGeometry(QtCore.QRect(600, 160, 111, 16))
        self.label_13.setStyleSheet("")
        self.label_13.setObjectName("label_13")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_5.setGeometry(QtCore.QRect(390, 390, 201, 32))
        self.lineEdit_5.setStyleSheet("")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_20 = QtWidgets.QLabel(self.tab)
        self.label_20.setGeometry(QtCore.QRect(100, 30, 71, 21))
        self.label_20.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_20.setStyleSheet("QLabel {\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: rgba(0,0,0,0.50);\n"
"line-height: 22px;}")
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName("label_20")
        self.label_15 = QtWidgets.QLabel(self.tab)
        self.label_15.setGeometry(QtCore.QRect(24, 30, 81, 21))
        self.label_15.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_15.setStyleSheet("QLabel {\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: rgba(0,0,0,0.65);\n"
"line-height: 22px;}")
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.tab)
        self.label_16.setGeometry(QtCore.QRect(90, 30, 21, 21))
        self.label_16.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_16.setStyleSheet("QLabel {\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: rgba(0,0,0,0.45);\n"
"line-height: 22px;}")
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.tab)
        self.label_17.setGeometry(QtCore.QRect(110, 80, 21, 41))
        self.label_17.setStyleSheet("color: rgb(227, 0, 17);")
        self.label_17.setObjectName("label_17")
        self.tabWidget.addTab(self.tab, "")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(0, 90, 180, 571))
        self.label_14.setStyleSheet("background: #001529;\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: #FFFFFF;\n"
"line-height: 22px;")
        self.label_14.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_14.setObjectName("label_14")
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
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "信源选择:"))
        self.label_3.setText(_translate("MainWindow", "信源切换\n"
"时间设置:"))
        self.label_4.setText(_translate("MainWindow", "检测间隔:"))
        self.label_5.setText(_translate("MainWindow", "检测内容:"))
        self.label_6.setText(_translate("MainWindow", "性能抓取\n"
"间隔时间:"))
        self.checkBox.setText(_translate("MainWindow", "HDMI2"))
        self.checkBox_2.setText(_translate("MainWindow", "HDMI3"))
        self.checkBox_3.setText(_translate("MainWindow", "ATV"))
        self.checkBox_4.setText(_translate("MainWindow", "DTMB"))
        self.label_7.setText(_translate("MainWindow", "分钟"))
        self.label_8.setText(_translate("MainWindow", "监测性能:"))
        self.checkBox_15.setText(_translate("MainWindow", "近场唤醒是否成功"))
        self.checkBox_17.setText(_translate("MainWindow", "遥控器是否回连成功"))
        self.checkBox_18.setText(_translate("MainWindow", "远场唤醒是否成功"))
        self.checkBox_20.setText(_translate("MainWindow", "蓝牙音箱是否回连成功"))
        self.checkBox_8.setText(_translate("MainWindow", "HDMI1"))
        self.label_9.setText(_translate("MainWindow", " H"))
        self.label_10.setText(_translate("MainWindow", "分钟"))
        self.pushButton_7.setText(_translate("MainWindow", "创建场景"))
        self.pushButton_8.setText(_translate("MainWindow", "一键调试"))
        self.label_11.setText(_translate("MainWindow", "！输入大于0的整数"))
        self.label_12.setText(_translate("MainWindow", "！输入大于0的整数"))
        self.label_13.setText(_translate("MainWindow", "！输入大于0的整数"))
        self.label_20.setText(_translate("MainWindow", "信源煲机"))
        self.label_15.setText(_translate("MainWindow", "信源煲机"))
        self.label_16.setText(_translate("MainWindow", " / "))
        self.label_17.setText(_translate("MainWindow", "*"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.label_14.setText(_translate("MainWindow", "\n"
"      信源煲机"))
        self.label.setText(_translate("MainWindow", "自动化测试"))
        self.pushButton_2.setText(_translate("MainWindow", "信源煲机"))

