# -*- coding: utf-8 -*-
import traceback
import sys
import datetime
import os
from io import BytesIO
from PIL import Image, ImageDraw
from flask import send_file, render_template
from flask_restful import reqparse, Resource


class UserResource(Resource):

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('UserID', location='headers')
            parser.add_argument('token', location='headers')
            parser.add_argument('timestamp', location='headers')
            # 分析请求
            args = parser.parse_args()
            UserID = args["UserID"]
            token = args["token"]
            timestamp = args["timestamp"]


            # render_template方法:渲染模板
            # 参数1: 模板名称  参数n: 传到模板里的数据
            return render_template('signup.html')
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
        # finally:
        #     time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #     #print("get image", OpCode, time_str)

    def post(self):
        print("user resource is ", self)
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('UserID', location='headers')
            parser.add_argument('token', location='headers')
            parser.add_argument('timestamp', location='headers')
            parser.add_argument('username', location='json')
            parser.add_argument('password', location='json')

            # 分析请求
            args = parser.parse_args()
            UserID = args["UserID"]
            token = args["token"]
            timestamp = args["timestamp"]

            print("parser is ", args)

            return '{"code": "201"}'
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

