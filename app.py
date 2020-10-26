from flask import Flask
from flask_restful import Api
from waitress import serve
from Resource.user_resource import UserResource
from Resource.product_resource import ProductResource

app = Flask(__name__)
api = Api(app)


@app.route('/')
def hello_world():
    return "Hello API."


api.add_resource(UserResource, '/User', '/User/<string:OpCode>')
api.add_resource(ProductResource, '/Product', '/Product/<string:GoodsCode>')

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8997)


# # 'app.py', 'Model/user.py','Resource/user_resource.py','Service/user_dao.py','Service/user_service.py'