# -*- coding: utf-8 -*-
import traceback
import sys
import datetime
import json
from flask_restful import reqparse, Resource
from Service.user_service import UserService
from Model.product import ProductInfo
from Model.product import DecimalEncoder


class ProductEnquiryResource(Resource):

    def post(self, prod_str):
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
            print(prod_str)
            result = {"code": 200, "msg": ""}
            prod_dict_list = json.loads(prod_str)
            if prod_dict_list is None:
                result["data"] = []
                result = {"code": 202, "msg": "prod list json is error."}
                return result, result["code"]
            result = user_service.addStockProductEnquiryPrice(OpCode, timestamp, token, prod_dict_list)
            # data = ["DisneyPlus", "Netflix", "Peacock"]
            # json_string = json.dumps(data)
            # print(json_string)
            # prod = ProductInfo()
            # prod.StockProductID = 100
            # prod.shouldPrice = 10.1
            # json_list = json.dumps(prod.__dict__)
            # print(json_list)
            # print('-'*60)
            if prod_list is not None:
                json_list = []
                for prod in prod_list:
                    print(prod.__dict__)
                    # prod_json = json.dumps(prod.desc())
                    json_list.append(prod.desc())
                result["data"] = json_list
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
            print("get product.py", OpCode, time_str)

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        args = parser.parse_args()
        print("request paramter:", args)
        result = args
        return args
