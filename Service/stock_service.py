# -*- coding: utf-8 -*-
import hashlib
import os
import base64, datetime
from Model.user import UserInfo
from Model.stock_dao import StockDao
from Model import constant_v as cv


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
            decode_token = self.get_decode_token(OpCode, timestamp, decode_password)
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

    def get_now_str(self):
        run_time = datetime.datetime.now()
        run_time_str = run_time.strftime('%Y-%m-%d %H:%M:%S')
        return run_time_str

    def get_decode_token(self, OpCode, timestamp, decode_password):
        # 加密算法，token，计算方法, 分成三步。得到的结果和 api中传入的token比较 是否相等。
        data = decode_password + str(timestamp) + OpCode
        decode_token = hashlib.md5(data.encode(encoding='UTF-8')).hexdigest() + str(timestamp)
        decode_token = hashlib.md5(decode_token.encode(encoding='UTF-8')).hexdigest()
        return decode_token

    def get_checked_user(self, OpCode, timestamp, token):

        loginUser = self._dao.select_user(OpCode)
        if loginUser is not None:
            # base64 password -> text
            decode_password = loginUser.decode_password()
            decode_token = self.get_decode_token(OpCode, timestamp, decode_password)
            if decode_token == token:
                return loginUser
            else:
                print(self.get_now_str(), "Error, user token is wrong ", loginUser.desc())
                return None
        else:
            print(self.get_now_str(), "Error, user is not existed.")
            return None

    def login(self, OpCode, timestamp, token):
        print(self.get_now_str(), "login by " + OpCode, "-"*30)

        user = self.get_checked_user(OpCode, timestamp, token)
        if user is not None:
            return {"ID": user.ID, "OpCode": user.OpCode, "OpName": user.OpName,
                    "Position": user.Position, "PositionName": user.PositionName}
        else:
            print(self.get_now_str(), "Error, user login is failure.")
            return None

    def get_dict_item(self, OpCode, timestamp, token, item_type):

        print(self.get_now_str(),timestamp, token, item_type, "get data dictionary type by " + OpCode, "-"*30)
        item_list = None
        user = self.get_checked_user(OpCode, timestamp, token)
        if user is not None:
            item_list = self._dao.select_dict_item_list(item_type)
        else:
            print(self.get_now_str(), "Error, get dictionary type is failure.", item_type)
        return item_list

    def get_stock_product(self, OpCode, timestamp, token, pageNo, filter_stock, ptype):
        # 获取商品 询价或采购
        print(self.get_now_str(), ptype, "PageNo=", pageNo, filter_stock, "get stock product by " + OpCode, "-"*30)
        product_list = None
        product_count = 0
        user = self.get_checked_user(OpCode, timestamp, token)
        if user is not None:
            product_list, product_count = self._dao.select_stock_product_list(pageNo, filter_stock)
        else:
            print(self.get_now_str(), "Error, get stockproduct is failure.", OpCode, "PageNo=", pageNo)
        return product_list, product_count

    def get_order_product(self, OpCode, timestamp, token, pageNo, filter_stock, ptype):
        print(self.get_now_str(), "PageNo=", pageNo, filter_stock, "get order product by " + OpCode, "-"*30)
        product_list = None
        product_count = 0
        user = self.get_checked_user(OpCode, timestamp, token)
        if user is not None:
            product_list, product_count = self._dao.select_order_product_list(pageNo, filter_stock, ptype)
        else:
            print(self.get_now_str(), "Error, get stockproduct order is failure.", OpCode, "PageNo=", pageNo)
        return product_list, product_count

    def get_product_image(self, OpCode, timestamp, token, imageGuid, year, month, module):
        print(self.get_now_str(), "get product big image by " + OpCode, "-"*30)
        product_list = None
        user = self.get_checked_user(OpCode, timestamp, token)
        disk_path = self._dao.disk_path
        user = self._dao.select_user(OpCode)
        if user is not None:
            file_path = os.path.normpath(os.path.join(disk_path, year, month, module, imageGuid))
            return file_path
        else:
            print(self.get_now_str(), "Error, get product big image is failure.")
            return None

    def add_stock_product_enquiry_price(self, OpCode, timestamp, token, prod_dict_list):

        print(self.get_now_str(), "add product enquiry price  by " + OpCode, "-"*30)
        user = self.get_checked_user(OpCode, timestamp, token)
        if user is not None:
            result = self._dao.add_stock_product_enquiry_price(prod_dict_list)
            return result
        else:
            print(self.get_now_str(), "Error, add product enquiry price is failure.", prod_dict_list)
            return None

    def post_order_product(self, OpCode, timestamp, token, prod_dict_list, operate):
        print(self.get_now_str(),  operate, "product order by " + OpCode, "-"*30)
        user = self.get_checked_user(OpCode, timestamp, token)
        if user is not None:
            if operate is None or operate == cv.order_goods:
                result = self.add_order_product(OpCode, timestamp, token, prod_dict_list)
                print("post_order_product result is ", result)
            elif operate == cv.cancel_order or operate == cv.complete_order or operate == cv.return_goods \
                    or operate == cv.undo_return or operate == cv.settlement_goods:
                result = self._dao.update_stock_product_order(prod_dict_list, operate)
            elif operate == cv.account_goods or operate == cv.undo_account:
                result = self._dao.merge_account_product(prod_dict_list, operate)
            else:
                print("--" * 50)
                print(operate, " maybe wrong.")
                print("--" * 50)

            return result
        else:

            print(self.get_now_str(), "Error, ", operate, " product order is failure.", prod_dict_list)
            return None

    def add_order_product(self, OpCode, timestamp, token, prod_dict_list):

        print(self.get_now_str(), "add product order by " + OpCode, "-"*30)
        user = self.get_checked_user(OpCode, timestamp, token)
        if user is not None:
            result = self._dao.add_stock_product_order(prod_dict_list)
            return result
        else:
            print(self.get_now_str(), "Error, add product order is failure.", prod_dict_list)
            return None

    def cancel_order_product(self, OpCode, timestamp, token, prod_dict_list):

        print(self.get_now_str(), "cancel product order by " + OpCode, "-"*30)
        user = self.get_checked_user(OpCode, timestamp, token)
        if user is not None:
            result = self._dao.update_stock_product_order(prod_dict_list, "cancel")
            return result
        else:
            print(self.get_now_str(), "Error, cancel product order is failure.", prod_dict_list)
            return None

    def complete_order_product(self, OpCode, timestamp, token, prod_dict_list):

        print(self.get_now_str(), "complete product order by " + OpCode, "-"*30)
        user = self.get_checked_user(OpCode, timestamp, token)
        if user is not None:
            result = self._dao.update_stock_product_order(prod_dict_list, "complete")
            return result
        else:
            print(self.get_now_str(), "Error, complete product order is failure.", prod_dict_list)
            return None

    def update_product_orderprice(self, OpCode, timestamp, token, prod_dict_list, operate):
        print(self.get_now_str(),  operate, "product order by " + OpCode, "-"*30)
        user = self.get_checked_user(OpCode, timestamp, token)
        if user is not None:
            result = self._dao.update_product_orderprice(prod_dict_list, operate)
            return result
        else:
            print(self.get_now_str(), "Error, ", operate, " product order is failure.", prod_dict_list)
            return None

    def get_account_product(self, OpCode, timestamp, token, pageNo, query_params, ptype):
        print(self.get_now_str(), "PageNo=", pageNo, query_params, "get account product by " + OpCode, "-"*30)
        product_list = None
        product_count = 0
        user = self.get_checked_user(OpCode, timestamp, token)
        if user is not None:
            account_product_list, product_count, product_list = self._dao.select_account_product(pageNo, query_params, ptype)
        else:
            print(self.get_now_str(), "Error, get account product is failure.", OpCode, "PageNo=", pageNo)
        return account_product_list, product_count, product_list

    def get_account_batchno(self, OpCode, timestamp, token, pageNo, query_params, ptype):
        print(self.get_now_str(), "PageNo=", pageNo, query_params, "get account product batchno by " + OpCode, "-"*30)
        product_list = None
        product_count = 0
        user = self.get_checked_user(OpCode, timestamp, token)
        if user is not None:
            batchno_list, batchno_count = self._dao.select_account_batchno(pageNo, query_params, ptype)
        else:
            print(self.get_now_str(), "Error, get account product batchno is failure.", OpCode, "PageNo=", pageNo)
        return batchno_list, batchno_count

    def get_orderprice_product(self, OpCode, timestamp, token, pageNo, query_params, ptypes):
        print(self.get_now_str(), "PageNo=", pageNo, query_params, "get orderprice product by " + OpCode, "-"*30)
        product_count = 0
        user = self.get_checked_user(OpCode, timestamp, token)
        if user is not None:
            orderprice_product_list, product_count = self._dao.select_product_orderprice_list(pageNo, query_params, ptypes)
        else:
            print(self.get_now_str(), "Error, select_product_orderprice_list is failure.", OpCode, "PageNo=", pageNo)
        return orderprice_product_list, product_count