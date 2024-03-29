# -*- coding: utf-8 -*-
import traceback
import sys
import datetime
import base64
import json
from flask_restful import reqparse, Resource
from Service.stock_service import StockService
from Model.product import ProductInfo
from Model.product import DecimalEncoder


def urlsafe_base64(base64_str):
    return base64_str.replace('*', '+').replace('-', '/').replace('.', '=')

# 采购商品的查询
class ProductStockResource(Resource):

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
            parser.add_argument('contractNo')
            parser.add_argument('specNo')
            parser.add_argument('goodsDesc')
            parser.add_argument('brand')
            parser.add_argument('enquiry')
            parser.add_argument('begin')
            parser.add_argument('end')
            # 分析请求
            args = parser.parse_args()
            OpCode = args["OpCode"]
            token = args["token"]
            timestamp = args["timestamp"]
            ptype = args["ptype"]
            # 去掉订货，订货，订货完成 三个状态的查询
            print("ProductStockResource request args is ", args)
            filter_stock = {}
            contractNo_base64 = args["contractNo"]
            if contractNo_base64 is not None:
                contractNo_base64 = urlsafe_base64(contractNo_base64)
                contractNo = base64.b64decode(contractNo_base64).decode('utf-8')
                filter_stock['contractNo'] = contractNo
                print("contractNo key is ", args["contractNo"], contractNo)
            else:
                filter_stock['contractNo'] = None

            specNo_base64 = args["specNo"]
            if specNo_base64 is not None:
                specNo_base64 = urlsafe_base64(specNo_base64)
                specNo = base64.b64decode(specNo_base64).decode('utf-8')
                filter_stock['specNo'] = specNo
                print("specNo key is ", args["specNo"], specNo)
            else:
                filter_stock['specNo'] = None
            goodsDesc_base64 = args["goodsDesc"]
            if goodsDesc_base64 is not None:
                goodsDesc_base64 = urlsafe_base64(goodsDesc_base64)
                goodsDesc = base64.b64decode(goodsDesc_base64).decode('utf-8')
                filter_stock['goodsDesc'] = goodsDesc
                print("goodsDesc key is ", args["goodsDesc"], goodsDesc)
            else:
                filter_stock['goodsDesc'] = None
            brand_base64 = args["brand"]
            if brand_base64 is not None:
                brand_base64 = urlsafe_base64(brand_base64)
                brands = base64.b64decode(brand_base64).decode('utf-8')
                brand_list = brands.split(';')
                filter_stock['brand'] = brand_list
                print("brand key is ", args["brand"], brand_list)
            else:
                filter_stock['brand'] = None
            enquiry_base64 = args["enquiry"]
            if enquiry_base64 is not None:
                enquiry_base64 = urlsafe_base64(enquiry_base64)
                print("enquiry_base64 is ", enquiry_base64)
                enquiry = base64.b64decode(enquiry_base64).decode('utf-8')
                filter_stock['enquiry'] = enquiry
                print("enquiry key is ", args["enquiry"], enquiry)
            else:
                filter_stock['enquiry'] = None
            begin_base64 = args["begin"]
            if begin_base64 is not None:
                begin_base64 = urlsafe_base64(begin_base64)
                begin_date = base64.b64decode(begin_base64).decode('utf-8')
                filter_stock['begin'] = begin_date
                print("begin_date key is ", args["begin"], begin_date)
            else:
                filter_stock['begin'] = None
            end_base64 = args["end"]
            if end_base64 is not None:
                end_base64 = urlsafe_base64(end_base64)
                end_date = base64.b64decode(end_base64).decode('utf-8')
                filter_stock['end'] = end_date
                print("end_date key is ", args["end"], end_date)
            else:
                filter_stock['end'] = None
            print("filter_stock is ", filter_stock)
            product_service = StockService()
            # 获取采购商品 列表。
            prod_list, prod_count = product_service.get_stock_product(OpCode, timestamp, token, pageNo, filter_stock, ptype)
            result = {"code": 200, "msg": "", "count": prod_count}
            if prod_list is not None:
                json_list = []
                for prod in prod_list:
                    json_list.append(prod.desc())
                result["data"] = json_list
            else:
                result["data"] = []
                result = {"code": 201, "msg": "stock product is not existed."}
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
            print("ProductResource get stock product ", OpCode, time_str)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        args = parser.parse_args()
        print("request paramter:", args)
        result = args
        return args
