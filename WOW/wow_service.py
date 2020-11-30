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

    def getUser(self, p_username, p_token, p_timestamp):
        dao = WowDao()
        userinfo = dao.select_user(None, p_username)
        if userinfo is not None:
            decode_token = userinfo.UserName + userinfo.Password + str(p_timestamp)
            token = hashlib.md5(decode_token.encode(encoding='UTF-8')).hexdigest()
            print("userinfo name is ", p_token, userinfo.UserName, userinfo.Password, p_timestamp)
            print("userinfo name is ", token, userinfo.UserName, userinfo.Password, p_timestamp)
            if token == p_token:
               print("token checked ok , username is ", p_username)
            else:
                userinfo = None
        return userinfo

    def getUserProfile(self, p_username, p_token, p_timestamp):
        userpfile = UserProfile()
        dao = WowDao()
        userinfo = dao.select_user(None, p_username)
        if userinfo is not None:
            decode_token = userinfo.UserName + userinfo.Password + str(p_timestamp)
            token = hashlib.md5(decode_token.encode(encoding='UTF-8')).hexdigest()
            if token == p_token:
               userpfile.UserID = userinfo.UserID
               temp_userpfile = dao.select_user_profile(userinfo.UserID)
               if temp_userpfile is not None:
                   userpfile = temp_userpfile
            else:
               userpfile = None
        return userpfile

    def mergeUserProfile(self, p_username, p_token, p_timestamp, args):
        userpfile = UserProfile()
        dao = WowDao()
        userinfo = dao.select_user(None, p_username)
        if userinfo is not None:
            decode_token = userinfo.UserName + userinfo.Password + str(p_timestamp)
            token = hashlib.md5(decode_token.encode(encoding='UTF-8')).hexdigest()
            if token == p_token:
               userpfile.UserID = userinfo.UserID
               temp_userpfile = dao.select_user_profile(userinfo.UserID)
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
                   print("userpfile update is ", userpfile.desc())
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
                   print("userpfile add is ", userpfile.desc())
                   userpfile = dao.insert_user_profile(userpfile)
            else:
               userpfile = None
        return userpfile


    def getRentalService(self, p_username, p_token, p_timestamp, p_rs_id):
        rs_list = []
        dao = WowDao()
        userinfo = dao.select_user(None, p_username)
        if userinfo is not None:
            decode_token = userinfo.UserName + userinfo.Password + str(p_timestamp)
            token = hashlib.md5(decode_token.encode(encoding='UTF-8')).hexdigest()
            if token == p_token:
                temp_userpfile = dao.select_user_profile(userinfo.UserID)
                if temp_userpfile is None:
                    rs_list = None
                else:
                    temp_cust_id = temp_userpfile.CustID
                    rs_list = dao.select_rental_service(p_rs_id, temp_cust_id)
            else:
                rs_list = None
        return rs_list


    def getAdminRentalService(self, p_username, p_token, p_timestamp, p_rs_id, p_cust_id):
        rs_list = []
        dao = WowDao()
        userinfo = dao.select_user(None, p_username)
        if userinfo is not None:
            decode_token = userinfo.UserName + userinfo.Password + str(p_timestamp)
            token = hashlib.md5(decode_token.encode(encoding='UTF-8')).hexdigest()
            if token == p_token:
                rs_list = dao.select_rental_service(p_rs_id, p_cust_id)
            else:
                rs_list = None
        return rs_list