import traceback
from PyQt5.QtCore import QThread, QCoreApplication, QObject, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDesktopWidget, QPushButton, QLabel, QLineEdit, QDialog, \
    QCheckBox
from PyQt5.QtGui import QPixmap
import datetime
import sys
import time
import requests
import os
import configparser
import json
import logging
import hashlib
import schedule
import threading
import SyncDao
import SyncWorker
import Scheduler
import global_v as gl


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.resize(1024, 768)
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self._title = "ShopYY产品同步 "
        self.setWindowTitle(self._title)
        btn_exit = QPushButton('退出', self)
        btn_exit.clicked.connect(QCoreApplication.instance().quit)
        btn_exit.resize(btn_exit.sizeHint())
        self.lbl_msg = QLabel('提示', self)
        self.chkbox_schedule = QCheckBox('产品同步自动化', self)
        self.chkbox_schedule.stateChanged.connect(self.changeSchedule)
        self.btn_export_api_goods = QPushButton("导出网站商品", self)
        self.btn_export_api_goods.clicked.connect(self.export_api_goods)
        # another line
        self.line_page_no = QLineEdit(self)
        self.line_page_no.setPlaceholderText("起始页码:1")
        self.btn_sync_full = QPushButton("全量同步", self)
        self.btn_sync_full.clicked.connect(self.sync_full)
        self.btn_sync_recent = QPushButton("增量同步", self)
        self.btn_sync_recent.clicked.connect(self.sync_recent)
        self.btn_sync_select = QPushButton("指定同步", self)
        self.btn_sync_select.clicked.connect(self.sync_select)
        # another line
        self.label_product_id = QLabel('ID', self)
        self.line_GoodsCode = QLineEdit('', self)
        self.btn_find_product = QPushButton("查找", self)
        self.btn_find_product.clicked.connect(self.find_product)
        self.lbl_product_name = QLabel('Name', self)
        self.lbl_product_created = QLabel('created', self)
        # spec window
        btn_spec = QPushButton("查看产品的规格", self)
        btn_spec.clicked.connect(self.show_spec_window)
        self.spec_window = ChildWindow()
        # image list
        self.lbl_product_large_image = QLabel('', self)
        self.lbl_product_logo = QLabel('', self)
        x = 10
        y = 5
        btn_exit.move(x, x)
        x = x + 100
        h = 44
        self.lbl_msg.move(x, y + 10)
        x = x + 450
        y = y + 44
        self.chkbox_schedule.setGeometry(x, y, 160, 44)
        self.btn_export_api_goods.setGeometry(x + 160 + 10, y + 5, 160, 34)
        # self.chkbox_schedule.toggle()
        # 换行
        # x = x + 450
        y = y + h
        w = 100
        self.line_page_no.setGeometry(x, y + 10, w, h - 20)
        x = x + w + 10
        w = 100
        self.btn_sync_full.setGeometry(x, y + 5, w, h - 10)
        x = x + w + 10
        w = 100
        self.btn_sync_recent.setGeometry(x, y + 5, w, h - 10)
        x = x + w + 10
        w = 100
        self.btn_sync_select.setGeometry(x, y + 5, w, h - 10)
        # 换行
        x = 10
        y = y + 44
        w = 60
        self.label_product_id.setGeometry(x, y + 10, w, h - 20)
        x = x + w + 10
        w = 100
        self.line_GoodsCode.setGeometry(x, y + 10, w, h - 20)
        x = x + w + 10
        w = 60
        self.btn_find_product.setGeometry(x, y + 5, w, h - 10)
        x = x + w + 10
        w = 400
        self.lbl_product_name.setGeometry(x, y, w, h)
        x = x + w + 100
        w = 100
        self.lbl_product_created.setGeometry(x, y, w, h)
        x = x + w + 10
        btn_spec.setGeometry(x, y + 5, 160, h - 10)
        y = y + 44 + 10
        self.lbl_product_logo.setGeometry(10, y + 250, 150, 150)
        self.lbl_product_large_image.setGeometry(170 + 50, y, 650, 650)
        self.show()
        self.counter = 0
        # thread and worker
        # 1 - create Worker and Thread inside the window
        self.worker = SyncWorker.SyncWorker()  # no parent!
        self.thread = QThread()  # no parent!
        # 2 - Connect Worker`s Signals to Form method slots to post data.
        self.worker.result.connect(self.print_output)
        # 3 - Move the Worker object to the Thread object
        self.worker.moveToThread(self.thread)
        # 4 - Connect Worker Signals to the Thread slots
        self.worker.finished.connect(self.thread_complete)
        # 5 - Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.worker.run)
        # * - Thread finished signal will close the app if you want!
        # self.thread.finished.connect(app.exit)
        # 6 - Start the thread
        self.line_GoodsCode.setText('')
        self.default_scheduler = Scheduler.Scheduler()

    def show_spec_window(self):
        try:
            productID = self.label_product_id.text()
            dao = SyncDao.EtlDao()
            spec_image = dao.select_product_spec_image(int(productID), 1)
            if not spec_image:
                self.showDialog("商品:" + productID + " 没有规格")
            else:
                self.spec_window.setWindowTitle("产品规格-" + str(spec_image["cc"]))
                self.spec_window.show_spec(spec_image)
                self.spec_window.show()
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
            print('#' * 60)

    def sync_full(self):
        page_no_str = self.line_page_no.text()
        try:
            page_no = int(page_no_str)
        except Exception as e:
            print(e)
            page_no = 1
        self.worker.page_no = page_no
        self.worker.sync_type = "full"
        self.thread.start()

    def sync_recent(self):
        self.worker.sync_type = "recent"
        self.thread.start()

    def sync_api_offline_goods(self):
        self.worker.sync_type = "goods_off_api"
        self.thread.start()

    def sync_select(self):
        self.worker.sync_type = "select"
        config = configparser.ConfigParser()
        init_file = os.path.normpath(os.path.join(os.curdir, "config", "ymcart.ini"))
        config.read(init_file)
        select_goods_codeno = self.line_GoodsCode.text()
        if len(select_goods_codeno) == 0:
            if config.has_option("api", "goods_codeno"):
                select_goods_codeno = config.get("api", "goods_codeno")
            else:
                select_goods_codeno = ""
        self.worker.select_goods_codeno = select_goods_codeno
        self.thread.start()
        print("select thread start")

    def export_api_goods(self):
        self.worker.sync_type = "export_goods_in_api"
        self.thread.start()

    def changeSchedule(self, state):
        if state == Qt.Checked:
            print("sync schedule start", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.setWindowTitle(self._title + " 自动化运行开启，每天0点全量同步，每5分钟产品下架同步，每5分钟产品修改和上架同步")
            self.sync_scheduler()
        else:
            self.default_scheduler.clear()
            print("sync schedule stop", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.setWindowTitle(self._title)

    def sync_scheduler(self):
        self.default_scheduler.every(5).minutes.do(self.sync_recent)
        self.default_scheduler.every().day.at("00:00").do(self.sync_full)
        self.default_scheduler.run_continuously(1)

    def find_product(self):
        try:
            GoodsCode = self.line_GoodsCode.text()
            dao = SyncDao.EtlDao()
            product_image = dao.select_product_image(GoodsCode)
            if not product_image:
                self.showDialog("商品:" + GoodsCode + " 没有信息")
            else:
                self.label_product_id.setText(str(product_image["ProductID"]))
                self.lbl_product_name.setText(product_image["ImageName"])
                self.lbl_product_created.setText(product_image["FileDate"])
                pixmap = QPixmap(product_image["ImageFilePath"])
                self.lbl_product_large_image.setPixmap(pixmap)
                self.lbl_product_large_image.setScaledContents(True)
                self.lbl_product_large_image.show()
                # 显示缩略图
                qp = QPixmap()
                qp.loadFromData(product_image["ThumbImage"], "JPEG", Qt.ImageConversionFlag.AutoColor)
                self.lbl_product_logo.setPixmap(qp)
                self.lbl_product_logo.setScaledContents(True)
                self.lbl_product_logo.show()
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
            print('#' * 60)

    def progress_fn(self, n):
        print("%d%% done" % n)

    def execute_this_fn(self, progress_callback):
        for n in range(0, 5):
            time.sleep(1)
            progress_callback.emit(n * 100 / 4)
        return "Done."

    def print_output(self, item):
        try:
            if "alert" in item:
                self.showDialog(item["alert"])
            elif "msg" in item:
                self.lbl_msg.setText(item["msg"])
                self.lbl_msg.resize(self.lbl_msg.sizeHint())
            elif "end" in item:
                self.worker.stop()
                self.thread.quit()
                self.thread.wait()
            elif "product" in item:
                product = item["product"]
                # print("emit product", product)
                GoodsCode = product["GoodsCode"]
                GoodsEName = product["GoodsEName"]
                dao = SyncDao.EtlDao()
                product_image = dao.select_product_image(GoodsCode)
                if not product_image:
                    self.showDialog("商品:" + str(GoodsCode) + " 没有信息")
                else:
                    self.label_product_id.setText(str(product["ProductID"]))
                    self.line_GoodsCode.setText(str(GoodsCode))
                    self.lbl_product_name.setText(GoodsEName)
                    self.lbl_product_created.setText(product_image["FileDate"])
                    """
                    pixmap = QPixmap(product_image["ImageFilePath"])
                    self.lbl_product_large_image.setPixmap(pixmap)
                    self.lbl_product_large_image.setScaledContents(True)
                    self.lbl_product_large_image.show()
                    """
                    # 显示缩略图
                    qp = QPixmap()
                    qp.loadFromData(product_image["ThumbImage"], "JPEG", Qt.ImageConversionFlag.AutoColor)
                    self.lbl_product_logo.setPixmap(qp)
                    self.lbl_product_logo.setScaledContents(True)
                    self.lbl_product_logo.show()
            else:
                print("-" * 60)
                print(item)
                print("-" * 60)
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

    def thread_complete(self):
        self.showDialog("运行结束" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("THREAD COMPLETE!")

    def stop_thread(self):
        self.worker.stop()
        self.thread.quit()
        self.thread.wait()

    def showDialog(self, msg):
        # 创建QDialog对象
        dialog = QDialog()
        lbl = QLabel(msg, dialog)
        lbl.move(10, 10)
        lbl.sizeHint()
        # 创建按钮到新创建的dialog对象中
        btn = QPushButton('ok', dialog)
        btn.clicked.connect(dialog.close)

        # 移动按钮，设置dialog的标题
        btn.move(50, 50)
        dialog.setWindowTitle(msg)
        # 设置窗口的属性为ApplicationModal模态，用户只有关闭弹窗后，才能关闭主界面
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def recurring_timer(self):
        self.counter += 1
        self.lbl_product_id.setText("Counter: %d" % self.counter)
        print("运行:" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


class ChildWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("产品规格")
        self.resize(800, 600)
        self.specCount = 1
        # spec window
        self.lbl_rowno = QLabel('行号', self)
        self.lbl_ProductID = QLabel('产品编号', self)
        self.lbl_SpecNo = QLabel('规格编号', self)
        self.lbl_GoodsSpec = QLabel('规格名称', self)
        self.lbl_FileDate = QLabel('创建时间', self)
        btn_prev = QPushButton("上一个", self)
        btn_prev.clicked.connect(self.show_spec_prev)
        btn_next = QPushButton("下一个", self)
        btn_next.clicked.connect(self.show_spec_next)
        self.lbl_large_image = QLabel(self)
        self.lbl_logo = QLabel(self)
        self.lbl_specActive = QLabel(self)
        self.lbl_status = QLabel(self)
        x = 10
        y = 5
        w = 30
        h = 40
        self.lbl_rowno.setGeometry(x, y, w, h)
        x = x + w + 10
        w = 60
        self.lbl_ProductID.setGeometry(x, y, w, h)
        x = x + w + 10
        self.lbl_SpecNo.setGeometry(x, y, w, h)
        x = x + w + 10
        w = 200
        self.lbl_GoodsSpec.setGeometry(x, y, w, h)
        x = x + w + 10
        self.lbl_FileDate.setGeometry(x, y, w, h)
        x = x + w + 10
        w = 60
        btn_prev.setGeometry(x, y, w, h)
        x = x + w + 10
        w = 60
        btn_next.setGeometry(x, y, w, h)
        x = 5
        y = y + h + 10
        w = 150
        h = 150
        self.lbl_logo.setGeometry(x, y, w, h)
        y2 = y + h + 10
        h = 40
        self.lbl_specActive.setGeometry(x, y2, w, h)
        y2 = y2 + h + 10
        self.lbl_status.setGeometry(x, y2, w, h)
        x = 5 + w + 10
        w = 500
        h = 500
        self.lbl_large_image.setGeometry(x, y, w, h)

    def show_spec(self, spec):
        self.specCount = spec["cc"]
        self.lbl_rowno.setText(str(spec["rowno"]))
        self.lbl_ProductID.setText(str(spec["ProductID"]))
        self.lbl_SpecNo.setText(spec["SpecNo"])
        self.lbl_GoodsSpec.setText(spec["GoodsSpec"])
        self.lbl_FileDate.setText(spec["FileDate"])
        self.lbl_specActive.setText("specActive=" + spec["specActive"])
        self.lbl_status.setText("status=" + spec["status"])
        pixmap = QPixmap(spec["ImageFilePath"])
        self.lbl_large_image.setPixmap(pixmap)
        self.lbl_large_image.setScaledContents(True)
        self.lbl_large_image.show()
        # 显示缩略图
        qp = QPixmap()
        qp.loadFromData(spec["ThumbImage"], "JPEG", Qt.ImageConversionFlag.AutoColor)
        self.lbl_logo.setPixmap(qp)
        self.lbl_logo.setScaledContents(True)
        self.lbl_logo.show()

    def show_spec_prev(self):
        try:
            rowno = int(self.lbl_rowno.text()) - 1
            if rowno < 0:
                rowno = self.specCount
            productID = self.lbl_ProductID.text()
            dao = SyncDao.EtlDao()
            spec_image = dao.select_product_spec_image(int(productID), rowno)
            print(spec_image)
            self.show_spec(spec_image)
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
            print('#' * 60)

    def show_spec_next(self):
        try:
            rowno = int(self.lbl_rowno.text()) + 1
            if rowno > self.specCount:
                rowno = 1
            productID = self.lbl_ProductID.text()
            dao = SyncDao.EtlDao()
            spec_image = dao.select_product_spec_image(int(productID), rowno)
            print(spec_image)
            self.show_spec(spec_image)
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
            print('#' * 60)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    init_file = os.path.normpath(os.path.join(os.curdir, "config", "ymcart.ini"))
    config.read(init_file)
    gl.pf_domain = config.get("api_pf", "domain_name")
    gl.pf_token = config.get("api_pf", "core_token")
    gl.ls_domain = config.get("api_ls", "domain_name")
    gl.ls_token = config.get("api_ls", "core_token")
    print(gl.ls_domain)
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
