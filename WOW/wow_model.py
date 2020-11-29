# -*- coding: utf-8 -*-
import json
import decimal


class UserInfo(object):
# ALTER TABLE user_info ADD CONSTRAINT user_info_user_name_un UNIQUE ( user_name );

    def __init__(self):
        super(UserInfo, self).__init__()
        print("initial class", self)
        self.__setup_model()

    def __del__(self):
        pass

    def __setup_model(self):
        self.UserID = 0
        self.UserName = ''
        self.UserType = ''
        self.Password = ''
        self.Created = ''

    def desc(self):
        model_dict = self.__dict__
        #product_dict["shouldPrice"] = str(self.shouldPrice)
        # product_dict["CreateDate"] = self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        print(self, model_dict)
        return model_dict


class UserProfile(object):
    def __init__(self):
        super(UserProfile, self).__init__()
        self.__setup_model()

    def __del__(self):
        pass

    def __setup_model(self):
        self.CustID = 0
        self.CustType = 'I'
        self.FirstName = ''
        self.LastName = ''
        self.DriverLicenseNumber = ''
        self.InsuranceCompanyName = ''
        self.InsurancePolicyNumber = ''
        self.CorporateName = ''
        self.CorporateRegNo = ''
        self.CorporateEmployeeID = ''
        self.Street = ''
        self.City = ''
        self.State = ''
        self.Country = ''
        self.Zip = ''
        self.Email = ''
        self.Tel = ''
        self.UserID = 0

    def desc(self):
        model_dict = self.__dict__
        #product_dict["shouldPrice"] = str(self.shouldPrice)
        # product_dict["CreateDate"] = self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        print(self, model_dict)
        return model_dict

