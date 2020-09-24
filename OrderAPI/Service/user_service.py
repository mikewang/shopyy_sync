# -*- coding: utf-8 -*-
import hashlib
from OrderAPI.Model.user import UserInfo
from OrderAPI.Service.user_dao import UserDao


class UserService(UserInfo):

    def __init__(self):
        super(UserService, self).__init__()
        self._dao = UserDao()

    def login(self, OpCode, timestamp, token):
        user = self._dao.select_user(OpCode)
        if user is not None:
            decode_password = user.decode_password()
            data = decode_password + str(timestamp) + OpCode
            decode_token = hashlib.md5(data.encode(encoding='UTF-8')).hexdigest() + str(timestamp)
            decode_token = hashlib.md5(decode_token.encode(encoding='UTF-8')).hexdigest()
            print(decode_token)
            if decode_token != token:
                user = None
                print("-"*10, OpCode , 'login failure', '-'*10)
        return user



