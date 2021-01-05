# -*- coding: utf-8 -*-
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import datetime
import traceback
from sync_single_website.Sync_Request_Api import SyncRequestApi as RequstApi
from sync_single_website.Sync_Write_Erp import SyncWriteErp as WriteErp
from sync_single_website import global_v as gl
import sys
import logging

class SyncWorker(QThread):
    signal = pyqtSignal(dict)
    worker_list = []
    _product_info_list_write_erp = []
    selected_goodscode = ""
    sync_sleep_time = 0
    
    def __init__(self):
        super(SyncWorker, self).__init__()
        print("thread inital", self)

    def __del__(self):
        print("auto del", self)
        self.wait()

    def callback_request_api(self, signal_message):
        # print("request callback", signal_message)
        self.signal.emit(signal_message)

    def callback_write_erp(self, signal_message):
        # print("request callback", signal_message)
        if "product.py" in signal_message:
            product_info = signal_message["product.py"]
            self.signal.emit({"message": "产品：" + product_info["GoodsCode"]})
            self._product_info_list_write_erp.append(product_info)
            print("同步产品", "第 " + str(len(self._product_info_list_write_erp)) + "个", product_info["GoodsCode"])
            signal_message["product.py"]["sync_no"] =  str(len(self._product_info_list_write_erp))
        self.signal.emit(signal_message)

    def sync_product_type(self, domain_name, token):
        request_api = RequstApi()
        request_api.signal.connect(self.callback_request_api)
        write_erp = WriteErp()
        write_erp.signal.connect(self.callback_write_erp)
        json_dict = request_api.request_category_list(domain_name, token)
        product_type_list = request_api.parse_category_list(domain_name, json_dict)
        # print(product_type_list)

        write_erp.write_product_type(domain_name, product_type_list)
        self.signal.emit({"message": "分类-同步完成"})

    def sync_product_info_full(self, domain_name, token):
        request_api = RequstApi()
        request_api.signal.connect(self.callback_request_api)
        write_erp = WriteErp()
        write_erp.sync_sleep_time = self.sync_sleep_time
        write_erp.signal.connect(self.callback_write_erp)
        self._product_info_list_write_erp = []
        page_no = 1
        page_cc = 0
        while True:
            if gl.worker_thread_isRunning == False:
                break
            json_dict = request_api.request_goods_list_full(domain_name, token, page_no)
            
            if "count" in json_dict:
                if page_no == 1:
                    cc = int(json_dict["count"])
                    message = "网站" + domain_name + "产品 " + str(cc) + " 个"
                    self.signal.emit({"message": message})
                if "data" in json_dict:
                    data = json_dict["data"]
                    if len(data) > 0:
                        page_cc = page_cc + len(data)
                        message = "网站" + domain_name + "第" + str(page_no) + \
                                  "页产品 " + str(len(data)) + " 个(" + str(page_cc) + "/" + str(cc) + ")"
                        self.signal.emit({"message": message})
                        # 分析 goods 的 json 数组
                        prod_info_list = request_api.parse_goods_list(domain_name, json_dict)
                        
                        write_erp.write_product_info(domain_name, prod_info_list)

                        # 下一页 继续，
                        if page_cc >= cc:
                            break
                        else:
                            page_no += 1
                    else:
                        break
                else:
                    break
            else:
                break

    def sync_product_info_recent(self, domain_name, token):
        request_api = RequstApi()
        request_api.signal.connect(self.callback_request_api)
        write_erp = WriteErp()
        write_erp.sync_sleep_time = self.sync_sleep_time
        write_erp.signal.connect(self.callback_write_erp)
        self._product_info_list_write_erp = []

        recent_prod_info_list = []
        recent_time = datetime.datetime.now() - datetime.timedelta(minutes=gl.recent_minutes)
        recent_time_str = recent_time.strftime('%Y-%m-%d %H:%M:%S')
        recent_type = "modify"
        page_no = 1
        page_cc = 0
        while True:
            if gl.worker_thread_isRunning == False:
                break
            json_dict = request_api.request_goods_list_recent(domain_name, token, recent_time_str, recent_type)
            
            if "count" in json_dict:
                if page_no == 1:
                    cc = int(json_dict["count"])
                    message = "网站" + domain_name + "最近修改的产品 " + str(cc) + " 个"
                    self.signal.emit({"message": message})
                if "data" in json_dict:
                    data = json_dict["data"]
                    if len(data) > 0:
                        page_cc = page_cc + len(data)
                        # 分析 goods 的 json 数组
                        prod_info_list = request_api.parse_goods_list(domain_name, json_dict)
                        
                        recent_prod_info_list = recent_prod_info_list + prod_info_list

                        # 下一页 继续，
                        if page_cc >= cc:
                            break
                        else:
                            page_no += 1
                    else:
                        break
                else:
                    break
            else:
                break
        recent_type = "create"
        page_no = 1
        page_cc = 0
        while True:
            if gl.worker_thread_isRunning == False:
                break
            json_dict = request_api.request_goods_list_recent(domain_name, token, recent_time_str, recent_type)
            
            if "count" in json_dict:
                if page_no == 1:
                    cc = int(json_dict["count"])
                    message = "网站" + domain_name + "最近新增的产品 " + str(cc) + " 个"
                    self.signal.emit({"message": message})
                if "data" in json_dict:
                    data = json_dict["data"]
                    if len(data) > 0:
                        page_cc = page_cc + len(data)
                        # 分析 goods 的 json 数组
                        prod_info_list = request_api.parse_goods_list(domain_name, json_dict)
                        
                        for prod in prod_info_list:
                            for prod2 in recent_prod_info_list:
                                if prod["ProductID"] == prod2["ProductID"]:
                                    prod_info_list.remove(prod)
                                    break
                        # 校验后剩余的产品
                        
                        recent_prod_info_list = recent_prod_info_list + prod_info_list
                        # 下一页 继续，
                        if page_cc >= cc:
                            break
                        else:
                            page_no += 1
                    else:
                        break
                else:
                    break
            else:
                break
        # write erp
        cc = len(recent_prod_info_list)
        message = "网站" + domain_name + "产品 " + str(cc) + " 个"
        self.signal.emit({"message": message})
        write_erp.write_product_info(domain_name, recent_prod_info_list)

    def sync_product_info_selected(self, domain_name, token, goodscode):
        request_api = RequstApi()
        request_api.signal.connect(self.callback_request_api)
        write_erp = WriteErp()
        write_erp.signal.connect(self.callback_write_erp)
        self._product_info_list_write_erp = []
        page_cc = 0
        json_dict = request_api.request_goods_list_selected(domain_name, token, goodscode)
        print("api json_dict", json_dict)
        if "count" in json_dict:
            cc = int(json_dict["count"])
            message = "网站" + domain_name + "产品 " + str(cc) + " 个"
            self.signal.emit({"message": message})
            if "data" in json_dict:
                data = json_dict["data"]
                if len(data) > 0:
                    page_cc = page_cc + len(data)
                    message = "网站" + domain_name + "产品 " + str(len(data)) + " 个(" + str(page_cc) + "/" + str(cc) + ")"
                    self.signal.emit({"message": message})
                    # 分析 goods 的 json 数组
                    prod_info_list = request_api.parse_goods_list(domain_name, json_dict)
                    print("parse prod_info_list", prod_info_list)
                    write_erp.write_product_info(domain_name, prod_info_list)
                else:
                    message = "网站" + domain_name + "页产品 " + goodscode + " 没有获取到它，请检查网站或重试。"
                    self.signal.emit({"message": message})

    def sync_product_info_full_offline(self, domain_name, token):
            request_api = RequstApi()
            request_api.signal.connect(self.callback_request_api)
            write_erp = WriteErp()
            write_erp.sync_sleep_time = self.sync_sleep_time
            write_erp.signal.connect(self.callback_write_erp)
            # 开始
            self._product_info_list_write_erp = []
            api_product_info_list = []
            page_no = 1
            page_cc = 0
            while True:
                if gl.worker_thread_isRunning == False:
                    break
                json_dict = request_api.request_goods_list_full(domain_name, token, page_no)
                
                if "count" in json_dict:
                    if page_no == 1:
                        cc = int(json_dict["count"])
                        message = "网站" + domain_name + "产品 " + str(cc) + " 个"
                        self.signal.emit({"message": message})
                    if "data" in json_dict:
                        data = json_dict["data"]
                        if len(data) > 0:
                            page_cc = page_cc + len(data)
                            message = "网站" + domain_name + "第" + str(page_no) + \
                                      "页产品 " + str(len(data)) + " 个(" + str(page_cc) + "/" + str(cc) + ")"
                            self.signal.emit({"message": message})
                            # 分析 goods 的 json 数组
                            prod_info_list = request_api.parse_goods_list(domain_name, json_dict)
                            
                            api_product_info_list = api_product_info_list + prod_info_list

                            # 下一页 继续，
                            if page_cc >= cc:
                                break
                            else:
                                page_no += 1
                        else:
                            break
                    else:
                        break
                else:
                    break
            # 比较数据库是否有 ，ERP有的,API没有的产品。
            write_erp.offline_product_info(domain_name, api_product_info_list, None)

    def sync_product_info_recent_offline(self, domain_name, token):
        request_api = RequstApi()
        request_api.signal.connect(self.callback_request_api)
        write_erp = WriteErp()
        write_erp.sync_sleep_time = self.sync_sleep_time
        write_erp.signal.connect(self.callback_write_erp)

        self._product_info_list_write_erp = []
        recent_prod_info_list = []
        recent_time = datetime.datetime.now() - datetime.timedelta(minutes=gl.recent_minutes)
        recent_time_str = recent_time.strftime('%Y-%m-%d %H:%M:%S')
        recent_type = "modify"
        page_no = 1
        page_cc = 0
        while True:
            if gl.worker_thread_isRunning == False:
                break
            json_dict = request_api.request_goods_list_recent_offline(domain_name, token, recent_time_str, recent_type)
            
            if "count" in json_dict:
                if page_no == 1:
                    cc = int(json_dict["count"])
                    message = "网站" + domain_name + "最近下架的产品 " + str(cc) + " 个"
                    self.signal.emit({"message": message})
                if "data" in json_dict:
                    data = json_dict["data"]
                    if len(data) > 0:
                        page_cc = page_cc + len(data)
                        # 分析 goods 的 json 数组
                        prod_info_list = request_api.parse_goods_list(domain_name, json_dict)
                        
                        recent_prod_info_list = recent_prod_info_list + prod_info_list

                        # 下一页 继续，
                        if page_cc >= cc:
                            break
                        else:
                            page_no += 1
                    else:
                        break
                else:
                    break
            else:
                break
        recent_type = "create"
        page_no = 1
        page_cc = 0
        while True:
            if gl.worker_thread_isRunning == False:
                break
            json_dict = request_api.request_goods_list_recent_offline(domain_name, token, recent_time_str, recent_type)
            
            if "count" in json_dict:
                if page_no == 1:
                    cc = int(json_dict["count"])
                    message = "网站" + domain_name + "最近下架的产品 " + str(cc) + " 个"
                    self.signal.emit({"message": message})
                if "data" in json_dict:
                    data = json_dict["data"]
                    if len(data) > 0:
                        page_cc = page_cc + len(data)
                        # 分析 goods 的 json 数组
                        prod_info_list = request_api.parse_goods_list(domain_name, json_dict)
                        
                        for prod in prod_info_list:
                            for prod2 in recent_prod_info_list:
                                if prod["ProductID"] == prod2["ProductID"]:
                                    prod_info_list.remove(prod)
                                    break;
                        # 校验后剩余的产品
                        
                        recent_prod_info_list = recent_prod_info_list + prod_info_list
                        # 下一页 继续，
                        if page_cc >= cc:
                            break
                        else:
                            page_no += 1
                    else:
                        break
                else:
                    break
            else:
                break
        # write erp
        # 比较数据库是否有 ，ERP有的,API没有的产品。
        write_erp.offline_product_info(domain_name, None, recent_prod_info_list)

    def query_product_info(self, GoodsCode):
        signal_emit = {"message": "查询产品:" + GoodsCode}
        self.signal.emit(signal_emit)
        write_erp = WriteErp()
        product_info = write_erp.query_product_info(GoodsCode)
        signal_emit = {"product.py": product_info}
        self.signal.emit(signal_emit)
        if product_info is None:
            message = "查询产品:" + GoodsCode + " 不存在。"
        else:
            product_image = product_info["product_image"]
            self.signal.emit({"product_image": product_image})
            product_spec_first = product_info["product_spec_first"]
            self.signal.emit({"product_spec_first": product_spec_first})
            message = "查询产品:" + GoodsCode + " 完成。"
        signal_emit = {"message": message}
        self.signal.emit(signal_emit)


    @pyqtSlot()
    def run(self):
        try:
            print("thread run..", self)
            gl.worker_thread_isRunning = True
            signal_emit = {"action": "begin"}
            self.signal.emit({"message": "同步操作开始 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            self.signal.emit(signal_emit)
            for worker in self.worker_list:
                if worker["name"] == "sync_product_type":
                    self.sync_product_type(worker["domain_name"], worker["token"])
                elif worker["name"] == "sync_product_info_full":
                    self.sync_product_info_full(worker["domain_name"], worker["token"])
                elif worker["name"] == "sync_product_info_recent":
                    self.sync_product_info_recent(worker["domain_name"], worker["token"])
                elif worker["name"] == "sync_product_info_full_offline":
                    self.sync_product_info_full_offline(worker["domain_name"], worker["token"])
                elif worker["name"] == "sync_product_info_recent_offline":
                    self.sync_product_info_recent_offline(worker["domain_name"], worker["token"])
                elif worker["name"] == "sync_product_info_selected":
                    self.sync_product_info_selected(worker["domain_name"], worker["token"], self.selected_goodscode)
                elif worker["name"] == "query_product_info":
                    self.query_product_info(self.selected_goodscode)
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
            logging.warning("数据同步" + " 在后台操作完成。" + str(self.worker_list))


