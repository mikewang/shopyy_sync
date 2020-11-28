from flask import Flask, render_template
from flask_restful import Api
from waitress import serve
from flask import request

from WOW.wow_service import WowService

app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
def index():
    print("timestamp is ", request.headers.get("timestamp"))
    return render_template('index2.html')


@app.route('/signup', methods=['GET', 'POST'])
def signin():
    request_timestamp = 100
    # print("request.headers is ", request.headers)

    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        print("Authority is ", request.headers.get("Authority"))
        username = request.form["username"]
        password = request.form["password"]

        print("-"*60)

        print("signup", username, password)
        return render_template('signup.html')


if __name__ == '__main__':
    app.run()
    # serve(app, host="0.0.0.0", port=8998)
