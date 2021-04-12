# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'task_manager.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1024, 633)
        Form.setWindowTitle("")
        Form.setStyleSheet("QPushButton#pushButton_2 {\n"
"background: #1890FF;\n"
"box-shadow: inset 0 2px 8px 0 rgba(0,0,0,0.45);\n"
"opacity: 0.65;\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: #FFFFFF;\n"
"line-height: 22px;\n"
"}\n"
"\n"
"")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1071, 781))
        self.widget.setObjectName("widget")
        self.tabWidget = QtWidgets.QTabWidget(self.widget)
        self.tabWidget.setGeometry(QtCore.QRect(180, 30, 844, 601))
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setStyleSheet("QTabBar::tab{\n"
"width: 80px;\n"
"height:30px;\n"
"font:12px;\n"
"color:black;\n"
"border: 1px solid black;}\n"
"QTabWidget::tab-bar{\n"
"        alignment:right;\n"
"}\n"
"QTabBar::tab:selected{\n"
"margin-left: 1;\n"
"margin-right: 0;\n"
"color: black;\n"
"border-color:rgb(217,217,217);\n"
"border: 1px solid black;\n"
"background-color:rgb(255, 255, 255);\n"
"margin-top: 6px;margin-bottom:6px;\n"
"} \n"
"QTabBar::tab:!selected{\n"
"margin-left: 1    ;\n"
"margin-right: 0;\n"
"color: black;\n"
"border: 1px solid black;\n"
"background-color:rgb(217,217,217);\n"
"margin-top: 10px;margin-bottom:2px;}\n"
"QTabWidget::pane{\n"
"top:-1px;\n"
"background-color:rgb(255,255,255);\n"
"}\n"
"\n"
"\n"
"\n"
"")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setElideMode(QtCore.Qt.ElideLeft)
        self.tabWidget.setUsesScrollButtons(True)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.tabWidget.addTab(self.tab_6, "")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(210, 30, 81, 31))
        self.pushButton.setStyleSheet("font-family: PingFangSC-Regular;\n"
"font-size: 9.33px;\n"
"color: #FFFFFF;\n"
"line-height: 14.67px;\n"
"background: #1890FF;\n"
"border-radius: 2.67px;\n"
"border-radius: 2.67px;")
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 180, 91))
        self.label_2.setStyleSheet("font-family: PingFangSC-Medium;\n"
"font-size: 23px;\n"
"color: #FFFFFF;\n"
"text-align: left;\n"
"background: #002140;\n"
"box-shadow: 2px 0 6px 0 rgba(0,21,41,0.35);")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 90, 181, 40))
        self.pushButton_2.setStyleSheet("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.label_11 = QtWidgets.QLabel(self.widget)
        self.label_11.setGeometry(QtCore.QRect(0, 90, 180, 571))
        self.label_11.setStyleSheet("background: #001529;\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: #FFFFFF;\n"
"line-height: 22px;")
        self.label_11.setText("")
        self.label_11.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_11.setObjectName("label_11")
        self.tabWidget.raise_()
        self.pushButton.raise_()
        self.label_2.raise_()
        self.label_11.raise_()
        self.pushButton_2.raise_()

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("Form", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("Form", "Tab 2"))
        self.pushButton.setText(_translate("Form", "报告路径"))
        self.label_2.setText(_translate("Form", "自动化测试"))
        self.pushButton_2.setText(_translate("Form", "任务列表"))

