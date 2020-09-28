# -*- coding: utf-8 -*-
import datetime
import base64

# 定义 用户 类


class UserInfo(object):

    def __init__(self):
        super(UserInfo, self).__init__()
        print("initial class", self)
        self.__setup_user()

    def __del__(self):
        pass

    def __setup_user(self):
        self.ID = 0
        self.OpCode = ''
        self.OpName = ''
        self.OpEName = ''
        self.Password = ''
        self.CreateDate = datetime.datetime.now()
        self.OrganizeID = 0
        self.Position = 0
        self.PositionName = ''

    def decode_password(self):
        base64_password = self.Password
        base64_bytes = base64_password.encode("utf8")
        password_bytes = base64.b64decode(base64_bytes)
        password = password_bytes.decode('utf8')
        return password

    def encode_password(self, password):
        password_bytes = password.encode('utf8')
        base64_bytes = base64.b64encode(password_bytes)
        base64_password = base64_bytes.decode("utf8")
        return base64_password

    def desc(self):
        user_dict = self.__dict__
        user_dict["CreateDate"] = self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        user_dict["realPassword"] = self.decode_password()
        print(user_dict)
        return user_dict



