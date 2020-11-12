from flask import Flask
from flask_restful import Api
from waitress import serve
from Resource.user_resource import UserResource
from Resource.product_resource import ProductResource
from Resource.image_resource import ImageResource

app = Flask(__name__)
api = Api(app)


@app.route('/')
def hello_world():
    return "Hello API."


api.add_resource(UserResource, '/User', '/User/<string:OpCode>')
api.add_resource(ProductResource, '/Product', '/Product/<int:pageNo>')
api.add_resource(ImageResource, '/Image', '/Image/<string:guid>')

#http://127.0.0.1:8997/Product/1?token=014987a60ada732c43262e4fa6d0a119&timestamp=1604754897&OpCode=delong

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8998)


# # 'app.py', 'Model/user.py','Resource/user_resource.py','Service/user_dao.py','Service/user_service.py'