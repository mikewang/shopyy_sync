# -*- coding: utf-8 -*-
import configparser
import traceback
import sys
import os
import datetime
import base64
import decimal
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

    def select_certificate(self):
        try:
            cert_list = []
            conn = self.conn_mysql()
            cursor = conn.cursor()
            sql = "SELECT sevicetype FROM jiazheng.sevicetype order by sevicetype desc"
            cursor.execute(sql)
            for row in cursor:
                cert_list.append(row[0])
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
            print("done", cert_list)
        finally:
            return cert_list

    def select_employee(self, p_employeeno, p_name):
        try:
            employee_list = []
            conn = self.conn_mysql()
            cursor = conn.cursor()
            if p_employeeno is not None:
                sql = "SELECT employeeno, name, sex,DATE_FORMAT(birthday,'%%Y-%%m-%%d') as birthday, national,  degree, telephone, address, salary,  language, certificate FROM employee where employeeno=%s"
                cursor.execute(sql, p_employeeno)
            elif p_name is not None:
                sql = "SELECT employeeno, name, sex,DATE_FORMAT(birthday,'%%Y-%%m-%%d') as birthday, national,  degree, telephone, address, salary,  language, certificate FROM employee where name like %s"
                cursor.execute(sql, '%' + p_name + '%')
            else:
                sql = "SELECT employeeno, name, sex,DATE_FORMAT(birthday,'%Y-%m-%d') as birthday, national,  degree, telephone, address, salary,  language, certificate FROM employee"
                cursor.execute(sql)
            for row in cursor:
                employee = Employee()
                employee.employeeno = row[0]
                employee.name = row[1]
                employee.sex = row[2]
                employee.birthday = row[3]
                employee.national = row[4]
                employee.degree = row[5]
                employee.telephone = row[6]
                employee.address = row[7]
                employee.salary = row[8]
                employee.language = row[9]
                employee.certificate = row[10]
                print("employee", employee.desc())
                employee_list.append(employee)
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
            print("done", employee_list)
        finally:
            return employee_list

    def insert_employee(self, p_employee):
        try:
            employee = p_employee
            conn = self.conn_mysql()
            cursor = conn.cursor()
            sql = "insert into employee( name, sex, birthday, national,  degree, telephone, address, salary,  language, certificate) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
            values = (employee.name, employee.sex ,employee.birthday,employee.national,  employee.degree,employee.telephone , employee.address, employee.salary, employee.language,employee.certificate )
            cursor.execute(sql, values)
            employee.employeeno = cursor.lastrowid
            cursor.close()
            conn.commit()
            conn.close()
            return employee
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

    def update_employee(self, p_employee):
        try:
            employee = p_employee
            conn = self.conn_mysql()
            cursor = conn.cursor()
            sql = "update employee set name =%s, sex=%s, birthday=%s, national=%s,  degree=%s, telephone=%s, address=%s, salary=%s,  language=%s, certificate=%s where employeeno=%s"
            values = (employee.name, employee.sex ,employee.birthday,employee.national,  employee.degree,employee.telephone , employee.address,employee.salary, employee.language,employee.certificate,employee.employeeno )
            cursor.execute(sql, values)
            cursor.close()
            conn.commit()
            conn.close()
            return employee
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

    def delete_employee(self, employeeno):
        try:
            conn = self.conn_mysql()
            cursor = conn.cursor()
            sql = "delete from  employee  where employeeno=%s"
            values = (employeeno)
            cursor.execute(sql, values)
            cursor.close()
            conn.commit()
            conn.close()
            return "1"
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

