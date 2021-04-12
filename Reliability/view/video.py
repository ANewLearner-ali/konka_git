# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'video.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1086, 647)
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
        self.tabWidget.setGeometry(QtCore.QRect(180, -20, 941, 671))
        self.tabWidget.setStyleSheet("QLabel {\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: rgba(0,0,0);\n"
"text-align: right;\n"
"line-height: 22px;\n"
"}\n"
"QLabel#label_15{\n"
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
        self.label_3.setGeometry(QtCore.QRect(70, 150, 121, 51))
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setStyleSheet("")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(100, 280, 101, 51))
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setStyleSheet("")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setGeometry(QtCore.QRect(90, 350, 121, 51))
        self.label_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_6.setStyleSheet("")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setGeometry(QtCore.QRect(210, 160, 591, 32))
        self.lineEdit.setStyleSheet("")
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.checkBox = QtWidgets.QCheckBox(self.tab)
        self.checkBox.setGeometry(QtCore.QRect(210, 90, 81, 21))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_2.setGeometry(QtCore.QRect(300, 90, 81, 21))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_3.setGeometry(QtCore.QRect(380, 90, 81, 21))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_4 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_4.setGeometry(QtCore.QRect(450, 90, 81, 21))
        self.checkBox_4.setObjectName("checkBox_4")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_2.setGeometry(QtCore.QRect(210, 300, 51, 32))
        self.lineEdit_2.setStyleSheet("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_7 = QtWidgets.QLabel(self.tab)
        self.label_7.setGeometry(QtCore.QRect(270, 300, 31, 31))
        self.label_7.setStyleSheet("font: 75 12pt \"新宋体\";")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.tab)
        self.label_8.setGeometry(QtCore.QRect(420, 290, 101, 51))
        self.label_8.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_8.setStyleSheet("")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.checkBox_15 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_15.setGeometry(QtCore.QRect(210, 430, 161, 31))
        self.checkBox_15.setObjectName("checkBox_15")
        self.checkBox_17 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_17.setGeometry(QtCore.QRect(210, 380, 161, 31))
        self.checkBox_17.setObjectName("checkBox_17")
        self.checkBox_18 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_18.setGeometry(QtCore.QRect(420, 430, 161, 31))
        self.checkBox_18.setObjectName("checkBox_18")
        self.checkBox_20 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_20.setGeometry(QtCore.QRect(420, 380, 181, 31))
        self.checkBox_20.setObjectName("checkBox_20")
        self.pushButton_7 = QtWidgets.QPushButton(self.tab)
        self.pushButton_7.setGeometry(QtCore.QRect(589, 550, 90, 32))
        self.pushButton_7.setStyleSheet("")
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_8 = QtWidgets.QPushButton(self.tab)
        self.pushButton_8.setGeometry(QtCore.QRect(469, 550, 90, 32))
        self.pushButton_8.setStyleSheet("")
        self.pushButton_8.setObjectName("pushButton_8")
        self.checkBox_8 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_8.setGeometry(QtCore.QRect(540, 90, 81, 21))
        self.checkBox_8.setObjectName("checkBox_8")
        self.checkBox_9 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_9.setGeometry(QtCore.QRect(620, 90, 81, 21))
        self.checkBox_9.setObjectName("checkBox_9")
        self.checkBox_10 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_10.setGeometry(QtCore.QRect(680, 90, 81, 21))
        self.checkBox_10.setObjectName("checkBox_10")
        self.checkBox_11 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_11.setGeometry(QtCore.QRect(210, 120, 141, 21))
        self.checkBox_11.setObjectName("checkBox_11")
        self.checkBox_12 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_12.setGeometry(QtCore.QRect(530, 120, 81, 21))
        self.checkBox_12.setObjectName("checkBox_12")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_3.setGeometry(QtCore.QRect(510, 300, 311, 32))
        self.lineEdit_3.setStyleSheet("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.checkBox_14 = QtWidgets.QCheckBox(self.tab)
        self.checkBox_14.setGeometry(QtCore.QRect(360, 120, 181, 21))
        self.checkBox_14.setObjectName("checkBox_14")
        self.label_15 = QtWidgets.QLabel(self.tab)
        self.label_15.setGeometry(QtCore.QRect(310, 310, 111, 16))
        self.label_15.setStyleSheet("")
        self.label_15.setObjectName("label_15")
        self.label_18 = QtWidgets.QLabel(self.tab)
        self.label_18.setGeometry(QtCore.QRect(70, 210, 121, 51))
        self.label_18.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_18.setStyleSheet("")
        self.label_18.setAlignment(QtCore.Qt.AlignCenter)
        self.label_18.setObjectName("label_18")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_8.setGeometry(QtCore.QRect(210, 220, 591, 32))
        self.lineEdit_8.setStyleSheet("")
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_9.setGeometry(QtCore.QRect(620, 380, 211, 32))
        self.lineEdit_9.setStyleSheet("")
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.label_37 = QtWidgets.QLabel(self.tab)
        self.label_37.setGeometry(QtCore.QRect(44, 40, 81, 21))
        self.label_37.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_37.setStyleSheet("QLabel {\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: rgba(0,0,0,0.65);\n"
"line-height: 22px;}")
        self.label_37.setAlignment(QtCore.Qt.AlignCenter)
        self.label_37.setObjectName("label_37")
        self.label_38 = QtWidgets.QLabel(self.tab)
        self.label_38.setGeometry(QtCore.QRect(140, 40, 91, 21))
        self.label_38.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_38.setStyleSheet("QLabel {\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: rgba(0,0,0,0.50);\n"
"line-height: 22px;}")
        self.label_38.setAlignment(QtCore.Qt.AlignCenter)
        self.label_38.setObjectName("label_38")
        self.label_39 = QtWidgets.QLabel(self.tab)
        self.label_39.setGeometry(QtCore.QRect(120, 40, 21, 21))
        self.label_39.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_39.setStyleSheet("QLabel {\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: rgba(0,0,0,0.45);\n"
"line-height: 22px;}")
        self.label_39.setAlignment(QtCore.Qt.AlignCenter)
        self.label_39.setObjectName("label_39")
        self.tabWidget.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.label_16 = QtWidgets.QLabel(self.tab_3)
        self.label_16.setGeometry(QtCore.QRect(60, 70, 121, 51))
        self.label_16.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_16.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 75 15pt \"新宋体\";\n"
"background-color: rgb(189, 215, 238);\n"
"")
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setObjectName("label_16")
        self.checkBox_19 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_19.setGeometry(QtCore.QRect(230, 80, 81, 21))
        self.checkBox_19.setObjectName("checkBox_19")
        self.checkBox_22 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_22.setGeometry(QtCore.QRect(360, 80, 121, 21))
        self.checkBox_22.setObjectName("checkBox_22")
        self.checkBox_23 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_23.setGeometry(QtCore.QRect(500, 80, 81, 21))
        self.checkBox_23.setObjectName("checkBox_23")
        self.pushButton_13 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_13.setGeometry(QtCore.QRect(800, 500, 91, 41))
        self.pushButton_13.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"font: 75 15pt \"新宋体\";\n"
