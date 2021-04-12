# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sence_task.ui'
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
        Form.setStyleSheet("QPushButton#pushButton_3 {\n"
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
"QLabel#label {\n"
"font-family: PingFangSC-Regular;\n"
"font-size: 14px;\n"
"color: rgba(0,0,0,0.65);\n"
"line-height: 22px;\n"
"}\n"
"")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(0, 0, 1071, 781))
        self.widget.setObjectName("widget")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setGeometry(QtCore.QRect(900, 20, 91, 31))
        self.pushButton_3.setStyleSheet("font-family: PingFangSC-Regular;\n"
"font-size: 9.33px;\n"
"color: #FFFFFF;\n"
"line-height: 14.67px;\n"
"background: #1890FF;\n"
"border-radius: 2.67px;\n"
"border-radius: 2.67px;")
        self.pushButton_3.setObjectName("pushButton_3")
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setGeometry(QtCore.QRect(180, 110, 844, 531))
        self.tableWidget.setStyleSheet("QTableWidget{\n"
"font: 12pt \"宋体\";\n"
"}\n"
"QPushButton{font: 75 10pt \"新宋体\"; };")
        self.tableWidget.setAutoScroll(True)
        self.tableWidget.setDragEnabled(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tableWidget.setTextElideMode(QtCore.Qt.ElideRight)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(25)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(30)
        self.tableWidget.verticalHeader().setHighlightSections(False)
        self.tableWidget.verticalHeader().setMinimumSectionSize(25)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        self.tableWidget_2 = QtWidgets.QTableWidget(self.widget)
        self.tableWidget_2.setGeometry(QtCore.QRect(180, 70, 844, 41))
        self.tableWidget_2.setStyleSheet("font-family: PingFangSC-Medium;\n"
"font-size: 9.33px;\n"
"color: rgba(0,0,0,0.85);\n"
"line-height: 14.67px;")
        self.tableWidget_2.setAutoScroll(True)
        self.tableWidget_2.setDragEnabled(False)
        self.tableWidget_2.setAlternatingRowColors(True)
        self.tableWidget_2.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tableWidget_2.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tableWidget_2.setTextElideMode(QtCore.Qt.ElideRight)
        self.tableWidget_2.setShowGrid(True)
        self.tableWidget_2.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(1)
        self.tableWidget_2.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        self.tableWidget_2.horizontalHeader().setVisible(False)
        self.tableWidget_2.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget_2.horizontalHeader().setHighlightSections(True)
        self.tableWidget_2.horizontalHeader().setMinimumSectionSize(25)
        self.tableWidget_2.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.tableWidget_2.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget_2.verticalHeader().setDefaultSectionSize(30)
        self.tableWidget_2.verticalHeader().setHighlightSections(False)
        self.tableWidget_2.verticalHeader().setMinimumSectionSize(25)
        self.tableWidget_2.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget_2.verticalHeader().setStretchLastSection(False)
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
        self.pushButton_3.raise_()
        self.tableWidget.raise_()
        self.tableWidget_2.raise_()
        self.label_11.raise_()
        self.label_2.raise_()
        self.pushButton_2.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        self.pushButton_3.setText(_translate("Form", "创建任务"))
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "场景名称"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Form", "创建日期"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Form", "执行次数/时长"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("Form", "环境依赖"))
        self.tableWidget_2.setSortingEnabled(False)
        self.pushButton_2.setText(_translate("Form", "场景列表"))
        self.label_2.setText(_translate("Form", "自动化测试"))

