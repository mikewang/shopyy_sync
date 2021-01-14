# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Sync_Main_Form.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
 #导入程序运行必须模块
import sys
import datetime
import os
import configparser
import logging
#PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPixmap
from ModbusApp import Scheduler, Constant as gl
from ModbusApp.Main_Form import Ui_Form as MainForm
from ModbusApp.Cazor_Worker import CazorWorker as Worker


class MainWindow(QMainWindow, MainForm):
    _title = "嘉兆声光报警软件"
    _default_scheduler = None

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)
        self.setWindowTitle(self._title)
        self._default_scheduler = Scheduler.Scheduler()
        logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                            level=logging.WARNING,
                            filename='cazor.log',
                            filemode='a')
        self.checkBox_modbus_check.stateChanged.connect(self.start_auto_check_modbus)
        self.btn_modbus_start.clicked.connect(lambda: self.manual_check_modbus())
        self.btn_modbus_stop.clicked.connect(lambda: self.stop_sync())
        self.btn_alert_device.clicked.connect(self.check_alert_device)

        self.workerThread = Worker()
        self.workerThread.signal.connect(self.callback_worker)

    def start_auto_check_modbus(self, state):
        if state == Qt.Checked:
            print("check schedule start", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.setWindowTitle(self._title + " 自动化开启，每5分钟扫描一次")
            self.check_scheduler()
        else:
            self._default_scheduler.clear()
            print("check schedule stop", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.setWindowTitle(self._title)

    def check_scheduler(self):
        self._default_scheduler.every(5).minutes.do(self.check_scheduler_what)
        self._default_scheduler.run_continuously(1)

    def check_scheduler_what(self):
        try:
            sync_name = "modbus监测"
            print(sync_name, "开始", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            logging.warning(sync_name + " 开始")
            self.listWidget_modbus_log.addItem(sync_name + " 开始 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            if self.workerThread.isRunning():
                logging.warning(sync_name + "上一次未完成，此次取消")
                message = sync_name + " 上一次未完成，此次同步取消 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.listWidget_modbus_log.addItem(message)
                self.listWidget_modbus_log.scrollToBottom()
                return
            self.workerThread.sync_sleep_time = 0
            # 同步产品
            worker = {"name": "check_modbus_basic"}
            self.workerThread.worker_list.append(worker)
            print("workerThread start", self.workerThread)
            self.workerThread.start()
            logging.warning(sync_name + " 提交到后台")
        except Exception as e:
            print(e)

    def manual_check_modbus(self):
        try:
            sync_name = "modbus server"
            self.listWidget_modbus_log.clear()
            print(sync_name, "开始", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.listWidget_modbus_log.addItem(sync_name + " 开始 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            if self.workerThread.isRunning():
                message = sync_name + " 上一次未完成，此次取消 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.listWidget_modbus_log.addItem(message)
                self.listWidget_modbus_log.scrollToBottom()
                return
            # 同步产品
            worker = {"name": "check_modbus_basic"}
            self.workerThread.worker_list.append(worker)
            self.workerThread.start()
        except Exception as e:
            print(e)

    def stop_sync(self):
        try:
            self.listWidget_modbus_log.addItem("同步预停止, " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            gl.worker_thread_isRunning = False
            self.listWidget_modbus_log.addItem("同步已停止, " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        except Exception as e:
            print(e)

    def check_alert_device(self):
        try:
            self.listWidget_modbus_log.clear()
            self.listWidget_modbus_log.addItem("报警设备测试, " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            if self.workerThread.isRunning():
                message = " 上一次未完成，此次取消 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.listWidget_modbus_log.addItem(message)
                self.listWidget_modbus_log.scrollToBottom()
                return

            # 同步产品
            worker = {"name": "check_alert_basic"}
            self.workerThread.worker_list.append(worker)
            print("workerThread start", self.workerThread)
            self.workerThread.start()
        except Exception as e:
            print(e)

    def callback_worker(self, signal_emit):
        if "action" in signal_emit:
            action = signal_emit["action"]
            if action == "begin":
                self.listWidget_modbus_log.clear()
                self.listWidget_modbus_log.addItem("开始,- " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            elif action == "end":
                self.listWidget_modbus_log.addItem("完成,- " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                self.listWidget_modbus_log.scrollToBottom()
        elif "message" in signal_emit:
            message = signal_emit["message"]
            self.listWidget_modbus_log.addItem(message)
            self.listWidget_modbus_log.scrollToBottom()
        elif "modbus" in signal_emit:
            red_list, alarm = signal_emit["modbus"]
            message = str(red_list) + " " + alarm
            self.listWidget_modbus_log.addItem(message)
        else:
            print("callback", signal_emit)


if __name__ == '__main__':
    config = configparser.ConfigParser()
    init_file = os.path.normpath(os.path.join(os.curdir, "cazor.cfg"))
    config.read(init_file)
    # gl.pf_domain = config.get("api_pf", "domain_name")
    # gl.pf_token = config.get("api_pf", "core_token")
    # gl.ls_domain = config.get("api_ls", "domain_name")
    # gl.ls_token = config.get("api_ls", "core_token")
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
    # the end