"background-color: rgb(46, 117, 182);\n"
"border: 2px solid rgb(65, 133, 156);\n"
"\n"
"}")
        self.pushButton_13.setObjectName("pushButton_13")
        self.pushButton_14 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_14.setGeometry(QtCore.QRect(690, 500, 101, 41))
        self.pushButton_14.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"font: 75 15pt \"新宋体\";\n"
"background-color: rgb(46, 117, 182);\n"
"border: 2px solid rgb(65, 133, 156);\n"
"\n"
"}")
        self.pushButton_14.setObjectName("pushButton_14")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_4.setGeometry(QtCore.QRect(230, 270, 71, 41))
        self.lineEdit_4.setStyleSheet("border: 1px solid rgb(0, 0, 0);")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_5 = QtWidgets.QLabel(self.tab_3)
        self.label_5.setGeometry(QtCore.QRect(60, 270, 121, 51))
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 75 15pt \"新宋体\";\n"
"background-color: rgb(189, 215, 238);\n"
"")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_20 = QtWidgets.QLabel(self.tab_3)
        self.label_20.setGeometry(QtCore.QRect(60, 160, 121, 51))
        self.label_20.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_20.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 75 15pt \"新宋体\";\n"
"background-color: rgb(189, 215, 238);\n"
"")
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName("label_20")
        self.checkBox_16 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_16.setGeometry(QtCore.QRect(460, 420, 161, 31))
        self.checkBox_16.setObjectName("checkBox_16")
        self.label_9 = QtWidgets.QLabel(self.tab_3)
        self.label_9.setGeometry(QtCore.QRect(60, 370, 121, 51))
        self.label_9.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_9.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 75 15pt \"新宋体\";\n"
