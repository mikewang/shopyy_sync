from flask import Flask
from flask_restful import Api
from waitress import serve
from Resource.user_resource import UserResource

app = Flask(__name__)
api = Api(app)


@app.route('/')
def hello_world():
    return "Hello Order."


api.add_resource(UserResource, '/User', '/User/<string:OpCode>')


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8997)


# # 'app.py', 'Model/user.py','Resource/user_resource.py','Service/user_dao.py','Service/user_service.py'