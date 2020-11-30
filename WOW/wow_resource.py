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
from WOW.wow_service import WowService


class UserResource(Resource):

    def get(self, username):
        try:
            parser = reqparse.RequestParser()
            #parser.add_argument('username', location='headers')
            parser.add_argument('token', location='headers')
            parser.add_argument('timestamp', location='headers')
            # 分析请求
            args = parser.parse_args()
            token = args["token"]
            timestamp = args["timestamp"]
            print("UserResource get is ", args)

            userinfo = WowService().getUser(username, token, timestamp)
            print("get userinfo is ", userinfo)
            if userinfo is not None:
                result = {"stat": 1}
                return json.dumps(result), 201
            else:
                result = {"stat": 0}
                return json.dumps(result), 201
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
            return json.dumps(result), 201


    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('timestamp', location='headers')
            parser.add_argument('username', location=['json', 'form'])
            parser.add_argument('password', location=['json', 'form'])

            # 分析请求
            args = parser.parse_args()
            timestamp = args["timestamp"]
            username = args["username"]
            password = args["password"]

            print("parser is ", args)
            p_user_info = {"UserName": username, "UserType": "Customer", "Password": password}
            userinfo = WowService().addUser(p_user_info)
            if userinfo is not None:
                result = {"stat": 1}
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
            return json.dumps(result), 201


class ProfileResource(Resource):

    def get(self, username):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('token', location='headers')
            parser.add_argument('timestamp', location='headers')
            # 分析请求
            args = parser.parse_args()
            token = args["token"]
            timestamp = args["timestamp"]
            userprofile = WowService().getUserProfile(username, token, timestamp)
            if userprofile is not None:
                result = {"stat": 1, "customer": userprofile.desc()}
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
        print("ProfileResource is ", self)
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', location='headers')
            parser.add_argument('token', location='headers')
            parser.add_argument('timestamp', location='headers')
            parser.add_argument('CustType', location=['json', 'form'])
            parser.add_argument('FirstName', location=['json', 'form'])
            parser.add_argument('LastName', location=['json', 'form'])
            parser.add_argument('DriverLicenseNumber', location=['json', 'form'])
            parser.add_argument('InsuranceCompanyName', location=['json', 'form'])
            parser.add_argument('InsurancePolicyNumber', location=['json', 'form'])
            parser.add_argument('CorporateName', location=['json', 'form'])
            parser.add_argument('CorporateRegNo', location=['json', 'form'])
            parser.add_argument('CorporateEmployeeID', location=['json', 'form'])
            parser.add_argument('Street', location=['json', 'form'])
            parser.add_argument('City', location=['json', 'form'])
            parser.add_argument('State', location=['json', 'form'])
            parser.add_argument('Country', location=['json', 'form'])
            parser.add_argument('Zip', location=['json', 'form'])
            parser.add_argument('Email', location=['json', 'form'])
            parser.add_argument('Tel', location=['json', 'form'])

            # 分析请求
            args = parser.parse_args()
            timestamp = args["timestamp"]
            username = args["username"]
            token = args["token"]
            print("ProfileResource post is ", args)
            userprofile = WowService().mergeUserProfile(username, token, timestamp, args)
            if userprofile is not None:
                result = {"stat": 1, "customer": userprofile.desc()}
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


class RentalResource(Resource):

    def get(self, username):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('token', location='headers')
            parser.add_argument('timestamp', location='headers')
            parser.add_argument('rs_id', location=['json', 'form'])

            # 分析请求
            args = parser.parse_args()
            token = args["token"]
            timestamp = args["timestamp"]
            rs_id = args["rs_id"]

            rs_list = WowService().getRentalService(username, token, timestamp, rs_id)
            if rs_list is not None:
                rss = []
                for rs in rs_list:
                    rss.append(rs.desc())
                result = {"stat": 1, "rs_list": rss}
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
        print("ProfileResource is ", self)
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', location='headers')
            parser.add_argument('token', location='headers')
            parser.add_argument('timestamp', location='headers')
            parser.add_argument('CustType', location=['json', 'form'])
            parser.add_argument('FirstName', location=['json', 'form'])
            parser.add_argument('LastName', location=['json', 'form'])
            parser.add_argument('DriverLicenseNumber', location=['json', 'form'])
            parser.add_argument('InsuranceCompanyName', location=['json', 'form'])
            parser.add_argument('InsurancePolicyNumber', location=['json', 'form'])
            parser.add_argument('CorporateName', location=['json', 'form'])
            parser.add_argument('CorporateRegNo', location=['json', 'form'])
            parser.add_argument('CorporateEmployeeID', location=['json', 'form'])
            parser.add_argument('Street', location=['json', 'form'])
            parser.add_argument('City', location=['json', 'form'])
            parser.add_argument('State', location=['json', 'form'])
            parser.add_argument('Country', location=['json', 'form'])
            parser.add_argument('Zip', location=['json', 'form'])
            parser.add_argument('Email', location=['json', 'form'])
            parser.add_argument('Tel', location=['json', 'form'])

            # 分析请求
            args = parser.parse_args()
            timestamp = args["timestamp"]
            username = args["username"]
            token = args["token"]
            print("ProfileResource post is ", args)
            userprofile = WowService().mergeUserProfile(username, token, timestamp, args)
            if userprofile is not None:
                result = {"stat": 1, "customer": userprofile.desc()}
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