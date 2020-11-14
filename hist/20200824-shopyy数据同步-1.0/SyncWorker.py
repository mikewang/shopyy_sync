import traceback
from PyQt5.QtCore import QThread, QCoreApplication, QObject, pyqtSignal, pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDesktopWidget, QPushButton, QLabel, QLineEdit, QDialog
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
import pandas as pd
import SyncDao



class SyncWorker(QObject):
    """
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(dict)
    progress = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        # Store constructor arguments (re-used for processing)
        self.page_no = 1
        self.select_goods_id = ""
        self.sync_type = ""
        self._isRunning = False
        self.api_online_goods = []
        self.api_offline_goods = []
        config = configparser.ConfigParser()
        init_file = os.path.normpath(os.path.join(os.curdir, "config", "ymcart.ini"))
        config.read(init_file)
        self._domain_name = config.get("api", "domain_name")
        self._common_token = config.get("api", "common_token")
        self._core_token = config.get("api", "core_token")
        if config.has_option("api", "recent_minutes"):
            self.recent_minutes = config.get("api", "recent_minutes")
        else:
            self.recent_minutes = 1440
        if config.has_option("api", "write_database"):
            self._sync_write_database = config.get("api", "write_database")
        else:
            self._sync_write_database = True
        # print("self._sync_write_database", self._sync_write_database)
        self._session = requests.session()
        self._goods_count = 0

    @pyqtSlot()
    def run(self):
        msg = ' 开始 ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(msg)
        if not self._isRunning:
            self._isRunning = True
        else:
            self.result.emit({"alert": "同步正在运行"})
            return

        self.result.emit({"msg": msg})
        if self.sync_type == "full":
            self._goods_count = 0
            sync_items = ["category", "full_goods"]
            self.api_online_goods = []
            for item_name in sync_items:
                self.sync_request_api(item_name)
            # 反向同步，网站下架
            if len(self.api_online_goods) > 100:
                self.sync_all_product_erp_database()
            self.api_online_goods = []
            self.stop()
            print("产品全量同步完成 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.result.emit({"end": "full goods"})
        elif self.sync_type == "recent":
            self.api_online_goods = []
            self._goods_count = 0
            sync_items = ["category", "recent_goods"]
            for item_name in sync_items:
                self.sync_request_api(item_name)
            # 反向同步 ，增量的产品的 spec 下架
            self.sync_product_spec_erp_database()
            self.api_online_goods = []
            # 反向 下架 产品
            self.api_offline_goods = []
            self.sync_request_api("goods_off_api")
            # 反向同步，网站下架
            if len(self.api_offline_goods) > 0:
                self.sync_offline_product_erp_database()
            print("产品下架:" + str(len(self.api_offline_goods)) + " 同步完成 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.api_offline_goods = []
            # 停止线程
            self.stop()
            print("产品增量同步完成 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.result.emit({"end": "select goods"})
        elif self.sync_type == "select":
            self.api_online_goods = []
            self._goods_count = 1
            self.sync_request_api("select_goods")
            # 反向同步 ，增量的产品的 spec 下架
            self.sync_product_spec_erp_database()
            self.api_online_goods = []
            self.stop()
            print("指定产品同步完成 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.result.emit({"end": "select goods"})
        if self.sync_type == "goods_off_api":
            self.api_offline_goods = []
            self.sync_request_api("goods_off_api")
            # 反向同步，网站下架
            if len(self.api_offline_goods) > 0:
                self.sync_offline_product_erp_database()
            self.api_offline_goods = []
            # 产品检查完成
            self.stop()
            print("产品下架同步完成 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.result.emit({"end": "sync goodsID"})
        if self.sync_type == "export_goods_in_api":
            self.sync_request_api("export_goods_in_api")
            self.stop()
            print("产品全量检查完成 " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            self.result.emit({"end": "export goods"})
        print("程序执行正常结束，goods count=" + str(self._goods_count))

    def stop(self):
        self._isRunning = False

    def request_categoryList(self):
        try:
            api = "api-erp-categoryList.html"
            print('请求' + api + ' 开始 ', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            url = self._domain_name + api
            data = {'token': self._core_token}
            response = self._session.post(url, data=data)
            print(url)
            response_text = ""
            if response.status_code == 200:
                response_text = response.text
            else:
                print("response.status_code=" + str(response.status_code))
            print('请求' + api + ' 结束 ', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            return response_text
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
            return None

    def parse_categoryList(self, json_str):
        json_dict = json.loads(json_str)
        logging.info(json_dict)
        code = json_dict["code"]
        data_array = json_dict["data"]
        product_type_list = []
        # Insert into Product_Type(ProductTypeID,ParentID,TypeName,SortID) values()
        if self._domain_name == "http://45915.us01.ymcart.com/":
            product_type = {'ProductTypeID': 10000, 'ParentID': -1, 'TypeName': "批发", 'SortID': 0}
            product_type_list.append(product_type)
            for item in data_array:
                category_id = item["id"]
                category_parent_id = item["parent_id"]
                category_base_name = item["base_name"]
                category_listorder = item["listorder"]
                # print(category_id, category_base_name, category_listorder)
                if category_parent_id == "0":
                    category_parent_id = "10000"
                product_type = {'ProductTypeID': int(category_id), 'ParentID': int(category_parent_id),
                                'TypeName': category_base_name,
                                'SortID': int(category_listorder)}
                product_type_list.append(product_type)
        elif self._domain_name == "http://32676.us01.ymcart.com/":
            product_type = {'ProductTypeID': 10001, 'ParentID': -1, 'TypeName': "零售", 'SortID': 0}
            product_type_list.append(product_type)
            for item in data_array:
                category_id = item["id"]
                category_parent_id = item["parent_id"]
                category_base_name = item["base_name"]
                category_listorder = item["listorder"]
                # print(category_id, category_base_name, category_listorder)
                if category_parent_id == "0":
                    category_parent_id = "10001"
                product_type = {'ProductTypeID': int(category_id), 'ParentID': int(category_parent_id),
                                'TypeName': category_base_name,
                                'SortID': int(category_listorder)}
                product_type_list.append(product_type)
        return product_type_list

    def request_goodsList(self, page_no, get_type, recent_minutes, goods_id):
        try:
            api = "api-commonErp-goodsList.html"
            msg = '请求' + api + ' 开始 ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(msg)
            # self.result.emit({"msg":msg})
            start_time = datetime.datetime.now() - datetime.timedelta(minutes=recent_minutes)
            start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
            url = self._domain_name + api
            if get_type == "full":
                data = {'token': self._core_token, "page_size": 10, "page_no": page_no, "status": 1}
            elif get_type == "offline":
                data = {'token': self._core_token, "page_size": 10, "page_no": page_no, "status": 0, "start_modify_time": start_time_str}
            elif get_type == "select":
                #print("select goods", goods_id)
                data = {'token': self._core_token, "page_size": 10, "page_no": page_no, "status": 1, "id": goods_id}
            elif get_type == "modify":
                data = {'token': self._core_token, "page_size": 10, "page_no": page_no, "start_modify_time": start_time_str, "status": 1}
            elif get_type == "create":
                data = {'token': self._core_token, "page_size": 10, "page_no": page_no, "start_time": start_time_str, "status": 1}
            else:
                data = ""
            # session = requests.Session()
            response = self._session.post(url, data=data)
            print(url)
            response_text = ""
            if response.status_code == 200:
                response_text = response.text
            else:
                print("response.status_code=" + str(response.status_code))
            print('请求' + api + ' 结束 ', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            return response_text
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
            return None

    def parse_goodsList_spec2image_only(self, json_str):
        json_dict = json.loads(json_str)
        logging.info(json_dict)
        print("parse_goodsList", json_dict)
        code = json_dict["code"]
        count = json_dict["count"]
        product_data_array = json_dict["data"]
        product_info_list = []
        for item in product_data_array:
            # 遍历产品数据 开始
            product_info = self.parse_goods_info(item)
            product_spec_list = []
            if "sku" in item:
                goods_sku = item["sku"]
                if goods_sku is not None:
                    for sku_item in goods_sku:
                        # print(sku_item)
                        product_spec = self.parse_goods_sku(sku_item)
                        product_spec["MinOrder"] = int(product_info["body_product_spec"]["moq"])
                        product_spec["mxoq"] = int(product_info["body_product_spec"]["mxoq"])
                        # set RecGuid
                        year = product_spec["SysNoTime"].split('-')[0]
                        month = product_spec["SysNoTime"].split('-')[1]
                        day = product_spec["SysNoTime"].split('-')[2].split(" ")[0]
                        md = hashlib.md5()
                        md.update((str(product_spec["ProductID"]) + str(product_spec["SpecNo"])).encode('utf-8'))
                        RecGuid = year + month + day + md.hexdigest().upper()
                        product_spec["RecGuid"] = RecGuid
                        SysNo = datetime.datetime.strptime(product_spec["SysNoTime"], '%Y-%m-%d %H:%M:%S')
                        product_spec["SysNo"] = SysNo
                        product_spec_list.append(product_spec)
            product_image_list = []
            if "images_album" in item:
                goods_images_album = item["images_album"]
                if goods_images_album is not None:
                    # print("goods_images_album", goods_images_album)
                    if "spec_name" in goods_images_album and "spec_image" in goods_images_album:
                        spec_name = goods_images_album["spec_name"]
                        spec_image_array = goods_images_album["spec_image"]
                        if spec_name is not None and spec_image_array is not None:
                            for spec_image in spec_image_array:
                                sku_value = spec_name + ":" + spec_image["muti_spec_value"]
                                product_image = {"sku_value": sku_value, "image": spec_image["image"]}
                                for product_spec in product_spec_list:
                                    sku_value_list = product_spec["sku_value"].split("<br />")
                                    if sku_value in sku_value_list and RecGuid not in product_image:
                                        product_image["RecGuid"] = product_spec["RecGuid"]
                                        product_image["SysNoTime"] = product_spec["SysNoTime"]
                                        product_image["LastEditTime"] = product_spec["LastEditTime"]
                                        break
                                if "RecGuid" not in product_image:
                                    print("product_image RecGuid is none", product_image, product_info)
                                else:
                                    product_image_list.append(product_image)
            product_spec_list_2 = []
            for product_spec in product_spec_list:
                sku_value_list = product_spec["sku_value"].split("<br />")
                for product_image in product_image_list:
                    if product_image["sku_value"] in sku_value_list:
                        product_spec["RecGuid"] = product_image["RecGuid"]
                        break
                product_spec_list_2.append(product_spec)
            # 设置数据
            product_info["product_spec"] = product_spec_list_2
            product_info["product_image"] = product_image_list
            logging.info(product_info)
            product_info_list.append(product_info)
            # print(product_info)
            # 继续遍历下一个产品数据，直到数组结束
        print("-"*200)
        return product_info_list

    def parse_goodsList(self, json_str):
        json_dict = json.loads(json_str)
        logging.info(json_dict)
        # print("parse_goodsList", json_dict)
        code = json_dict["code"]
        count = json_dict["count"]
        product_data_array = json_dict["data"]
        product_info_list = []
        for item in product_data_array:
            # 遍历产品数据 开始
            product_info = self.parse_goods_info(item)
            product_spec_list = []
            product_image_list = []
            if "sku" in item:
                goods_sku = item["sku"]
                if goods_sku is not None:
                    for sku_item in goods_sku:
                        # print(sku_item)
                        product_spec = self.parse_goods_sku(sku_item)
                        product_spec["MinOrder"] = int(product_info["body_product_spec"]["moq"])
                        product_spec["mxoq"] = int(product_info["body_product_spec"]["mxoq"])
                        # set RecGuid
                        year = product_spec["SysNoTime"].split('-')[0]
                        month = product_spec["SysNoTime"].split('-')[1]
                        day = product_spec["SysNoTime"].split('-')[2].split(" ")[0]
                        md = hashlib.md5()
                        md.update((str(product_spec["ProductID"]) + str(product_spec["SpecNo"])).encode('utf-8'))
                        RecGuid = year + month + day + md.hexdigest().upper()
                        product_spec["RecGuid"] = RecGuid
                        SysNo = datetime.datetime.strptime(product_spec["SysNoTime"], '%Y-%m-%d %H:%M:%S')
                        product_spec["SysNo"] = SysNo
                        # image recguid add
                        if "images_album" in item:
                            goods_images_album = item["images_album"]
                            if goods_images_album is not None:
                                # print("goods_images_album", goods_images_album)
                                if "spec_name" in goods_images_album and "spec_image" in goods_images_album:
                                    spec_name = goods_images_album["spec_name"]
                                    spec_image_array = goods_images_album["spec_image"]
                                    if spec_name is not None and spec_image_array is not None:
                                        product_image = {}
                                        for spec_image in spec_image_array:
                                            sku_value = spec_name + ":" + spec_image["muti_spec_value"]
                                            product_image["sku_value"] = sku_value
                                            product_image["image"] = spec_image["image"]
                                            sku_value_list = product_spec["sku_value"].split("<br />")
                                            if sku_value in sku_value_list:
                                                product_image["RecGuid"] = product_spec["RecGuid"]
                                                product_image["SysNoTime"] = product_spec["SysNoTime"]
                                                product_image["LastEditTime"] = product_spec["LastEditTime"]
                                                break
                                        if "RecGuid" not in product_image:
                                            print("product_image RecGuid is none", product_image, product_info)
                                        else:
                                            product_image_list.append(product_image)
                        # print(product_spec["SpecNo"], product_spec["RecGuid"])
                        product_spec_list.append(product_spec)
            # product_spec and product_image 设置完毕，一对一
            # 设置数据
            product_info["product_spec"] = product_spec_list
            product_info["product_image"] = product_image_list
            logging.info(product_info)
            product_info_list.append(product_info)
            # print(product_info)
            # 继续遍历下一个产品数据，直到数组结束
        print("-"*200)
        return product_info_list

    def parse_goods_info(self, item):
        goods_id = item["id"]
        # print(goods_id)
        if "base_name" in item:
            base_name = item["base_name"]
        else:
            base_name = ""
        # 商品编号,真正的主键
        if self._domain_name == "http://45915.us01.ymcart.com/":
            goods_codeno = "PF-" + item["codeno"]
        elif self._domain_name == "http://32676.us01.ymcart.com/":
            goods_codeno = "LS-" + item["codeno"]
        else:
            goods_codeno = item["codeno"]
        if "image" in item:
            image_url = item["image"]
            if image_url is None:
                image_url = ""
            else:
                pass
                # print(goods_codeno, image_url)
        else:
            image_url = ""
        if "price" in item:
            price = item["price"]
        else:
            price = "0"
        if "weight" in item:
            weight = item["weight"]
        else:
            weight = "0"
        if "volume" in item:
            volume = item["volume"]
        else:
            volume = "0"
        if "brand_id" in item:
            brand_id = item["brand_id"]
            if brand_id is None:
                brand_id = ""
        else:
            brand_id = ""
        if "brand_name" in item:
            brand_name = item["brand_name"]
            if brand_name is None:
                brand_name = ""
        else:
            brand_name = ""
        if "goods_type_id" in item:
            goods_type_id = item["goods_type_id"]
            if goods_type_id is None:
                goods_type_id = ""
        else:
            goods_type_id = ""
        if "category_id" in item:
            category_id = item["category_id"]
            if category_id is None:
                category_id = ""
        else:
            category_id = ""
        if "category_name" in item:
            category_name = item["category_name"]
            if category_name is None:
                category_name = ""
        else:
            category_name = ""
        if "spec_mode" in item:
            spec_mode = item["spec_mode"]
            if spec_mode is None:
                spec_mode = ""
        else:
            spec_mode = ""
        if "moq" in item:
            moq = item["moq"]
            if moq is None:
                moq = "0"
        else:
            moq = "0"
        if "mxoq" in item:
            mxoq = item["mxoq"]
            if mxoq is None:
                mxoq = "0"
        else:
            mxoq = "0"
        create_time = item["create_time"]
        if "modify_time" in item:
            modify_time = item["modify_time"]
        else:
            modify_time = "0"
        goods_create_time_str = datetime.datetime.fromtimestamp(
            int(create_time)
        ).strftime('%Y-%m-%d %H:%M:%S')
        goods_modify_time_str = datetime.datetime.fromtimestamp(
            int(modify_time)
        ).strftime('%Y-%m-%d %H:%M:%S')
        if "stock_nums" in item:
            stock_nums = item["stock_nums"]
        else:
            stock_nums = 99999
        # print(goods_id, category_id, goods_codeno, base_name, goods_create_time_str, goods_modify_time_str, brand_id,
        # brand_name, goods_type_id, category_na
        #                     SysNo = int(time.mktime(product_type["SysNoTime"]))ght, volume, spec_mode, moq, mxoq)
        body_product_spec = {"brand_id": brand_id, "brand_name": brand_name, "goods_type_id": goods_type_id,
                             "category_name": category_name,
                             "price": price, "weight": weight, "volume": volume, "spec_mode": spec_mode, "moq": moq,
                             "mxoq": mxoq}
        product_info = {"ProductID": int(goods_id), "TypeID": int(category_id), "GoodsCode": goods_codeno,
                        "GoodsEName": base_name, "stock_nums": stock_nums,
                        "CreateDate": goods_create_time_str, "EditDate": goods_modify_time_str, "image": image_url,
                        "body_product_spec": body_product_spec}
        return product_info

    def parse_goods_sku(self, item):
        sku_id = item["id"]
        if "goods_id" in item:
            goods_id = item["goods_id"]
        sku_code = item["codeno"]
        if sku_code is None:
            sku_code = ""
        if sku_code == "":
            sku_code = item["sku_code"]
        sku_value = item["sku_value"]
        price = item["price"]
        weight = item["weight"]
        volume = item["volume"]
        stock_nums = item["stock_nums"]
        if "create_time" in item:
            create_time = item["create_time"]
        else:
            create_time = "0"
        create_time_str = datetime.datetime.fromtimestamp(
            int(create_time)
        ).strftime('%Y-%m-%d %H:%M:%S')
        if "update_time" in item:
            update_time = item["update_time"]
        else:
            update_time = "0"
        update_time_str = datetime.datetime.fromtimestamp(
            int(update_time)
        ).strftime('%Y-%m-%d %H:%M:%S')
        # print(goods_id, sku_id, sku_code, sku_value, price, weight, volume, create_time_str, update_time_str)
        product_spec = {"ProductSpecID": int(sku_id), "ProductID": int(goods_id), "SpecNo": sku_code,
                        "GoodsSpec": sku_value, "OuterBulk": float(volume), "GrossWeight": float(weight),
                        "FOBPrice": float(price), "stock_nums": stock_nums,
                        "SysNoTime": create_time_str, "LastEditTime": update_time_str, "sku_value": sku_value}
        return product_spec

    def merge_product_info(self, product_info):
        self.merge_force_product_info(product_info, None)

    def merge_force_product_info(self, product_info, sync_type):
        # 保存全局对象，用于 反向删除操作
        stock_nums = product_info["stock_nums"]
        # stock_nums = 0 , 则不同步到erp中，在erp反向操作时，将erp中的产品下架，因为已经是库存为0
        if int(stock_nums) > 0:
            self.api_online_goods.append(product_info)
            # 前端 界面显示
            # 开始 保存到数据库
            # 保存商品的主信息
            dao = SyncDao.EtlDao()
            print("同步开始", product_info["ProductID"], "序号", self._goods_count + 1,
                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            dao.merge_product_info(product_info)
            # 保存商品的图片
            dao.merge_product_image(product_info, None, sync_type)
            # 保存 商品的规格
            # print(product_info["product_spec"])
            for product_spec in product_info["product_spec"]:
                # print("product_spec",product_spec)
                dao.merge_product_spec(product_spec)
                dao.merge_Product_Material_Info(product_spec, product_info)
            for spec_image in product_info["product_image"]:
                # print("spec_image", spec_image)
                dao.merge_product_image(product_info, spec_image, sync_type)
            # 保存到数据库操作完成。
            # 设置 产品及附加的主图
            # print("设置 产品及附加的主图", product_info["ProductID"])
            dao.update_product_default_image(product_info["ProductID"])
            spec_mode = (product_info["body_product_spec"])["spec_mode"]
            if spec_mode != "1":
                if len(product_info["product_spec"]) == 1:
                    product_spec = product_info["product_spec"][0]
                    RecGuid = product_spec["RecGuid"]
                    dao.merge_product_single_spec_image(product_info)
                else:
                    print("非多规格产品", product_info["ProductID"], "修改规格图失败")
        else:
            print("该产品不同步，其库存为0：", product_info)
        # 设置 产品序号
        self._goods_count += 1
        print("同步结束", product_info["ProductID"], "序号", self._goods_count,
              datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("-" * 100)
        # 前端界面显示
        self.result.emit({"product.py": product_info})
        time.sleep(1)

    def sync_all_product_erp_database(self):
        dao = SyncDao.EtlDao()
        # 先同步所有的商品，如果erp数据库有，而网站没有，则删除erp数据库的商品
        # 再同步erp数据库中剩下所有商品的所有规格，如果erp数据库中该商品的规格比网站多，则删除erp中该商品的多余的规格
        dao_prod_set = set()
        api_prod_set = set()
        dao_prod_list = dao.select_product_info(self._domain_name)
        for dao_prod in dao_prod_list:
            dao_prod_set.add(int(dao_prod["ProductID"]))
        for api_prod in self.api_online_goods:
            api_prod_set.add(int(api_prod["ProductID"]))
        sync_set = dao_prod_set.difference(api_prod_set)
        print("erp数据库中要删除的商品:", sync_set)
        for dao_productID in sync_set:
            dao.offline_product_info(dao_productID)

    def sync_offline_product_erp_database(self):
        dao = SyncDao.EtlDao()
        # 先同步所有的商品，如果erp数据库有，而网站没有，则删除erp数据库的商品
        # 再同步erp数据库中剩下所有商品的所有规格，如果erp数据库中该商品的规格比网站多，则删除erp中该商品的多余的规格
        dao_prod_set = set()
        api_prod_set = set()
        dao_prod_list = dao.select_product_info(self._domain_name)
        for dao_prod in dao_prod_list:
            if dao_prod["Status"] == 0 and dao_prod["ProductActive"] == 0:
                dao_prod_set.add(int(dao_prod["ProductID"]))
        for api_prod in self.api_offline_goods:
            api_prod_set.add(int(api_prod["ProductID"]))
        sync_set = api_prod_set.intersection(dao_prod_set)
        print("erp数据库中要下架的商品:", sync_set)
        for dao_productID in sync_set:
            dao.offline_product_info(dao_productID)

    def sync_product_spec_erp_database(self):
        dao = SyncDao.EtlDao()
        # 只同步单个商品，如果erp数据库中该商品的规格比网站多，则删除erp中该商品的多余的规格
        for prod in self.api_online_goods:
            productID = prod["ProductID"]
            dao_spec_list = dao.select_product_spec(prod)
            dao_spec_set = set()
            api_spec_set = set()
            for dao_spec in dao_spec_list:
                dao_spec_set.add(dao_spec["SpecNo"])
            # print("dao_spec", dao_spec_set)
            for api_spec in prod["product_spec"]:
                api_spec_set.add(api_spec["SpecNo"])
            # print("api_spec", api_spec_set)
            sync_set = dao_spec_set.difference(api_spec_set)
            # print("erp数据库中要删除商品:" + str(productID) + " 的规格：", sync_set)
            for dao_specNo in sync_set:
                dao.offline_product_spec(productID, dao_specNo)

    def sync_request_api(self, item_name):
        try:
            print(item_name, " 开始：" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            # self.result.emit({"msg": "开始：" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            if item_name == "updateGoods":
                self.request_update_goods()
            elif item_name == "category":
                text = self.request_categoryList()
                while text is None or len(text) == 0:
                    time.sleep(3)
                    text = self.request_categoryList()
                self.result.emit({"msg": text})
                product_type_list = self.parse_categoryList(text)
                # 保存数据到数据库
                if self._sync_write_database == True:
                    dao = SyncDao.EtlDao()
                    dao.merge_product_type(product_type_list)
                else:
                    print("show product_type_list", product_type_list)
            elif item_name == "goods_off_api":
                page_goods_count = 1
                sync_page_no = 1
                while page_goods_count > 0 and self._isRunning:
                    text = self.request_goodsList(sync_page_no, "offline", self.recent_minutes, "")
                    while text is None or len(text) == 0:
                        time.sleep(1)
                        text = self.request_goodsList(sync_page_no, "offline", self.self.recent_minutes, "")
                    page_goods_list = self.parse_goodsList(text)
                    # 写入数据库
                    for product_info in page_goods_list:
                        p = {"ProductID": product_info["ProductID"], "GoodsCode": product_info["GoodsCode"],
                             "GoodsEName": product_info["GoodsEName"], "stock_nums": product_info["stock_nums"]}
                        self.api_offline_goods.append(p)
                    page_goods_count = len(page_goods_list)
                    sync_page_no += 1
            elif item_name == "export_goods_in_api":
                api_product_list = []
                page_goods_count = 1
                sync_page_no = 1
                while page_goods_count > 0 and self._isRunning:
                    text = self.request_goodsList(sync_page_no, "full", 0, "")
                    while text is None or len(text) == 0:
                        time.sleep(1)
                        text = self.request_goodsList(sync_page_no, "full", 0, "")
                    page_goods_list = self.parse_goodsList(text)
                    # 写入数据库
                    for product_info in page_goods_list:
                        p = {"ProductID": product_info["ProductID"], "GoodsCode": product_info["GoodsCode"],
                             "GoodsEName": product_info["GoodsEName"], "stock_nums": product_info["stock_nums"]}
                        api_product_list.append(p)
                        print(len(api_product_list), p)
                        self.result.emit({"msg": str(len(api_product_list)) + ":" + str(p)})
                    page_goods_count = len(page_goods_list)
                    sync_page_no += 1
                # 产品检查完成
                api_product_list_csv = pd.DataFrame(api_product_list, columns=['ProductID', 'GoodsCode', 'GoodsEName','stock_nums'])
                api_product_list_csv.to_csv('api_product_list.csv')
                self.result.emit({"alert": "网站上有 " + str(len(api_product_list)) + "个商品"})
            elif item_name == "full_goods":
                page_goods_count = 1
                sync_page_no = 1
                if self.page_no > 1:
                    sync_page_no = self.page_no
                while page_goods_count > 0 and self._isRunning:
                    msg = '页码：' + str(sync_page_no) + " 时间：" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(msg)
                    # 发送到主线程
                    self.result.emit({"msg": msg})
                    text = self.request_goodsList(sync_page_no, "full", 0, "")
                    while text is None or len(text) == 0:
                        msg = '页码：' + str(sync_page_no) + " 时间：" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(item_name, msg)
                        self.result.emit({"msg": msg})
                        time.sleep(1)
                        text = self.request_goodsList(sync_page_no, "full", 0, "")
                    page_goods_list = self.parse_goodsList(text)
                    # 写入数据库
                    for product_info in page_goods_list:
                        if self._sync_write_database == True:
                            self.merge_product_info(product_info)
                        else:
                            print("product_info", product_info)
                    page_goods_count = len(page_goods_list)
                    sync_page_no += 1
                # 产品同步完成
            elif item_name == "recent_goods":
                # modify product.py
                page_goods_count = 1
                sync_page_no = 1
                while page_goods_count > 0 and self._isRunning:
                    msg = '页码：' + str(sync_page_no) + " 时间：" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(msg)
                    # 发送到主线程
                    self.result.emit({"msg": msg})
                    text = self.request_goodsList(sync_page_no, "modify", self.recent_minutes, "")
                    while text is None or len(text) == 0:
                        msg = '页码：' + str(sync_page_no) + " 时间：" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(item_name, msg)
                        self.result.emit({"msg": msg})
                        time.sleep(1)
                        text = self.request_goodsList(sync_page_no, "modify", self.recent_minutes,  "")
                    page_goods_list = self.parse_goodsList(text)
                    # print(page_goods_list)
                    # 写入数据库
                    for product_info in page_goods_list:
                        if self._sync_write_database == True:
                            print("最近更新", product_info)
                            self.merge_product_info(product_info)
                        else:
                            print("最近更新", product_info)
                    page_goods_count = len(page_goods_list)
                    sync_page_no += 1
                # create product.py
                page_goods_count = 1
                sync_page_no = 1
                while page_goods_count > 0 and self._isRunning:
                    msg = '页码：' + str(sync_page_no) + " 时间：" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(msg)
                    # 发送到主线程
                    self.result.emit({"msg": msg})
                    text = self.request_goodsList(sync_page_no, "create", 1000,  "")
                    while text is None or len(text) == 0:
                        msg = '页码：' + str(sync_page_no) + " 时间：" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(item_name, msg)
                        self.result.emit({"msg": msg})
                        time.sleep(1)
                        text = self.request_goodsList(sync_page_no, "create", 1000, "")
                    page_goods_list = self.parse_goodsList(text)
                    # 写入数据库
                    for product_info in page_goods_list:
                        if self._sync_write_database == True:
                            print("最近新增", product_info)
                            self.merge_product_info(product_info)
                        else:
                            print("最近新增", product_info)
                    page_goods_count = len(page_goods_list)
                    sync_page_no += 1
                # 产品同步完成
            elif item_name == "select_goods":
                # print("self.select_goods_id", self.select_goods_id)
                page_goods_count = 1
                sync_page_no = 1
                while page_goods_count > 0 and self._isRunning:
                    msg = '页码：' + str(sync_page_no) + " 时间：" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(msg)
                    # 发送到主线程
                    self.result.emit({"msg": msg})
                    text = self.request_goodsList(sync_page_no, "select", 0, self.select_goods_id)
                    while text is None or len(text) == 0:
                        msg = '页码：' + str(sync_page_no) + " 时间：" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(item_name, msg)
                        self.result.emit({"msg": msg})
                        time.sleep(1)
                        text = self.request_goodsList(sync_page_no, "select", 0, self.select_goods_id)
                    page_goods_list = self.parse_goodsList(text)
                    # 写入数据库
                    for product_info in page_goods_list:
                        if self._sync_write_database == True:
                            print("指定产品", product_info)
                            self.merge_force_product_info(product_info, "select")
                        else:
                            print("指定产品", product_info)
                    page_goods_count = len(page_goods_list)
                    sync_page_no += 1
                # 产品同步完成
            print(item_name, " 结束：" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
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

