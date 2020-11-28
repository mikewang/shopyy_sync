# -*- coding: utf-8 -*-
import hashlib
import os
import base64
import datetime
from WOW.wow_model import UserInfo
from WOW.wow_dao import WowDao


class WowService(object):

    def __init__(self):
        super(WowService, self).__init__()


    @staticmethod
    def testInfo(p1):
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return time_str

    @staticmethod
    def registerUser(p_user_dict):
        p1 = {"UserName": "Test1", "UserType": "Customer", "Password": "abcd"}

        userInfo = UserInfo()
        userInfo.UserName = p1["UserName"]
        userInfo.UserType = p1["UserType"]
        userInfo.Password = p1["Password"]
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dao = WowDao()
        add_user = dao.add_user(userInfo)
        print("registerUser service done , register user i s", add_user)
        return time_str