from flask import Flask, render_template
from flask_restful import Api
from waitress import serve
from JiaZheng.jiazheng_service import JiaZhengService
from flask import request, jsonify, Response
import json
from JiaZheng.jiazheng_resource import WorkerListResource

app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/worker', methods=['GET'])
def signin():
    return render_template('worker.html')


@app.route('/about', methods=['GET'])
def signup():
    return render_template('about.html')


api.add_resource(WorkerListResource, '/worker_list')


if __name__ == '__main__':
    #app.run()
    serve(app, host="0.0.0.0", port=8998)
