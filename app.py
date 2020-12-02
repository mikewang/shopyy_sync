from flask import Flask, render_template, url_for, Response
from flask_restful import Api
from waitress import serve
from Resource.user_resource import UserResource
from Resource.product_resource import ProductResource
from Resource.image_resource import ImageResource
from Resource.dict_resource import DictResource
from Resource.product_enquiry_resource import ProductEnquiryResource as EnquiryResource
from Resource.product_order_resource import ProductOrderResource as OrderResource

app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
def index():
    return "Hello API."


api.add_resource(UserResource, '/User', '/User/<string:OpCode>')
api.add_resource(ProductResource, '/Product', '/Product/<int:pageNo>')
api.add_resource(ImageResource, '/Image', '/Image/<string:guid>')
api.add_resource(DictResource, '/Dict', '/Dict/<string:item_type>')
api.add_resource(EnquiryResource, '/Enquiry')
api.add_resource(OrderResource, '/Order', '/Order/<int:pageNo>')


@api.representation('text/html')  # 当要返回的数据类型是这里定义的content-type的时候，会执行这里的函数
def output_html(data, code, headers):
    """ 在representation装饰的函数中，必须放回一个Response对象 """
    resp = Response(data)
    return resp


# http://127.0.0.1:8997/Product/1?token=014987a60ada732c43262e4fa6d0a119&timestamp=1604754897&OpCode=delong

if __name__ == '__main__':
    # prod = ProductInfo()
    # prod.shouldPrice = decimal.Decimal('11.98')
    # print(prod.__dict__)
    # print(prod.desc())
    # jsonstr = "[{'name':'test'},{'name':'abcd'}]"
    # print(jsonstr)
    # jsondict = json.loads(jsonstr)
    # for dd in jsondict:
    #     print(dd["name"])
    # print(jsondict)
    # p1 = float('1.0')
    # p2 = eval('1e-3')
    # p3 = p1*p2
    # print("p3", p3)

    # temp_prod_list = "[{'stockProductID': 10703, 'createTime': '2020-11-24 18:00:54', 'opCode': 'delong', 'ID': 0}, {'createTime': '2020-11-24 18:00:54', 'ID': 0, 'stockProductID': 10704, 'opCode': 'delong'}, {'opCode': 'delong', 'stockProductID':10708, 'ID': 0, 'createTime': '2020-11-24 18:00:54'}, {'createTime': '2020-11-24 18:00:54', 'stockProductID': 10709, 'opCode': 'delong', 'ID': 0}]"
    # # prod_dict_list = prod_list
    # t1 = eval(temp_prod_list)
    # t1 = json.dumps(t1)
    # print("temp_prod_list is ", t1)
    # prod_dict_list = json.loads(t1)
    # print("prod_dict_list length is ", len(prod_dict_list))
    # base64_str = "W3sib3BDb2RlIjoiZGVsb25nIiwiSUQiOjAsInN0b2NrUHJvZHVjdElEIjoxMDcwMywiY3JlYXRlVGltZSI6IjIwMjAtMTEtMjUgMDg6MzI6MTgifSx7InN0b2NrUHJvZHVjdElEIjoxMDcwNCwib3BDb2RlIjoiZGVsb25nIiwiY3JlYXRlVGltZSI6IjIwMjAtMTEtMjUgMDg6MzI6MTgiLCJJRCI6MH0seyJvcENvZGUiOiJkZWxvbmciLCJJRCI6MCwic3RvY2tQcm9kdWN0SUQiOjEwNzA3LCJjcmVhdGVUaW1lIjoiMjAyMC0xMS0yNSAwODozMjoxOCJ9XQ=="
    # jsonstr = base64.b64decode(base64_str).decode('utf-8')
    # jsondict = json.loads(jsonstr)
    # print(len(jsondict))
    #
    # base64_str = "5pyq6K+i5Lu3"
    # jsonstr = base64.b64decode(base64_str).decode('utf-8')
    # print(jsonstr)
    # ss_bytes = bytes(jsonstr, 'utf-8')
    # ss = base64.b64encode(ss_bytes).decode()
    # print(base64_str)
    # print(ss)
    serve(app, host="0.0.0.0", port=8998)