"background-color: rgb(189, 215, 238);\n"
"")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.checkBox_21 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_21.setGeometry(QtCore.QRect(250, 420, 161, 31))
        self.checkBox_21.setObjectName("checkBox_21")
        self.checkBox_31 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_31.setGeometry(QtCore.QRect(250, 470, 181, 31))
        self.checkBox_31.setObjectName("checkBox_31")
        self.checkBox_32 = QtWidgets.QCheckBox(self.tab_3)
        self.checkBox_32.setGeometry(QtCore.QRect(460, 470, 161, 31))
        self.checkBox_32.setObjectName("checkBox_32")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.tab_3)
        self.lineEdit_5.setGeometry(QtCore.QRect(230, 170, 61, 41))
        self.lineEdit_5.setStyleSheet("border: 1px solid rgb(0, 0, 0);")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_10 = QtWidgets.QLabel(self.tab_3)
        self.label_10.setGeometry(QtCore.QRect(300, 180, 41, 31))
        self.label_10.setStyleSheet("font: 75 12pt \"新宋体\";")
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.tab_3)
        self.label_11.setGeometry(QtCore.QRect(310, 280, 41, 31))
        self.label_11.setStyleSheet("font: 75 12pt \"新宋体\";")
        self.label_11.setObjectName("label_11")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_17 = QtWidgets.QLabel(self.tab_2)
        self.label_17.setGeometry(QtCore.QRect(60, 60, 121, 51))
        self.label_17.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_17.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 75 15pt \"新宋体\";\n"
"background-color: rgb(189, 215, 238);\n"
"")
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName("label_17")
        self.radioButton_5 = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_5.setGeometry(QtCore.QRect(230, 70, 81, 21))
        self.radioButton_5.setStyleSheet("QAbstractButton\n"
"{\n"
"font: 75 11pt \"新宋体\";\n"
"}")
        self.radioButton_5.setObjectName("radioButton_5")
        self.radioButton_6 = QtWidgets.QRadioButton(self.tab_2)
        self.radioButton_6.setGeometry(QtCore.QRect(360, 70, 111, 21))
        self.radioButton_6.setStyleSheet("QAbstractButton\n"
"{\n"
"font: 75 11pt \"新宋体\";\n"
"}")
        self.radioButton_6.setObjectName("radioButton_6")
        self.pushButton_9 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_9.setGeometry(QtCore.QRect(800, 500, 91, 41))
        self.pushButton_9.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"font: 75 15pt \"新宋体\";\n"
"background-color: rgb(46, 117, 182);\n"
"border: 2px solid rgb(65, 133, 156);\n"
"\n"
"}")
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_10 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_10.setGeometry(QtCore.QRect(690, 500, 101, 41))
        self.pushButton_10.setStyleSheet("QPushButton{\n"
"color: rgb(255, 255, 255);\n"
"font: 75 15pt \"新宋体\";\n"
"background-color: rgb(46, 117, 182);\n"
"border: 2px solid rgb(65, 133, 156);\n"
"\n"
"}")
        self.pushButton_10.setObjectName("pushButton_10")
        self.label_12 = QtWidgets.QLabel(self.tab_2)
        self.label_12.setGeometry(QtCore.QRect(310, 170, 41, 31))
        self.label_12.setStyleSheet("font: 75 12pt \"新宋体\";")
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.tab_2)
        self.label_13.setGeometry(QtCore.QRect(60, 170, 121, 51))
        self.label_13.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_13.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 75 15pt \"新宋体\";\n"
