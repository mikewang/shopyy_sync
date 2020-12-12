# -*- coding: utf-8 -*-
import traceback
import sys
import datetime
import os
from io import BytesIO
from PIL import Image, ImageDraw
from flask import send_file, render_template
from flask_restful import reqparse, Resource
import json
from JiaZheng.jiazheng_service import JiaZhengService


class CertListResource(Resource):

    def get(self):
        try:
            parser = reqparse.RequestParser()
            # 分析请求
            args = parser.parse_args()
            cert_list = JiaZhengService().getCert()
            print("get cert_list is ", cert_list)
            if cert_list is not None:
                result = {"stat": 1, "data": cert_list}
                return result, 200
            else:
                result = {"stat": 0}
                return result, 201
                #return json.dumps(result), 201
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # Get information about the exception that is currently being handled
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print('e.message:\t', exc_value)
            print("Note, object e and exc of Class %s is %s the same." % (type(exc_value), ('not', '')[exc_value is e]))
            print('traceback.print_exc(): ', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            print('#' * 60)
            result = {"stat": 0}
            return result, 201

class WorkerListResource(Resource):

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('name')
            # 分析请求
            args = parser.parse_args()
            name = args["name"]

            employee_list = JiaZhengService().getEmployee(None, name)
            print("get employee_list is ", employee_list)
            if employee_list is not None:
                emp_ss = []
                for employee in employee_list:
                    emp_ss.append(employee.desc())
                result = {"stat": 1, "data": emp_ss}
                return result, 200
            else:
                result = {"stat": 0}
                return result, 201
                #return json.dumps(result), 201
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # Get information about the exception that is currently being handled
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print('e.message:\t', exc_value)
            print("Note, object e and exc of Class %s is %s the same." % (type(exc_value), ('not', '')[exc_value is e]))
            print('traceback.print_exc(): ', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            print('#' * 60)
            result = {"stat": 0}
            return result, 201


class WorkerResource(Resource):

    def get(self, employeeno):
        try:
            parser = reqparse.RequestParser()
            # 分析请求
            args = parser.parse_args()

            employee_list = JiaZhengService().getEmployee(employeeno, None)
            print("get employee_list is ", employee_list)
            if employee_list is not None and len(employee_list) > 0:
                employee = employee_list[0]
                result = {"stat": 1, "data": employee.desc()}
                return result, 200
            else:
                result = {"stat": 0}
                return result, 201
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # Get information about the exception that is currently being handled
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print('e.message:\t', exc_value)
            print("Note, object e and exc of Class %s is %s the same." % (type(exc_value), ('not', '')[exc_value is e]))
            print('traceback.print_exc(): ', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            print('#' * 60)
            result = {"stat": 0}
            return result, 201

    def post(self):
        print("ProfileResource is ", self)
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('employeeno', location=['json', 'form'])
            parser.add_argument('name', location=['json', 'form'])
            parser.add_argument('sex', location=['json', 'form'])
            parser.add_argument('birthday', location=['json', 'form'])
            parser.add_argument('national', location=['json', 'form'])
            parser.add_argument('certificate', location=['json', 'form'])
            parser.add_argument('degree', location=['json', 'form'])
            parser.add_argument('telephone', location=['json', 'form'])
            parser.add_argument('address', location=['json', 'form'])
            parser.add_argument('salary', location=['json', 'form'])
            parser.add_argument('language', location=['json', 'form'])

            # 分析请求
            args = parser.parse_args()

            print("worker post is ", args)
            employee = JiaZhengService().mergeWorker(args)
            if employee is not None:
                result = {"stat": 1, "data": employee.desc()}
                return result
            else:
                result = {"stat": 0}
                return result
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # Get information about the exception that is currently being handled
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print('e.message:\t', exc_value)
            print("Note, object e and exc of Class %s is %s the same." % (type(exc_value), ('not', '')[exc_value is e]))
            print('traceback.print_exc(): ', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            print('#' * 60)
            result = {"stat": 0}
            return json.dumps(result)


    def delete(self):
        print("ProfileResource is ", self)
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('employeeno', location=['json', 'form'])

            # 分析请求
            args = parser.parse_args()
            employeeno = args["employeeno"]
            print("worker delete is ", args)
            res = JiaZhengService().deleteWorker(args)
            if res is not None:
                result = {"stat": 1, "data": res}
                return result
            else:
                result = {"stat": 0}
                return result
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # Get information about the exception that is currently being handled
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print('e.message:\t', exc_value)
            print("Note, object e and exc of Class %s is %s the same." % (type(exc_value), ('not', '')[exc_value is e]))
            print('traceback.print_exc(): ', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            print('#' * 60)
            result = {"stat": 0}
            return json.dumps(result)


class RentalResource(Resource):

    def get(self, username):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('token', location='headers')
            parser.add_argument('timestamp', location='headers')
            parser.add_argument("rs_id", location=['json', 'args'])
            parser.add_argument("cust_id", location=['json', 'args'])
            # 分析请求
            args = parser.parse_args()
            token = args["token"]
            timestamp = args["timestamp"]
            rs_id = args["rs_id"]
            cust_id = args["cust_id"]

            print(self, args)

            rs_list = WowService().getRentalService(username, token, timestamp, rs_id, cust_id)
            if rs_list is not None:
                rss = []
                for rs in rs_list:
                    rss.append(rs.desc())
                result = {"stat": 1, "rs_list": rss}
                print("get rental service is ", result)
                return json.dumps(result)
            else:
                result = {"stat": 0}
                return json.dumps(result)
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # Get information about the exception that is currently being handled
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print('e.message:\t', exc_value)
            print("Note, object e and exc of Class %s is %s the same." % (type(exc_value), ('not', '')[exc_value is e]))
            print('traceback.print_exc(): ', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            print('#' * 60)
            result = {"stat": 0}
            return json.dumps(result)

    def post(self):
        print("post RentalResource is ", self)
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', location='headers')
            parser.add_argument('token', location='headers')
            parser.add_argument('timestamp', location='headers')
            parser.add_argument('rs_id', location=['json', 'form'])
            parser.add_argument('Pickup_Location', location=['json', 'form'])
            parser.add_argument('Dropoff_Location', location=['json', 'form'])
            parser.add_argument('Pickup_Date', location=['json', 'form'])
            parser.add_argument('Dropoff_Date', location=['json', 'form'])
            parser.add_argument('Start_Odometer', location=['json', 'form'])
            parser.add_argument('End_Odometer', location=['json', 'form'])
            parser.add_argument('Daily_Odometer_Limit', location=['json', 'form'])
            parser.add_argument('Vehicle_ID', location=['json', 'form'])
            parser.add_argument('rental_rate', location=['json', 'form'])
            parser.add_argument('rental_fee', location=['json', 'form'])
            parser.add_argument('rental_amount', location=['json', 'form'])
            parser.add_argument('really_amount', location=['json', 'form'])
            parser.add_argument('Cust_ID', location=['json', 'form'])
            parser.add_argument('wow_userid', location=['json', 'form'])

            # 分析请求
            args = parser.parse_args()
            timestamp = args["timestamp"]
            username = args["username"]
            token = args["token"]
            print("Rental Service post is ", args)
            rental = WowService().mergeRentalService(username, token, timestamp, args)
            if rental is not None:
                result = {"stat": 1, "rental": rental.desc()}
                return json.dumps(result)
            else:
                result = {"stat": 0}
                return json.dumps(result)
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # Get information about the exception that is currently being handled
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print('e.message:\t', exc_value)
            print("Note, object e and exc of Class %s is %s the same." % (type(exc_value), ('not', '')[exc_value is e]))
            print('traceback.print_exc(): ', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            print('#' * 60)
            result = {"stat": 0}
            return json.dumps(result)

    def delete(self):
        print("delete RentalResource is ", self)
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', location='headers')
            parser.add_argument('token', location='headers')
            parser.add_argument('timestamp', location='headers')
            parser.add_argument('rs_id', location=['json', 'form'])

            # 分析请求
            args = parser.parse_args()
            timestamp = args["timestamp"]
            username = args["username"]
            token = args["token"]
            print("Rental Service delete is ", args)
            rental = WowService().deleteRentalService(username, token, timestamp, args)
            if rental is not None:
                result = {"stat": 1, "rental": rental.desc()}
                return json.dumps(result)
            else:
                result = {"stat": 0}
                return json.dumps(result)
        except Exception as e:
            print('str(Exception):\t', str(Exception))
            print('str(e):\t\t', str(e))
            print('repr(e):\t', repr(e))
            # Get information about the exception that is currently being handled
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print('e.message:\t', exc_value)
            print("Note, object e and exc of Class %s is %s the same." % (type(exc_value), ('not', '')[exc_value is e]))
            print('traceback.print_exc(): ', traceback.print_exc())
            print('traceback.format_exc():\n%s' % traceback.format_exc())
            print('#' * 60)
            result = {"stat": 0}
            return json.dumps(result)