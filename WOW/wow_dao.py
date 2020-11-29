# -*- coding: utf-8 -*-
import configparser
import traceback
import sys
import os
import pyodbc
import datetime
import base64
from WOW.wow_model import UserInfo, UserProfile
from Model.product import ProductInfo, ProductEnquiryPrice
import pymysql


class WowDao(object):

    def __init__(self):
        super(WowDao, self).__init__()
        try:
            conn = self.conn_mysql()
            cur = conn.cursor()
            cur.execute("select @@version")
            output = cur.fetchone()
            print(self, output)
            conn.close()
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # Get information about the exception that is currently being handled
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print('e.message:\t', exc_value)
            print("Note, object e and exc of Class %s is %s the same." %
                  (type(exc_value), ('not', '')[exc_value is e]))
            print('traceback.print_exc(): ', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            print('-' * 60)


    def conn_mysql(self):
        config = configparser.ConfigParser()
        config_file = os.path.normpath(os.path.join(os.curdir, "wow_config.ini"))
        config.read(config_file)
        mysql_host = config.get("mysql_db", "host")
        mysql_user = config.get("mysql_db", "user")
        mysql_password = config.get("mysql_db", "password")
        mysql_db = config.get("mysql_db", "db")
        mysql_port = int(config.get("mysql_db", "port"))
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_db,
                               port=mysql_port)
        return conn

    def select_user(self, p_userID, p_userName):
        try:
            userInfo = None
            conn = self.conn_mysql()
            cursor = conn.cursor()
            if p_userID is not None:
                sql = "SELECT USER_ID,USER_NAME, USER_TYPE, PASSWORD, DATE_FORMAT(CREATED,'%%Y-%%m-%%d %%H:%%i:%%s') as CREATED FROM User_Info where User_ID=%s"
                cursor.execute(sql, p_userID)
            elif p_userName is not None:
                sql = "SELECT USER_ID,USER_NAME, USER_TYPE, PASSWORD, DATE_FORMAT(CREATED,'%%Y-%%m-%%d %%H:%%i:%%s') as CREATED FROM User_Info where User_Name=%s"
                cursor.execute(sql, p_userName)
            row = cursor.fetchone()
            if row is not None:
                userInfo = UserInfo()
                userInfo.UserID = row[0]
                userInfo.UserName = row[1]
                userInfo.UserType = row[2]
                userInfo.Password = row[3]
                userInfo.Created = row[4]
                #userInfo.Created = datetime.datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')
            else:
                print("User:  Not Existed.")
            cursor.close()
            conn.close()
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # Get information about the exception that is currently being handled
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print('e.message:\t', exc_value)
            print("Note, object e and exc of Class %s is %s the same." %
                  (type(exc_value), ('not', '')[exc_value is e]))
            print('traceback.print_exc(): ', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            print('#' * 60)
        else:
            print("done", userInfo)
        finally:
            return userInfo

    def add_user(self, p_userInfo):
        try:
            userInfo = p_userInfo
            conn = self.conn_mysql()
            with conn.cursor() as cursor:
                sql = "insert into user_info(USER_NAME, USER_TYPE, PASSWORD, created) values(%s, %s, %s, now()) "
                values = (userInfo.UserName, userInfo.UserType, userInfo.Password)
                cursor.execute(sql, values)
                userInfo.UserID = cursor.lastrowid
                cursor.close()
            conn.commit()
            conn.close()
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # Get information about the exception that is currently being handled
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print('e.message:\t', exc_value)
            print("Note, object e and exc of Class %s is %s the same." %
                  (type(exc_value), ('not', '')[exc_value is e]))
            print('traceback.print_exc(): ', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            print('#' * 60)
            userInfo = None
        else:
            print("add user done, userinfo is ", userInfo.desc())
        finally:
            return userInfo

    def select_user_profile(self, p_userID):
        try:
            userProfile = None
            conn = self.conn_mysql()
            cursor = conn.cursor()
            sql = "SELECT CUST_ID,CUST_TYPE,STREET,CITY,STATE,COUNTRY,ZIP,EMAIL,TEL,USER_ID FROM customer_info where User_ID=%s"
            cursor.execute(sql, p_userID)
            row = cursor.fetchone()
            if row is not None:
                userProfile = UserProfile()
                userProfile.CustID = row[0]
                userProfile.CustType = row[1]
                userProfile.Street = row[2]
                userProfile.City = row[3]
                userProfile.State = row[4]
                userProfile.Country = row[5]
                userProfile.Zip = row[6]
                userProfile.Email = row[7]
                userProfile.Tel = row[8]
                userProfile.UserID = row[9]
            else:
                print("User Profile:  Not Existed.")
            cursor.close()
            if userProfile is not None:
                if userProfile.CustType == 'I':
                    cursor = conn.cursor()
                    sql = "SELECT CUST_ID,FIRST_NAME,LAST_NAME,DRIVER_LICENSE_NUMBER,INSURANCE_COMPANY_NAME,INSURANCE_POLICY_NUMBER FROM customer_individual where CUST_ID=%s"
                    cursor.execute(sql, userProfile.CustID)
                    row = cursor.fetchone()
                    if row is not None:
                        userProfile.FirstName = row[1]
                        userProfile.LastName = row[2]
                        userProfile.DriverLicenseNumber = row[3]
                        userProfile.InsuranceCompanyName = row[4]
                        userProfile.InsurancePolicyNumber = row[5]
                    cursor.close()
                elif userProfile.CustType == 'C':
                    cursor = conn.cursor()
                    sql = "SELECT CUST_ID,NAME,REG_NO,EMPLOYEE_ID FROM customer_corporate where CUST_ID=%s"
                    cursor.execute(sql, userProfile.CustID)
                    row = cursor.fetchone()
                    if row is not None:
                        userProfile.CorporateName = row[1]
                        userProfile.CorporateRegNo = row[2]
                        userProfile.CorporateEmployeeID = row[3]
                    cursor.close()
            conn.close()
            return userProfile
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # Get information about the exception that is currently being handled
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print('e.message:\t', exc_value)
            print("Note, object e and exc of Class %s is %s the same." %
                  (type(exc_value), ('not', '')[exc_value is e]))
            print('traceback.print_exc(): ', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            print('#' * 60)
            return None

    def insert_user_profile(self, p_userProfile):
        try:
            customer = p_userProfile
            conn = self.conn_mysql()
            with conn.cursor() as cursor:
                sql = "insert into customer_info(CUST_TYPE,STREET,CITY,STATE,COUNTRY,ZIP,EMAIL,TEL,USER_ID) " \
                      "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                values = (customer.CustType, customer.Street, customer.City,customer.State, customer.Country, customer.Zip,customer.Email, customer.Tel, customer.UserID)
                cursor.execute(sql, values)
                customer.CustID = cursor.lastrowid
                cursor.close()
            if customer.CustType == 'I':
                with conn.cursor() as cursor:
                    sql = "insert into customer_individual(CUST_ID,FIRST_NAME,LAST_NAME,DRIVER_LICENSE_NUMBER,INSURANCE_COMPANY_NAME,INSURANCE_POLICY_NUMBER) " \
                          "values(%s,%s,%s,%s,%s,%s)"
                    values = [customer.CustID, customer.FirstName, customer.LastName,customer.DriverLicenseNumber, customer.InsuranceCompanyName, customer.InsurancePolicyNumber]
                    cursor.execute(sql, values)
                    cursor.close()
            if customer.CustType == 'C':
                with conn.cursor() as cursor:
                    sql = "insert into customer_individual(CUST_ID,NAME,REG_NO,EMPLOYEE_ID) " \
                          "values(%s,%s,%s,%s)"
                    values = [customer.CustID, customer.CorporateName, customer.CorporateRegNo,customer.CorporateEmployeeID]
                    cursor.execute(sql, values)
                    cursor.close()
            conn.commit()
            conn.close()
            return customer
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # Get information about the exception that is currently being handled
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print('e.message:\t', exc_value)
            print("Note, object e and exc of Class %s is %s the same." %
                  (type(exc_value), ('not', '')[exc_value is e]))
            print('traceback.print_exc(): ', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            print('#' * 60)
            return None

    def update_user_profile(self, p_userProfile):
        try:
            customer = p_userProfile
            conn = self.conn_mysql()
            print("update_user_profile", customer)
            with conn.cursor() as cursor:
                sql = "update customer_info set CUST_TYPE = %s, STREET = %s,City = %s, State = %s, Country=%s, Zip=%s,Email=%s, Tel=%s,USER_ID=%s where cust_id=%s"
                values = (customer.CustType, customer.Street, customer.City, customer.State, customer.Country, customer.Zip, customer.Email, customer.Tel, customer.UserID, customer.CustID)
                cursor.execute(sql, values)
                cursor.close()
            if customer.CustType == 'I':
                with conn.cursor() as cursor:
                    sql = "update customer_individual set FIRST_NAME = %s, LAST_NAME = %s, DRIVER_LICENSE_NUMBER = %s, INSURANCE_COMPANY_NAME = %s, INSURANCE_POLICY_NUMBER = %s where CUST_ID=%s"
                    values = (customer.FirstName, customer.LastName, customer.DriverLicenseNumber,
                              customer.InsuranceCompanyName, customer.InsurancePolicyNumber, customer.CustID)
                    cursor.execute(sql, values)
                    cursor.close()
            if customer.CustType == 'C':
                with conn.cursor() as cursor:
                    sql = "update customer_individual set NAME=%s, REG_NO=%s, EMPLOYEE_ID=%s where CUST_ID =%s"
                    values = ( customer.CorporateName, customer.CorporateRegNo,
                              customer.CorporateEmployeeID, customer.CustID)
                    cursor.execute(sql, values)
                    cursor.close()
            conn.commit()
            conn.close()
            return customer
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # Get information about the exception that is currently being handled
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print('e.message:\t', exc_value)
            print("Note, object e and exc of Class %s is %s the same." %
                  (type(exc_value), ('not', '')[exc_value is e]))
            print('traceback.print_exc(): ', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            print('#' * 60)
            return None