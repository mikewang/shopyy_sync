# -*- coding: utf-8 -*-
import configparser
import traceback
import sys
import os
import datetime
import base64
from JiaZheng.jiazheng_model import Employee, Job
import pymysql


class JiaZhengDao(object):

    def __init__(self):
        super(JiaZhengDao, self).__init__()
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
        config_file = os.path.normpath(os.path.join(os.curdir, "config.ini"))
        print("config file is ", config_file)
        config.read(config_file)
        mysql_host = config.get("mysql_db", "host")
        mysql_user = config.get("mysql_db", "user")
        mysql_password = config.get("mysql_db", "password")
        mysql_db = config.get("mysql_db", "db")
        mysql_port = int(config.get("mysql_db", "port"))
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_db,
                               port=mysql_port)
        return conn

    def select_employee(self, p_employeeno, p_name):
        try:
            employee = None
            conn = self.conn_mysql()
            cursor = conn.cursor()
            if p_employeeno is not None:
                sql = "SELECT USER_ID,USER_NAME, USER_TYPE, PASSWORD, DATE_FORMAT(CREATED,'%%Y-%%m-%%d %%H:%%i:%%s') as CREATED FROM User_Info where User_ID=%s"
                cursor.execute(sql, p_userID)
            elif p_name is not None:
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

    def add_employee(self, p_employee):
        try:
            userInfo = p_userInfo
            conn = self.conn_mysql()
            cursor = conn.cursor()
            sql = "insert into user_info(USER_NAME, USER_TYPE, PASSWORD, created) values(%s, %s, %s, now()) "
            values = (userInfo.UserName, userInfo.UserType, userInfo.Password)
            cursor.execute(sql, values)
            userInfo.UserID = cursor.lastrowid
            cursor.close()
            conn.commit()
            conn.close()
            return userInfo
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





