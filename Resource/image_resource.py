# -*- coding: utf-8 -*-
import traceback
import sys
import datetime
import os
from io import BytesIO
from PIL import Image, ImageDraw
from flask import send_file
from flask_restful import reqparse, Resource
from Service.stock_service import StockService


class ImageResource(Resource):

    def get(self, guid):
        try:
            # 增加请求解析参数
            parser = reqparse.RequestParser()
            parser.add_argument('OpCode', location='headers')
            parser.add_argument('token', location='headers')
            parser.add_argument('timestamp', location='headers')
            parser.add_argument('year')
            parser.add_argument('month')
            parser.add_argument('module')
            # 分析请求
            args = parser.parse_args()
            OpCode = args["OpCode"]
            token = args["token"]
            timestamp = args["timestamp"]
            year = args["year"]
            month = args["month"]
            module = args["module"]
            print(args)
            user_service = StockService()
            filepath = os.path.normpath(os.path.join("D:\ymcartphotos", "2019", "01", "501", "201901084598491BB92E63A2B183F04758DF4278"))
            filepath = user_service.get_product_image(OpCode, timestamp, token, guid, year, month, module)
            try:
                image = Image.open(filepath)
            except Exception as e:
                print(e)
                image = Image.new("RGB", (200, 50))
                draw = ImageDraw.Draw(image)
                draw.text((10, 10), "big image is not existed.")
            img_io = BytesIO()
            image.save(img_io, 'JPEG', quality=70)
            img_io.seek(0)
            return send_file(img_io, mimetype="image/jpeg")
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
            print("get image", OpCode, time_str)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        args = parser.parse_args()
        print("request paramter:", args)
        result = args
        return args
