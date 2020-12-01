# -*- coding: utf-8 -*-
import hashlib
import os
import base64
import datetime
import hashlib
from WOW.wow_model import UserInfo, UserProfile, RentalService
from WOW.wow_dao import WowDao


class WowService(object):

    def __init__(self):
        super(WowService, self).__init__()

    @staticmethod
    def testInfo(p1):
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return time_str

    def addUser(self, p_user_dict):
        p1 = p_user_dict
        userInfo = UserInfo()
        userInfo.UserName = p1["UserName"]
        userInfo.UserType = p1["UserType"]
        userInfo.Password = p1["Password"]
        time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dao = WowDao()
        add_user = dao.add_user(userInfo)
        print("add user service done ,  user is ", add_user)
        return add_user

    def getToken(self, p_username, p_timestamp):
        dao = WowDao()
        userinfo = dao.select_user(None, p_username)
        if userinfo is not None:
            decode_token = userinfo.UserName + userinfo.Password + str(p_timestamp)
            token = hashlib.md5(decode_token.encode(encoding='UTF-8')).hexdigest()
            userprofile = dao.select_user_profile(userinfo.UserID)
            return token, userinfo, userprofile
        else:
            return "", None

    def getUser(self, p_username, p_token, p_timestamp):
        token, userinfo, userprofile = self.getToken(p_username, p_timestamp)
        if token == p_token:
            return userinfo
        else:
            return None

    def getUserProfile(self, p_username, p_token, p_timestamp):
        token, userinfo, userprofile = self.getToken(p_username, p_timestamp)
        if token == p_token:
            return userprofile
        else:
            return None

    def mergeUserProfile(self, p_username, p_token, p_timestamp, args):
        token, userinfo, temp_userpfile = self.getToken(p_username, p_timestamp)
        if token == p_token:
            dao = WowDao()
            userpfile = UserProfile()
            if temp_userpfile is not None:
                # update
                userpfile = temp_userpfile
                userpfile.CustType = args["CustType"]
                userpfile.FirstName = args["FirstName"]
                userpfile.LastName = args["LastName"]
                userpfile.DriverLicenseNumber = args["DriverLicenseNumber"]
                userpfile.InsuranceCompanyName = args["InsuranceCompanyName"]
                userpfile.InsurancePolicyNumber = args["InsurancePolicyNumber"]
                userpfile.CorporateName = args["CorporateName"]
                userpfile.CorporateRegNo = args["CorporateRegNo"]
                userpfile.CorporateEmployeeID = args["CorporateEmployeeID"]
                userpfile.Street = args["Street"]
                userpfile.City = args["City"]
                userpfile.State = args["State"]
                userpfile.Country = args["Country"]
                userpfile.Zip = args["Zip"]
                userpfile.Email = args["Email"]
                userpfile.Tel = args["Tel"]
                userpfile.UserID = userinfo.UserID
                print("user profile update is ", userpfile.desc())
                userpfile = dao.update_user_profile(userpfile)
            else:
                # insert
                userpfile.CustType = args["CustType"]
                userpfile.FirstName = args["FirstName"]
                userpfile.LastName = args["LastName"]
                userpfile.DriverLicenseNumber = args["DriverLicenseNumber"]
                userpfile.InsuranceCompanyName = args["InsuranceCompanyName"]
                userpfile.InsurancePolicyNumber = args["InsurancePolicyNumber"]
                userpfile.CorporateName = args["CorporateName"]
                userpfile.CorporateRegNo = args["CorporateRegNo"]
                userpfile.CorporateEmployeeID = args["CorporateEmployeeID"]
                userpfile.Street = args["Street"]
                userpfile.City = args["City"]
                userpfile.State = args["State"]
                userpfile.Country = args["Country"]
                userpfile.Zip = args["Zip"]
                userpfile.Email = args["Email"]
                userpfile.Tel = args["Tel"]
                userpfile.UserID = userinfo.UserID
                print("user profile add is ", userpfile.desc())
                userpfile = dao.insert_user_profile(userpfile)
            return userpfile
        else:
            return None

    def getRentalService(self, p_username, p_token, p_timestamp, p_rs_id):
        token, userinfo, temp_userpfile = self.getToken(p_username, p_timestamp)
        if token == p_token:
            rs_list = []
            dao = WowDao()
            if temp_userpfile is not None:
                temp_cust_id = temp_userpfile.CustID
                rs_list = dao.select_rental_service(p_rs_id, temp_cust_id)
            else:
                rs_list = None
            return rs_list
        else:
            return None

    def getAdminRentalService(self, p_username, p_token, p_timestamp, p_rs_id, p_cust_id):
        token, userinfo, temp_userpfile = self.getToken(p_username, p_timestamp)
        if token == p_token:
            dao = WowDao()
            rs_list = dao.select_rental_service(p_rs_id, p_cust_id)
            return rs_list
        else:
            return None

    def mergeRentalService(self, p_username, p_token, p_timestamp, args):
        token, userinfo, temp_userpfile = self.getToken(p_username, p_timestamp)
        if token == p_token:
            dao = WowDao()
            if temp_userpfile is not None:
                rs_id = args["rs_id"]
                rs_list = dao.select_rental_service(rs_id, None)
                if len(rs_list) > 0:
                    rs = rs_list[0]
                    if rs.Cust_ID != temp_userpfile.CustID:
                        rs = None
                    else:
                        # update
                        rental = RentalService()
                        rental.rs_id = args["rs_id"]
                        rental.Pickup_Location = args["Pickup_Location"]
                        rental.Dropoff_Location = args["Dropoff_Location"]
                        rental.Pickup_Date = args["Pickup_Date"]
                        # other fields
                        rental.Cust_ID = rs.Cust_ID
                        rs = dao.update_rental_service(rental)
                else:
                    # insert
                    rental = RentalService()
                    rental.Pickup_Location = args["Pickup_Location"]
                    rental.Dropoff_Location = args["Dropoff_Location"]
                    rental.Pickup_Date = args["Pickup_Date"]
                    # other fields
                    rental.Cust_ID = temp_userpfile.CustID
                    rs = dao.insert_rental_service(rental)
            else:
                rs = None
            return rs
        else:
            return None

    def deleteRentalService(self, p_username, p_token, p_timestamp, args):
        token, userinfo, temp_userpfile = self.getToken(p_username, p_timestamp)
        if token == p_token:
            dao = WowDao()
            if temp_userpfile is not None:
                rs_id = args["rs_id"]
                rs_list = dao.select_rental_service(rs_id, None)
                if len(rs_list) > 0:
                    rs = rs_list[0]
                    if rs.Cust_ID != temp_userpfile.CustID:
                        rs = None
                    else:
                        # update
                        rental = RentalService()
                        rental.rs_id = args["rs_id"]

                        rs = dao.delete_rental_service(rental)
                else:
                    # insert
                    rental = RentalService()
                    rental.Pickup_Location = args["Pickup_Location"]
                    rental.Dropoff_Location = args["Dropoff_Location"]
                    rental.Pickup_Date = args["Pickup_Date"]
                    # other fields
                    rental.Cust_ID = temp_userpfile.CustID
                    rs = dao.insert_rental_service(rental)
            else:
                rs = None
            return rs
        else:
            return None
