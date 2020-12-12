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

    def getCert(self):
        dao = JiaZhengDao()
        cert_list = dao.select_certificate()
        return cert_list

    def mergeWorker(self, args):
        employeeno = args["employeeno"]
        dao = JiaZhengDao()
        employee_list = dao.select_employee(employeeno, None)
        if len(employee_list) > 0:
            #update
            employee = Employee()
            employee.employeeno = args["employeeno"]
            employee.name = args["name"]
            employee.sex = args["sex"]
            employee.birthday = args["birthday"]
            employee.national = args["national"]
            employee.degree = args["degree"]
            employee.telephone = args["telephone"]
            employee.address = args["address"]
            employee.salary = args["salary"]
            employee.language = args["language"]
            employee.certificate = args["certificate"]
            print("update employee is ", employee.desc())
            employee = dao.update_employee(employee)
            return employee
        else:
            #insert
            employee = Employee()
            employee.employeeno = args["employeeno"]
            employee.name = args["name"]
            employee.sex = args["sex"]
            employee.birthday = args["birthday"]
            employee.national = args["national"]
            employee.degree = args["degree"]
            employee.telephone = args["telephone"]
            employee.address = args["address"]
            employee.salary = args["salary"]
            employee.language = args["language"]
            employee.certificate = args["certificate"]
            print("insert employee is ", employee.desc())
            employee = dao.insert_employee(employee)
            return employee

    def deleteWorker(self, args):
        employeeno = args["employeeno"]
        dao = JiaZhengDao()
        return dao.delete_employee(employeeno)
