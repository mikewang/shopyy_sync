# -*- coding: utf-8 -*-
import decimal


class Employee(object):

    def __init__(self):
        super(Employee, self).__init__()
        self.__setup_model()

    def __del__(self):
        pass

    def __setup_model(self):
        self.employeeno = 0
        self.name = ''
        self.sex = ''
        self.birthday = ''
        self.national = ''
        self.degree = ''
        self.telephone = ''
        self.address = ''
        self.salary = 0.00
        self.language = ''
        self.certificate = ''
        self.jobs = []

    def desc(self):
        model_dict = self.__dict__
        model_dict["salary"] = str(self.salary)
        print(self, model_dict)
        return model_dict


class Job(object):

    def __init__(self):
        super(Employee, self).__init__()
        self.__setup_model()

    def __del__(self):
        pass

    def __setup_model(self):
        self.workno = 0
        self.employeeno = 0
        self.startdate = ''
        self.enddate = ''
        self.work_desc = ''

    def desc(self):
        model_dict = self.__dict__
        print(self, model_dict)
        return model_dict
