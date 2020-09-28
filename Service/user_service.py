# -*- coding: utf-8 -*-
import hashlib
import io
import base64
from Model.user import UserInfo
from Service.user_dao import UserDao


class UserService(UserInfo):

    def __init__(self):
        super(UserService, self).__init__()
        self._dao = UserDao()
        self._loginUser = None

    def __decodeToken(self, OpCode, timestamp, decode_password):
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
            decode_token = self.__decodeToken(OpCode, timestamp, decode_password)
            if decode_token != token:
                self._loginUser = None
                print("-"*10, OpCode, 'login failure', '-'*10)
        if self._loginUser is not None:
            return {"ID":  self._loginUser.ID, "OpCode": self._loginUser.OpCode, "OpName": self._loginUser.OpName,
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
            decode_token = self.__decodeToken(OpCode, timestamp, decode_password)
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
                    print("imageBase64", base64_image)
                    product_image["ThumbImage"] = None
        return product_image
