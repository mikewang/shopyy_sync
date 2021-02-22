# -*- coding: utf-8 -*-
import traceback
import sys
import datetime
import json
from flask_restful import reqparse, Resource
from Service.stock_service import StockService
import base64


def urlsafe_base64(base64_str):
    return base64_str.replace('*', '+').replace('-', '/').replace('.', '=')


class ProductOrderpriceResource(Resource):

    def get(self, pageNo):
        try:
            # 增加请求解析参数
            parser = reqparse.RequestParser()
            parser.add_argument('OpCode', location='headers')
            parser.add_argument('token', location='headers')
            parser.add_argument('timestamp', location='headers')
            # parser.add_argument('OpCode', location=['headers', 'args'])
            # parser.add_argument('token', location=['headers', 'args'])
            # parser.add_argument('timestamp', location=['headers', 'args'])
            parser.add_argument('t')
            parser.add_argument('ptypes')
            parser.add_argument('stockProductIDs')
            parser.add_argument('specNos')
            # 分析请求
            args = parser.parse_args()
            OpCode = args["OpCode"]
            token = args["token"]
            timestamp = args["timestamp"]
            ptypes = args["ptypes"]
            print("request args is ", args)
            query_params = {}
            stockProductIDs_base64 = args["stockProductIDs"]
            if stockProductIDs_base64 is not None:
                stockProductIDs_base64 = urlsafe_base64(stockProductIDs_base64)
                stockProductIDs = base64.b64decode(stockProductIDs_base64).decode('utf-8')
                query_params['stockProductIDs'] = stockProductIDs
                print("orderprice key is ", args["stockProductIDs"], stockProductIDs)
            else:
                query_params['stockProductIDs'] = None
            specNos_base64 = args["specNos"]
            if specNos_base64 is not None:
                specNos_base64 = urlsafe_base64(specNos_base64)
                specNos = base64.b64decode(specNos_base64).decode('utf-8')
                query_params['specNos'] = specNos
                print("orderprice key is ", args["specNos"], specNos)
            else:
                query_params['specNos'] = None

            print("query_params is ", query_params)
            orderprice_service = StockService()
            orderprice_prod_list, prod_count = orderprice_service.get_orderprice_product(OpCode, timestamp, token, pageNo, query_params, ptypes)
            result = {"code": 200, "msg": "", "count": prod_count}
            if orderprice_prod_list is not None:
                json_list = []
                for prod in orderprice_prod_list:
                    print("orderprice prod is ", prod.desc())
                    # prod_json = json.dumps(prod.desc())
                    json_list.append(prod.desc())
                result["data"] = json_list
            else:
                result["data"] = []
                result = {"code": 201, "msg": "product is not existed."}
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
            print("get orderprice product ", OpCode, time_str)

    def post(self):
        try:
            # 增加请求解析参数
            parser = reqparse.RequestParser()
            parser.add_argument('OpCode', location='headers')
            parser.add_argument('token', location='headers')
            parser.add_argument('timestamp', location='headers')
            parser.add_argument('prod_list', location='json')
            parser.add_argument('operate', location='json')
            # 分析请求
            args = parser.parse_args()
            OpCode = args["OpCode"]
            token = args["token"]
            timestamp = args["timestamp"]
            operate = args["operate"]
            prod_list_json_base64 = args["prod_list"]
            prod_list_json_base64 = urlsafe_base64(prod_list_json_base64)
            prod_list_json = base64.b64decode(prod_list_json_base64).decode('utf-8')
            run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(run_time_str, "prod json is ", prod_list_json)
            result = {"code": 201, "msg": ""}
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
            run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(run_time_str, "add order product ", OpCode)
