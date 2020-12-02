# -*- coding: utf-8 -*-
import traceback
import sys
import datetime
import json
from flask_restful import reqparse, Resource
from Service.stock_service import StockService
from Model.product import ProductInfo
from Model.product import DecimalEncoder
import base64


def base64Replace(base64_str):
    return base64_str.replace('*', '+').replace('-', '/').replace('.', '=')


class ProductEnquiryResource(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        args = parser.parse_args()
        print("request paramter:", args)
        result = args
        return args

    def post(self):
        try:
            # 增加请求解析参数
            parser = reqparse.RequestParser()
            # parser.add_argument('OpCode', location=['headers', 'args'])
            # parser.add_argument('token', location=['headers', 'args'])
            # parser.add_argument('timestamp', location=['headers', 'args'])
            parser.add_argument('OpCode', location='headers')
            parser.add_argument('token', location='headers')
            parser.add_argument('timestamp', location='headers')
            parser.add_argument('prod_list', location='json')
            # 分析请求
            args = parser.parse_args()
            print("reqparse args is ", args)
            OpCode = args["OpCode"]
            token = args["token"]
            timestamp = args["timestamp"]
            prod_list_json_base64 = args["prod_list"]
            prod_list_json_base64 = base64Replace(prod_list_json_base64)
            prod_list_json = base64.b64decode(prod_list_json_base64).decode('utf-8')
            user_service = StockService()
            print("prod list json data is ", prod_list_json)
            result = {"code": 201, "msg": ""}
            # prod_dict_list = prod_list
            prod_dict_list = json.loads(prod_list_json)
            if prod_dict_list is None:
                result["data"] = []
                result = {"code": 500, "msg": "prod list json is error."}
                return result, result["code"]
            result_status = user_service.addStockProductEnquiryPrice(OpCode, timestamp, token, prod_dict_list)
            # data = ["DisneyPlus", "Netflix", "Peacock"]
            # json_string = json.dumps(data)
            # print(json_string)
            # prod = ProductInfo()
            # prod.StockProductID = 100
            # prod.shouldPrice = 10.1
            # json_list = json.dumps(prod.__dict__)
            # print(json_list)
            # print('-'*60)
            if result_status is not None:
                result["data"] = result_status
            else:
                result["data"] = []
                result = {"code": 201, "msg": "product.py is not existed."}
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
            print("enquiry price product.py", OpCode, time_str)


