# -*- coding: utf-8 -*-
import hashlib
import os
import base64
from Model.user import UserInfo
from Model.stock_dao import StockDao


class StockService(UserInfo):

    def __init__(self):
        super(StockService, self).__init__()
        self._dao = StockDao()
        self._loginUser = None

    def getDecodeToken(self, OpCode, timestamp, decode_password):
        # 加密算法，token，计算方法
        data = decode_password + str(timestamp) + OpCode
        decode_token = hashlib.md5(data.encode(encoding='UTF-8')).hexdigest() + str(timestamp)
        decode_token = hashlib.md5(decode_token.encode(encoding='UTF-8')).hexdigest()
        return decode_token

    def login(self, OpCode, timestamp, token):
        print("login", OpCode, timestamp, token)
        self._loginUser = self._dao.select_user(OpCode)
        if self._loginUser is not None:
            # 加密算法，token，计算方法
            decode_password = self._loginUser.decode_password()
            decode_token = self.getDecodeToken(OpCode, timestamp, decode_password)
            if decode_token != token:
                self._loginUser = None
                print("-" * 10, OpCode, 'login failure', '-' * 10)
        if self._loginUser is not None:
            return {"ID": self._loginUser.ID, "OpCode": self._loginUser.OpCode, "OpName": self._loginUser.OpName,
                    "Position": self._loginUser.Position, "PositionName": self._loginUser.PositionName}
        else:
            return None

    def testImage(self, OpCode, timestamp, token, GoodsCode):
        print("get image", OpCode, timestamp, token, GoodsCode)
        product_image = None
        user = self._dao.select_user(OpCode)
        if user is not None:
            # 加密算法，token，计算方法
            decode_password = user.decode_password()
            decode_token = self.getDecodeToken(OpCode, timestamp, decode_password)
            if decode_token == token:
                product_image = self._dao.select_product_image(GoodsCode)
                # print("product_image", product_image)
                if product_image is not None:
                    ThumbImage = product_image["ThumbImage"]
                    base64_bytes = base64.b64encode(ThumbImage)
                    base64_image = base64_bytes.decode("utf8")
                    # bytes = io.BytesIO(ThumbImage)
                    # wrapper = io.TextIOWrapper(ThumbImage, encoding="utf-8")
                    product_image["imageBase64"] = base64_image
                    # print("imageBase64", base64_image)
                    product_image["ThumbImage"] = None
                else:
                    print("Error token:", "get image", GoodsCode)
        return product_image

    def getDictItem(self, OpCode, timestamp, token, item_type):
        print("get data dictionary of type", OpCode, timestamp, token, item_type)
        item_list = None
        user = self._dao.select_user(OpCode)
        if user is not None:
            # 加密算法，token，计算方法
            decode_password = user.decode_password()
            decode_token = self.getDecodeToken(OpCode, timestamp, decode_password)
            if decode_token == token:
                item_list = self._dao.select_dict_item_list(item_type)
            else:
                print("Error token:", "get data dictionary of type", item_type)
        return item_list

    def getStockProduct(self, OpCode, timestamp, token, pageNo, filter_stock):
        print("get stock product of PageNo", OpCode, timestamp, token, pageNo)
        product_list = None
        user = self._dao.select_user(OpCode)
        if user is not None:
            # 加密算法，token，计算方法
            decode_password = user.decode_password()
            decode_token = self.getDecodeToken(OpCode, timestamp, decode_password)
            if decode_token == token:
                product_list = self._dao.select_stock_product_list(pageNo, filter_stock)
            else:
                print("Error token:", "get stock product of pageNo", pageNo)
        return product_list

    def getStockProductOrder(self, OpCode, timestamp, token, pageNo, filter_stock):
        print("get stock product order of PageNo", OpCode, timestamp, token, pageNo)
        product_list = None
        user = self._dao.select_user(OpCode)
        if user is not None:
            # 加密算法，token，计算方法
            decode_password = user.decode_password()
            decode_token = self.getDecodeToken(OpCode, timestamp, decode_password)
            if decode_token == token:
                product_list = self._dao.select_stock_product_order_list(pageNo, filter_stock)
            else:
                print("Error token:", "get stock product order of pageNo", pageNo)
        return product_list

    def getProductImage(self, OpCode, timestamp, token, imageGuid, year, month, module):
        print("get stock product.py big image", OpCode, timestamp, token, imageGuid)
        file_path = None
        user = self._dao.select_user(OpCode)
        disk_path = self._dao.disk_path
        if user is not None:
            # 加密算法，token，计算方法
            decode_password = user.decode_password()
            decode_token = self.getDecodeToken(OpCode, timestamp, decode_password)
            if decode_token == token:
                file_path = os.path.normpath(os.path.join(disk_path, year, month, module, imageGuid))
        return file_path

    def addStockProductEnquiryPrice(self, OpCode, timestamp, token, prod_dict_list):
        result = None
        user = self._dao.select_user(OpCode)
        if user is not None:
            # 加密算法，token，计算方法
            decode_password = user.decode_password()
            decode_token = self.getDecodeToken(OpCode, timestamp, decode_password)
            if decode_token == token:
                result = self._dao.add_stock_product_enquiry_price(prod_dict_list)
            else:
                print("Error token:", "get stock product of enquiry price", prod_dict_list)
        return result

    def addStockProductOrder(self, OpCode, timestamp, token, prod_dict_list):
        result = None
        user = self._dao.select_user(OpCode)
        if user is not None:
            # 加密算法，token，计算方法
            decode_password = user.decode_password()
            decode_token = self.getDecodeToken(OpCode, timestamp, decode_password)
            if decode_token == token:
                result = self._dao.add_stock_product_order(prod_dict_list)
            else:
                print("Error token:", "get stock product of order", prod_dict_list)
        return result