"background-color: rgb(189, 215, 238);\n"
"")
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_6.setGeometry(QtCore.QRect(230, 170, 71, 41))
        self.lineEdit_6.setStyleSheet("border: 1px solid rgb(0, 0, 0);")
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.label_14 = QtWidgets.QLabel(self.tab_2)
        self.label_14.setGeometry(QtCore.QRect(60, 280, 121, 51))
        self.label_14.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_14.setStyleSheet("color: rgb(0, 0, 0);\n"
"font: 75 15pt \"新宋体\";\n"
"background-color: rgb(189, 215, 238);\n"
"")
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_7.setGeometry(QtCore.QRect(230, 280, 561, 51))
        self.lineEdit_7.setStyleSheet("border: 1px solid rgb(0, 0, 0);")
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.tabWidget.addTab(self.tab_2, "")
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
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(0, 90, 180, 571))
        self.label_19.setStyleSheet("background: #001529;\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: #FFFFFF;\n"
"line-height: 22px;")
        self.label_19.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_19.setObjectName("label_19")
        self.label_19.raise_()
        self.tabWidget.raise_()
        self.label.raise_()
        self.pushButton_2.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "*视频商:"))
        self.label_3.setText(_translate("MainWindow", "在线视频起播命令\n"
"  配置文件PC路径："))
        self.label_4.setText(_translate("MainWindow", "性能抓取\n"
"间隔时间:"))
        self.label_6.setText(_translate("MainWindow", "检测内容:"))
        self.checkBox.setText(_translate("MainWindow", "腾讯视频"))
        self.checkBox_2.setText(_translate("MainWindow", "爱奇艺"))
        self.checkBox_3.setText(_translate("MainWindow", "酷喵"))
        self.checkBox_4.setText(_translate("MainWindow", "QQ音乐MV"))
        self.label_7.setText(_translate("MainWindow", "分钟"))
        self.label_8.setText(_translate("MainWindow", "监测性能:"))
        self.checkBox_15.setText(_translate("MainWindow", "近场唤醒是否成功"))
        self.checkBox_17.setText(_translate("MainWindow", "遥控器是否回连成功"))
        self.checkBox_18.setText(_translate("MainWindow", "远场唤醒是否成功"))
        self.checkBox_20.setText(_translate("MainWindow", "蓝牙音箱是否回连成功"))
        self.pushButton_7.setText(_translate("MainWindow", "创建场景"))
        self.pushButton_8.setText(_translate("MainWindow", "一键调试"))
        self.checkBox_8.setText(_translate("MainWindow", "QQ音乐"))
        self.checkBox_9.setText(_translate("MainWindow", "HDP"))
        self.checkBox_10.setText(_translate("MainWindow", "电视家"))
        self.checkBox_11.setText(_translate("MainWindow", "本地视频_大码率"))
        self.checkBox_12.setText(_translate("MainWindow", "信源"))
        self.checkBox_14.setText(_translate("MainWindow", "本地视频_混合编解码"))
        self.label_15.setText(_translate("MainWindow", "！输入大于0的整数"))
        self.label_18.setText(_translate("MainWindow", "本地视频资源\n"
"     TV端路径:"))
        self.label_37.setText(_translate("MainWindow", "视频类压测"))
        self.label_38.setText(_translate("MainWindow", "内置视频压测"))
        self.label_39.setText(_translate("MainWindow", " / "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.label_16.setText(_translate("MainWindow", "投屏模式："))
        self.checkBox_19.setText(_translate("MainWindow", "乐播投屏"))
        self.checkBox_22.setText(_translate("MainWindow", "dlna投屏"))
        self.checkBox_23.setText(_translate("MainWindow", "miracast（无线投屏）"))
        self.pushButton_13.setText(_translate("MainWindow", "创建场景"))
        self.pushButton_14.setText(_translate("MainWindow", "一键调试"))
        self.label_5.setText(_translate("MainWindow", "性能抓取\n"
"间隔时间:"))
        self.label_20.setText(_translate("MainWindow", "*直达应用："))
        self.checkBox_16.setText(_translate("MainWindow", "近场唤醒是否成功"))
        self.label_9.setText(_translate("MainWindow", "检测内容:"))
        self.checkBox_21.setText(_translate("MainWindow", "遥控器是否回连成功"))
        self.checkBox_31.setText(_translate("MainWindow", "蓝牙音箱是否回连成功"))
        self.checkBox_32.setText(_translate("MainWindow", "远场唤醒是否成功"))
        self.label_10.setText(_translate("MainWindow", " H"))
        self.label_11.setText(_translate("MainWindow", "分钟"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Page"))
        self.label_17.setText(_translate("MainWindow", "*视频选择："))
        self.radioButton_5.setText(_translate("MainWindow", "大码率"))
        self.radioButton_6.setText(_translate("MainWindow", "混合编解码"))
        self.pushButton_9.setText(_translate("MainWindow", "创建场景"))
        self.pushButton_10.setText(_translate("MainWindow", "一键调试"))
        self.label_12.setText(_translate("MainWindow", "分钟"))
        self.label_13.setText(_translate("MainWindow", "性能抓取\n"
"间隔时间:"))
        self.label_14.setText(_translate("MainWindow", "监测性能:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Tab 2"))
        self.label.setText(_translate("MainWindow", "自动化测试"))
        self.pushButton_2.setText(_translate("MainWindow", "内置视频压测"))
        self.label_19.setText(_translate("MainWindow", "\n"
"      视频类压测"))

