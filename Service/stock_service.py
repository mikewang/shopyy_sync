# -*- coding: utf-8 -*-
import hashlib
import os
import base64, datetime
from Model.user import UserInfo
from Model.stock_dao import StockDao


class StockService(UserInfo):

    def __init__(self):
        super(StockService, self).__init__()
        self._dao = StockDao()

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

    def getNowStr(self):
        run_time = datetime.datetime.now()
        run_time_str = run_time.strftime('%Y-%m-%d %H:%M:%S')
        return run_time_str

    def getDecodeToken(self, OpCode, timestamp, decode_password):
        # 加密算法，token，计算方法, 分成三步。得到的结果和 api中传入的token比较 是否相等。
        data = decode_password + str(timestamp) + OpCode
        decode_token = hashlib.md5(data.encode(encoding='UTF-8')).hexdigest() + str(timestamp)
        decode_token = hashlib.md5(decode_token.encode(encoding='UTF-8')).hexdigest()
        return decode_token

    def getUserChecked(self, OpCode, timestamp, token):

        loginUser = self._dao.select_user(OpCode)
        if loginUser is not None:
            # base64 password -> text
            decode_password = loginUser.decode_password()
            decode_token = self.getDecodeToken(OpCode, timestamp, decode_password)
            if decode_token == token:
                return loginUser
            else:
                print(self.getNowStr(), "Error, user token is wrong ", loginUser.desc())
                return None
        else:
            print(self.getNowStr(), "Error, user is not existed.")
            return None

    def login(self, OpCode, timestamp, token):
        print(self.getNowStr(), "login", OpCode)

        user = self.getUserChecked(OpCode, timestamp, token)
        if user is not None:
            return {"ID": user.ID, "OpCode": user.OpCode, "OpName": user.OpName,
                    "Position": user.Position, "PositionName": user.PositionName}
        else:
            print(self.getNowStr(), "Error, user login is failure.")
            return None

    def getDictItem(self, OpCode, timestamp, token, item_type):

        print(self.getNowStr(), "get  data dictionary type", OpCode, timestamp, token, item_type)
        item_list = None
        user = self.getUserChecked(OpCode, timestamp, token)
        if user is not None:
            item_list = self._dao.select_dict_item_list(item_type)
        else:
            print(self.getNowStr(), "Error, get dictionary type is failure.", item_type)
        return item_list

    def getStockProduct(self, OpCode, timestamp, token, pageNo, filter_stock, ptype):

        print(self.getNowStr(), ptype, "get stock product", OpCode, "PageNo=", pageNo, filter_stock)
        product_list = None
        user = self.getUserChecked(OpCode, timestamp, token)
        if user is not None:
            product_list = self._dao.select_stock_product_list(pageNo, filter_stock)
        else:
            print(self.getNowStr(), "Error, get stockproduct is failure.", OpCode, "PageNo=", pageNo)
        return product_list

    def getOrderProduct(self, OpCode, timestamp, token, pageNo, filter_stock, ptype):
        print(self.getNowStr(), "get order product ", OpCode, "PageNo=", pageNo, filter_stock)
        product_list = None
        user = self.getUserChecked(OpCode, timestamp, token)
        if user is not None:
            product_list = self._dao.select_order_product_list(pageNo, filter_stock, ptype)
        else:
            print(self.getNowStr(), "Error, get stockproduct order is failure.", OpCode, "PageNo=", pageNo)
        return product_list

    def getProductImage(self, OpCode, timestamp, token, imageGuid, year, month, module):
        print(self.getNowStr(), "get product big image ", OpCode)
        product_list = None
        user = self.getUserChecked(OpCode, timestamp, token)
        disk_path = self._dao.disk_path
        user = self._dao.select_user(OpCode)
        if user is not None:
            file_path = os.path.normpath(os.path.join(disk_path, year, month, module, imageGuid))
            return file_path
        else:
            print(self.getNowStr(), "Error, get product big image is failure.")
            return None

    def addStockProductEnquiryPrice(self, OpCode, timestamp, token, prod_dict_list):

        print(self.getNowStr(), "add product enquiry price  ", OpCode)
        user = self.getUserChecked(OpCode, timestamp, token)
        if user is not None:
            result = self._dao.add_stock_product_enquiry_price(prod_dict_list)
            return result
        else:
            print(self.getNowStr(), "Error, add product enquiry price is failure.", prod_dict_list)
            return None

    def postStockProductOrder(self, OpCode, timestamp, token, prod_dict_list, operate):
        print(self.getNowStr(), "product order ", operate, OpCode)
        user = self.getUserChecked(OpCode, timestamp, token)
        if user is not None:
            if operate == "cancel":
                result = self._dao.update_stock_product_order(prod_dict_list, operate)
            elif operate == "complete":
                result = self._dao.update_stock_product_order(prod_dict_list, operate)
            else:
                result = self.addStockProductOrder(OpCode, timestamp, token, prod_dict_list)
            return result
        else:
            print(self.getNowStr(), "Error, ", operate, " product order is failure.", prod_dict_list)
            return None

    def addStockProductOrder(self, OpCode, timestamp, token, prod_dict_list):

        print(self.getNowStr(), "add product order ", OpCode)
        user = self.getUserChecked(OpCode, timestamp, token)
        if user is not None:
            result = self._dao.add_stock_product_order(prod_dict_list)
            return result
        else:
            print(self.getNowStr(), "Error, add product order is failure.", prod_dict_list)
            return None

    def cancelStockProductOrder(self, OpCode, timestamp, token, prod_dict_list):

        print(self.getNowStr(), "cancel product order ", OpCode)
        user = self.getUserChecked(OpCode, timestamp, token)
        if user is not None:
            result = self._dao.update_stock_product_order(prod_dict_list, "cancel")
            return result
        else:
            print(self.getNowStr(), "Error, cancel product order is failure.", prod_dict_list)
            return None

    def completeStockProductOrder(self, OpCode, timestamp, token, prod_dict_list):

        print(self.getNowStr(), "complete product order ", OpCode)
        user = self.getUserChecked(OpCode, timestamp, token)
        if user is not None:
            result = self._dao.update_stock_product_order(prod_dict_list, "complete")
            return result
        else:
            print(self.getNowStr(), "Error, complete product order is failure.", prod_dict_list)
            return None

