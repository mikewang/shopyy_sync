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


class RentalService(object):
    def __init__(self):
        super(RentalService, self).__init__()
        self.__setup_model()

    def __del__(self):
        pass

    def __setup_model(self):
        self.rs_id = 0
        self.Pickup_Location = 'I'
        self.Dropoff_Location = ''
        self.Pickup_Date = ''
        self.Dropoff_Date = ''
        self.Start_Odometer = 0
        self.End_Odometer = 0
        self.Daily_Odometer_Limit = 0
        self.rental_rate = 0.0
        self.rental_fee = 0.0
        self.rental_amount = 0.0
        self.really_amount = 0.0
        self.Vehicle_ID = 0
        self.Cust_ID = 0

        self.wow_userid = 0


    def desc(self):
        model_dict = self.__dict__
        model_dict["rental_rate"] = str(self.rental_rate)
        model_dict["rental_fee"] = str(self.rental_fee)
        model_dict["rental_amount"] = str(self.rental_amount)
        model_dict["really_amount"] = str(self.really_amount)

        # product_dict["CreateDate"] = self.CreateDate.strftime('%Y-%m-%d %H:%M:%S')
        print(self, model_dict)
        return model_dict
