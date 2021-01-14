# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import datetime
import traceback
import sys
import logging
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
from ModbusApp import Scheduler, Constant as gl


class CazorWorker(QThread):
    signal = pyqtSignal(dict)
    worker_list = []
    sync_sleep_time = 0

    def __init__(self):
        super(CazorWorker, self).__init__()
        print("thread initial", self)

    def __del__(self):
        print("auto del", self)
        self.wait()

    def modbus_tcp(ip="11.101.102.180"):
        print("加载modbus_tk 完成")
        red = []
        alarm = ""
        try:
            # 设定串口为从站
            master = modbus_tcp.TcpMaster()
            master.set_timeout(5.0)
            master.set_verbose(True)
            red = master.execute(6, cst.READ_HOLDING_REGISTERS, 40100, 2)  # 这里可以修改需要读取的功能码
            # print(red)
            alarm = "正常"
            return list(red), alarm
        except Exception as exc:
            # print(str(exc))
            alarm = (str(exc))
            return red, alarm  ##如果异常就返回[],故障信息

    def check_modbus_basic(self):
        self.signal.emit({"message": "检查开始1"})
        red_list, alarm = self.modbus_tcp()
        self.signal.emit({"modbus": (red_list, alarm)})
        self.signal.emit({"message": "检查完成2"})

    def check_alert_device(self):
        self.signal.emit({"message": "测试声光报警设备"})

    @pyqtSlot()
    def run(self):
        try:
            print("thread run..", self)
            gl.worker_thread_isRunning = True
            signal_emit = {"action": "begin"}
            self.signal.emit(signal_emit)
            self.signal.emit({"message": "操作开始 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

            for worker in self.worker_list:
                if worker["name"] == "check_modbus_basic":
                    self.check_modbus_basic()
                elif worker["name"] == "check_alert_basic":
                    self.check_alert_device()
            self.signal.emit({"message": "操作结束 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # Get information about the exception that is currently being handled
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print('e.message:\t', exc_value)
            print("Note, object e and exc of Class %s is %s the same." %
                  (type(exc_value), ('not', '')[exc_value is e]))
            print('traceback.print_exc(): ', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            print('*' * 60)
        else:
            print("thread result", self)
        finally:
            gl.worker_thread_isRunning = False
            signal_emit = {"action": "end"}
            self.signal.emit(signal_emit)
            print("thread end..", self)
            logging.warning("扫描操作" + " 在后台完成。" + str(self.worker_list))


