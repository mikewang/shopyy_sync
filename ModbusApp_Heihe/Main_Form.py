# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main_Form.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(499, 392)
        Form.setMaximumSize(QtCore.QSize(500, 640))
        self.checkBox_modbus_check = QtWidgets.QCheckBox(Form)
        self.checkBox_modbus_check.setGeometry(QtCore.QRect(10, 10, 131, 31))
        self.checkBox_modbus_check.setObjectName("checkBox_modbus_check")
        self.btn_modbus_stop = QtWidgets.QPushButton(Form)
        self.btn_modbus_stop.setGeometry(QtCore.QRect(440, 10, 51, 31))
        self.btn_modbus_stop.setObjectName("btn_modbus_stop")
        self.listWidget_modbus_log = QtWidgets.QListWidget(Form)
        self.listWidget_modbus_log.setGeometry(QtCore.QRect(10, 50, 481, 261))
        self.listWidget_modbus_log.setObjectName("listWidget_modbus_log")
        self.btn_alert_device = QtWidgets.QPushButton(Form)
        self.btn_alert_device.setGeometry(QtCore.QRect(380, 330, 111, 31))
        self.btn_alert_device.setObjectName("btn_alert_device")
        self.btn_modbus_start = QtWidgets.QPushButton(Form)
        self.btn_modbus_start.setGeometry(QtCore.QRect(370, 10, 51, 31))
        self.btn_modbus_start.setObjectName("btn_modbus_start")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.checkBox_modbus_check.setText(_translate("Form", "声光报警自动运行"))
        self.btn_modbus_stop.setText(_translate("Form", "停止"))
        self.btn_alert_device.setText(_translate("Form", "测试报警设备"))
        self.btn_modbus_start.setText(_translate("Form", "开始"))
