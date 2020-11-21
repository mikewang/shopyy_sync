from flask import Flask, render_template
from flask_restful import Api
from waitress import serve
from Resource.user_resource import UserResource
from Resource.product_resource import ProductResource
from Resource.image_resource import ImageResource
from Resource.wow_resource import WOWResource
from Model.product import ProductInfo
import decimal


app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
def index():

    my_int = 18
    my_str = 'curry'
    my_list = [1, 5, 4, 3, 2]
    my_dict = {
        'name': 'durant',
        'age': 28
    }

    # render_template方法:渲染模板
    # 参数1: 模板名称  参数n: 传到模板里的数据
    return render_template('hello.html',
                           my_int=my_int,
                           my_str=my_str,
                           my_list=my_list,
                           my_dict=my_dict)
    return render_template('hello.html')
    # return "Hello API."


api.add_resource(UserResource, '/User', '/User/<string:OpCode>')
api.add_resource(ProductResource, '/Product', '/Product/<int:pageNo>')
api.add_resource(ImageResource, '/Image', '/Image/<string:guid>')



#http://127.0.0.1:8997/Product/1?token=014987a60ada732c43262e4fa6d0a119&timestamp=1604754897&OpCode=delong

if __name__ == '__main__':
    # prod = ProductInfo()
    # prod.shouldPrice = decimal.Decimal('11.98')
    # print(prod.__dict__)
    # print(prod.desc())
    serve(app, host="0.0.0.0", port=8998)


# # 'app.py', 'Model/user.py','Resource/user_resource.py','Service/user_dao.py','Service/user_service.py'