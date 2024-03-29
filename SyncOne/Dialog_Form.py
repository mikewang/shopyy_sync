# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Dialog_Form.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(378, 318)
        self.btn_offline_full_sync = QtWidgets.QPushButton(Dialog)
        self.btn_offline_full_sync.setGeometry(QtCore.QRect(120, 210, 121, 23))
        self.btn_offline_full_sync.setObjectName("btn_offline_full_sync")
        self.btn_offline_recent_sync = QtWidgets.QPushButton(Dialog)
        self.btn_offline_recent_sync.setGeometry(QtCore.QRect(120, 240, 121, 23))
        self.btn_offline_recent_sync.setObjectName("btn_offline_recent_sync")
        self.btn_cancel = QtWidgets.QPushButton(Dialog)
        self.btn_cancel.setGeometry(QtCore.QRect(120, 280, 121, 23))
        self.btn_cancel.setObjectName("btn_cancel")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 30, 301, 20))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.btn_full_sync = QtWidgets.QPushButton(Dialog)
        self.btn_full_sync.setGeometry(QtCore.QRect(120, 120, 121, 23))
        self.btn_full_sync.setObjectName("btn_full_sync")
        self.btn_recent_sync = QtWidgets.QPushButton(Dialog)
        self.btn_recent_sync.setGeometry(QtCore.QRect(120, 150, 121, 23))
        self.btn_recent_sync.setObjectName("btn_recent_sync")
        self.comboBox_download_file = QtWidgets.QComboBox(Dialog)
        self.comboBox_download_file.setGeometry(QtCore.QRect(240, 60, 121, 22))
        self.comboBox_download_file.setObjectName("comboBox_download_file")
        self.comboBox_download_file.addItem("")
        self.comboBox_download_file.addItem("")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(10, 60, 161, 20))
        self.label_6.setObjectName("label_6")
        self.comboBox_sleep_time = QtWidgets.QComboBox(Dialog)
        self.comboBox_sleep_time.setGeometry(QtCore.QRect(180, 60, 41, 22))
        self.comboBox_sleep_time.setObjectName("comboBox_sleep_time")
        self.comboBox_sleep_time.addItem("")
        self.comboBox_sleep_time.addItem("")
        self.comboBox_sleep_time.addItem("")
        self.comboBox_sleep_time.addItem("")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btn_offline_full_sync.setText(_translate("Dialog", "下架产品全量同步"))
        self.btn_offline_recent_sync.setText(_translate("Dialog", "下架产品增量同步"))
        self.btn_cancel.setText(_translate("Dialog", "取消"))
        self.label.setText(_translate("Dialog", "产品同步操作"))
        self.btn_full_sync.setText(_translate("Dialog", "全量同步"))
        self.btn_recent_sync.setText(_translate("Dialog", "增量同步"))
        self.comboBox_download_file.setItemText(0, _translate("Dialog", "图片重新下载(否)"))
        self.comboBox_download_file.setItemText(1, _translate("Dialog", "图片重新下载(是)"))
        self.label_6.setText(_translate("Dialog", "每个产品同步的时间间隔秒数"))
        self.comboBox_sleep_time.setItemText(0, _translate("Dialog", "0"))
        self.comboBox_sleep_time.setItemText(1, _translate("Dialog", "3"))
        self.comboBox_sleep_time.setItemText(2, _translate("Dialog", "5"))
        self.comboBox_sleep_time.setItemText(3, _translate("Dialog", "10"))
