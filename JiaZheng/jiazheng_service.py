# -*- coding: utf-8 -*-
import hashlib
import os
import base64
import datetime
import hashlib
from JiaZheng.jiazheng_model import Employee, Job
from JiaZheng.jiazheng_dao import JiaZhengDao


class JiaZhengService(object):

    def __init__(self):
        super(JiaZhengService, self).__init__()

    @staticmethod
    def testInfo(p1):
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return time_str

    def getEmployee(self, p_employeeno, p_name):
        dao = JiaZhengDao()
        employee_list = dao.select_employee(p_employeeno, p_name)
        return employee_list
