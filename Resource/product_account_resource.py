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


class ProductAccountResource(Resource):

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
            parser.add_argument('ptype')
            parser.add_argument('orderID')
            parser.add_argument('batchNo')
            parser.add_argument('goodsDesc')
            parser.add_argument('brand')
            parser.add_argument('enquiry')
            parser.add_argument('begin')
            parser.add_argument('end')
            parser.add_argument('supplier')
            parser.add_argument('specno')
            # 分析请求
            args = parser.parse_args()
            OpCode = args["OpCode"]
            token = args["token"]
            timestamp = args["timestamp"]
            ptype = args["ptype"]
            print("request args is ", args)
            filter_stock = {}
            orderID = args["orderID"]
            if orderID is not None:
                filter_stock['orderID'] = orderID
                print("enquiry key is ", args["orderID"], orderID)
            else:
                filter_stock['orderID'] = None
            enquiry_base64 = args["batchNo"]
            if enquiry_base64 is not None:
                enquiry_base64 = base64Replace(enquiry_base64)
                print("enquiry_base64 is ", enquiry_base64)
                batchNo = base64.b64decode(enquiry_base64).decode('utf-8')
                filter_stock['batchNo'] = batchNo
                print("enquiry key is ", args["batchNo"], batchNo)
            else:
                filter_stock['batchNo'] = None
            goodsDesc_base64 = args["goodsDesc"]
            if goodsDesc_base64 is not None:
                goodsDesc_base64 = base64Replace(goodsDesc_base64)
                goodsDesc = base64.b64decode(goodsDesc_base64).decode('utf-8')
                filter_stock['goodsDesc'] = goodsDesc
                print("goodsDesc key is ", args["goodsDesc"], goodsDesc)
            else:
                filter_stock['goodsDesc'] = None
            brand_base64 = args["brand"]
            if brand_base64 is not None:
                brand_base64 = base64Replace(brand_base64)
                brands = base64.b64decode(brand_base64).decode('utf-8')
                brand_list = brands.split(';')
                filter_stock['brand'] = brand_list
                print("brand key is ", args["brand"], brand_list)
            else:
                filter_stock['brand'] = None

            begin_base64 = args["begin"]
            if begin_base64 is not None:
                begin_base64 = base64Replace(begin_base64)
                begin_date = base64.b64decode(begin_base64).decode('utf-8')
                filter_stock['begin'] = begin_date
                print("begin_date key is ", args["begin"], begin_date)
            else:
                filter_stock['begin'] = None
            end_base64 = args["end"]
            if end_base64 is not None:
                end_base64 = base64Replace(end_base64)
                end_date = base64.b64decode(end_base64).decode('utf-8')
                filter_stock['end'] = end_date
                print("end_date key is ", args["end"], end_date)
            else:
                filter_stock['end'] = None
            supplier_base64 = args["supplier"]
            if supplier_base64 is not None:
                supplier_base64 = base64Replace(supplier_base64)
                supplier = base64.b64decode(supplier_base64).decode('utf-8')
                filter_stock['supplier'] = supplier
                print("supplier key is ", args["supplier"], supplier)
            else:
                filter_stock['supplier'] = None
            specno_base64 = args["specno"]
            if specno_base64 is not None:
                specno_base64 = base64Replace(specno_base64)
                specno = base64.b64decode(specno_base64).decode('utf-8')
                filter_stock['specno'] = specno
                print("specno key is ", args["specno"], specno)
            else:
                filter_stock['specno'] = None

            print("filter_stock is ", filter_stock)
            user_service = StockService()
            account_prod_list, prod_count, product_list = user_service.get_account_product(OpCode, timestamp, token, pageNo, filter_stock, ptype)
            result = {"code": 200, "msg": "", "count": prod_count}
            if account_prod_list is not None:
                json_list = []
                for prod in account_prod_list:
                    # prod_json = json.dumps(prod.desc())
                    json_list.append(prod.desc())
                result["data"] = json_list
                json_list = []
                for prod in product_list:
                    # prod_json = json.dumps(prod.desc())
                    json_list.append(prod.desc())
                result["data2"] = json_list
            else:
                result["data"] = []
                result["data2"] = []
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
            print("get account product ", OpCode, time_str)

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
            prod_list_json_base64 = base64Replace(prod_list_json_base64)
            prod_list_json = base64.b64decode(prod_list_json_base64).decode('utf-8')
            run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(run_time_str, "prod json is ", prod_list_json)
            result = {"code": 201, "msg": ""}
            prod_dict_list = json.loads(prod_list_json)
            if prod_dict_list is None:
                result["data"] = []
                result = {"code": 500, "msg": "prod json is error."}
                return result, result["code"]
            user_service = StockService()
            result_product = user_service.post_order_product(OpCode, timestamp, token, prod_dict_list, operate)
            if result_product is not None:
                result = {"code": 200, "msg": ""}
                json_list = []
                for prod in result_product:
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
            run_time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(run_time_str, "add order product ", OpCode)
