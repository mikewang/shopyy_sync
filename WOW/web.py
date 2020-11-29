from flask import Flask, render_template
from flask_restful import Api
from waitress import serve
from flask import request, jsonify, Response
import json

from WOW.wow_resource import UserResource

app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
def index():
    print("timestamp is ", request.headers.get("timestamp"))
    return render_template('index2.html')

@api.representation('text/html')  # 当要返回的数据类型是这里定义的content-type的时候，会执行这里的函数
def output_html(data, code, headers):
    """ 在representation装饰的函数中，必须放回一个Response对象 """
    resp = Response(data)
    return resp

api.add_resource(UserResource, '/signup')


@app.route('/signup2', methods=['GET', 'POST'])
def signin():
    request_timestamp = 100
    # print("request.headers is ", request.headers)

    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        print("Authority is ", request.headers.get("Authority"))
        jsondata = request.get_data()
        jsonstring = jsondata.decode()
        print("json string is ", jsonstring)
        jsondata = json.loads(jsonstring)
        print("jsondata is ", jsondata)
        username = jsondata["username"]
        password = jsondata["password"]

        print("-"*60)

        print("signup", username, password)
        return render_template('signup.html')


if __name__ == '__main__':
    #app.run()
    serve(app, host="0.0.0.0", port=8998)
