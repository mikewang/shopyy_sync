# -*- coding: utf-8 -*-
import traceback
import sys
import datetime
import os
from io import BytesIO
from PIL import Image, ImageDraw
from flask import send_file, render_template
from flask_restful import reqparse, Resource


class WOWResource(Resource):

    def get(self):
        try:
            # 增加请求解析参数
            # parser = reqparse.RequestParser()
            # parser.add_argument('OpCode')
            # parser.add_argument('token')
            # parser.add_argument('timestamp')
            # parser.add_argument('year')
            # parser.add_argument('month')
            # parser.add_argument('module')
            # # 分析请求
            # args = parser.parse_args()
            # OpCode = args["OpCode"]
            # token = args["token"]
            # timestamp = args["timestamp"]
            # year = args["year"]
            # month = args["month"]
            # module = args["module"]
            # print(args)
            my_int = 18
            my_str = 'curry'
            my_list = [1, 5, 4, 3, 2]
            my_dict = {
                'name': 'durant',
                'age': 28
            }

            # render_template方法:渲染模板
            # 参数1: 模板名称  参数n: 传到模板里的数据
            return render_template('hello.html', my_int=my_int, my_str=my_str, my_list=my_list, my_dict=my_dict)
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
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        args = parser.parse_args()
        print("request paramter:", args)
        result = args
        return args
