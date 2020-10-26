# -*- coding: utf-8 -*-
import traceback
import sys
import datetime
from flask_restful import reqparse, Resource
from Service.user_service import UserService


class ProductResource(Resource):

    def get(self, GoodsCode):
        try:
            # 增加请求解析参数
            parser = reqparse.RequestParser()
            parser.add_argument('OpCode')
            parser.add_argument('token')
            parser.add_argument('timestamp')
            # 分析请求
            args = parser.parse_args()
            OpCode = args["OpCode"]
            token = args["token"]
            timestamp = args["timestamp"]
            user_service = UserService()
            test_image = user_service.testImage(OpCode, timestamp, token, GoodsCode)
            result = {"code": 200, "msg": ""}
            if test_image is not None:
                result["data"] = test_image["imageBase64"]
            else:
                result = {"code": 201, "msg": "产品不存在"}
            return result, result["code"]
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
        finally:
            time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print("get user", OpCode, time_str)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        args = parser.parse_args()
        print("request paramter:", args)
        result = args
        return args
