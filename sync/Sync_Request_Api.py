# -*- coding: utf-8 -*-
import traceback
from PyQt5.QtCore import QObject, pyqtSignal
import datetime
import sys
import requests
import json
import hashlib
from sync import global_v as gl


class SyncRequestApi(QObject):
    signal = pyqtSignal(dict)

    def __init__(self):
        super(SyncRequestApi, self).__init__()

    def __del__(self):
       print("auto del", self)

    def request_category_list(self, domain_name, token):
        try:
            json_dict = {}
            api = "api-erp-categoryList.html"
            url = domain_name + api
            time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(url, time_str)
            data = {'token': token}
            response = requests.session().post(url, data=data)
            response_text = ""
            if response.status_code == 200:
                response_text = response.text
                json_dict = json.loads(response_text)
                # self.signal.emit({"message": str(json_dict)})
            else:
                print("response.status_code=" + str(response.status_code))
            print(url, "访问完成", time_str)
            return json_dict
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

    def parse_category_list(self, domain_name, json_dict):
        code = json_dict["code"]
        data_array = json_dict["data"]
        product_type_list = []
        # Insert into Product_Type(ProductTypeID,ParentID,TypeName,SortID) values()
        if domain_name == gl.pf_domain or domain_name == gl.ls_domain:
            product_type = {'ProductTypeID': 10000, 'ParentID': -1, 'TypeName': "批发/零售", 'SortID': 0}
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
        elif domain_name == gl.ls_domain:
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

    def request_goods_list_full(self, domain_name, token, page_no):
        try:
            json_dict = {}
            api = "api-commonErp-goodsList.html"
            url = domain_name + api
            time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = {"page_size": 200, "page_no": page_no, "status": 1}
            print(url, str(data), time_str)
            data["token"] = token
            response = requests.session().post(url, data=data)
            response_text = ""
            if response.status_code == 200:
                response_text = response.text
                json_dict = json.loads(response_text)
            else:
                print("response.status_code=" + str(response.status_code))
            time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(url, "访问完成", time_str)
            return json_dict
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

    def request_goods_list_recent(self, domain_name, token, recent_time_str, recent_type):
        try:
            json_dict = {}
            api = "api-commonErp-goodsList.html"
            url = domain_name + api
            time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if recent_type == "modify":
                data = {"page_size": 100, "page_no": 1, "start_modify_time": recent_time_str, "status": 1}
            else:
                data = {"page_size": 100, "page_no": 1, "start_time": recent_time_str, "status": 1}
            print(url, str(data), time_str)
            data["token"] = token
            response = requests.session().post(url, data=data)
            response_text = ""
            if response.status_code == 200:
                response_text = response.text
                json_dict = json.loads(response_text)
            else:
                print("response.status_code=" + str(response.status_code))
            time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(url, "访问完成", time_str)
            return json_dict
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

    def request_goods_list_selected(self, domain_name, token, goodscode):
        try:
            json_dict = {}
            api = "api-commonErp-goodsList.html"
            url = domain_name + api
            time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = {"page_size": 1, "page_no": 1, "codeno": goodscode}
            print(url, str(data), time_str)
            data["token"] = token
            response = requests.session().post(url, data=data)
            response_text = ""
            if response.status_code == 200:
                response_text = response.text
                json_dict = json.loads(response_text)
            else:
                print("response.status_code=" + str(response.status_code))
            time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(url, "访问完成", time_str)
            return json_dict
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

    def request_goods_list_recent_offline(self, domain_name, token, recent_time_str, recent_type):
        try:
            json_dict = {}
            api = "api-commonErp-goodsList.html"
            url = domain_name + api
            time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if recent_type == "modify":
                data = {"page_size": 100, "page_no": 1, "start_modify_time": recent_time_str, "status": 0}
            else:
                data = {"page_size": 100, "page_no": 1, "start_time": recent_time_str, "status": 0}
            print(url, str(data), time_str)
            data["token"] = token
            response = requests.session().post(url, data=data)
            response_text = ""
            if response.status_code == 200:
                response_text = response.text
                json_dict = json.loads(response_text)
            else:
                print("response.status_code=" + str(response.status_code))
            time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(url, "访问完成", time_str)
            return json_dict
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

    def parse_goods_list(self, domain_name, json_dict):
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
                        product_spec["GoodsCode"] = product_info["body_product_spec"]["GoodsCode"]
                        product_spec["MinOrder"] = int(product_info["body_product_spec"]["moq"])
                        product_spec["mxoq"] = int(product_info["body_product_spec"]["mxoq"])
                        # set RecGuid
                        year = product_spec["SysNoTime"].split('-')[0]
                        month = product_spec["SysNoTime"].split('-')[1]
                        day = product_spec["SysNoTime"].split('-')[2].split(" ")[0]
                        md = hashlib.md5()
                        md.update((str(product_spec["GoodsCode"]) + str(product_spec["SpecNo"])).encode('utf-8'))
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
            # logging.info(product_info)
            product_info_list.append(product_info)
            # print(product_info)
            # 继续遍历下一个产品数据，直到数组结束
        print("-"*200)
        return product_info_list

    def parse_goods_info(self, item):
        # print("parse_goods_info", item)
        goods_id = item["id"]
        # print(goods_id)
        if "base_name" in item:
            base_name = item["base_name"]
        else:
            base_name = ""
        # 商品编号,真正的主键
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
        ProductActive = "0"
        if "status" in item:
            status = item["status"]
            if status == "0":
                ProductActive = "1"
        # print(goods_id, category_id, goods_codeno, base_name, goods_create_time_str, goods_modify_time_str, brand_id,
        # brand_name, goods_type_id, category_na
        #                     SysNo = int(time.mktime(product_type["SysNoTime"]))ght, volume, spec_mode, moq, mxoq)
        body_product_spec = {"GoodsCode": goods_codeno, "brand_id": brand_id, "brand_name": brand_name,
                             "goods_type_id": goods_type_id, "category_name": category_name,
                             "price": price, "weight": weight, "volume": volume, "spec_mode": spec_mode, "moq": moq,
                             "mxoq": mxoq}
        product_info = {"ProductID": int(goods_id), "TypeID": int(category_id), "GoodsCode": goods_codeno,
                        "GoodsEName": base_name, "stock_nums": stock_nums, "ProductActive": ProductActive,
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

    def parse_goods_simple_list(self, domain_name, json_dict):
        code = json_dict["code"]
        count = json_dict["count"]
        product_data_array = json_dict["data"]
        product_info_list = []
        for item in product_data_array:
            # 遍历产品数据 开始
            product_info = self.parse_goods_info(item)
            # logging.info(product_info)
            product_info_list.append(product_info)
            # print(product_info)
            # 继续遍历下一个产品数据，直到数组结束
        return product_info_list