# -*- coding: utf-8 -*-
import hashlib
import os
import base64
import datetime
from Model.user import UserInfo
from Model.user_dao import UserDao


class WOWService(UserInfo):

    def __init__(self):
        super(WOWService, self).__init__()

    @staticmethod
    def testInfo(p1):
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return time_str
