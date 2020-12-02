# -*- coding: utf-8 -*-
import traceback
import sys
import datetime
from flask_restful import reqparse, Resource
from Service.stock_service import StockService
import json


class UserResource(Resource):

    def get(self, OpCode):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('token', location='headers')
            parser.add_argument('timestamp', location='headers')
            args = parser.parse_args()
            print("request paramter:", args, OpCode)
            token = args["token"]
            timestamp = args["timestamp"]
            stock_service = StockService()
            user_info = stock_service.login(OpCode, timestamp, token)
            result = {"code": 200, "msg": ""}
            if user_info is not None:
                result["data"] = user_info
            else:
                result = {"code": 201, "msg": "用户不存在或者密码错"}
            return json.dumps(result), result["code"]
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
        finally:
            time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print("get user", OpCode, time_str)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        args = parser.parse_args()
        print("request parameter:", args)
        return None
