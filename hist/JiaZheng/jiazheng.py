from flask import Flask, render_template
from flask_restful import Api
from waitress import serve
from JiaZheng.jiazheng_service import JiaZhengService
from flask import request, jsonify, Response
import json
from JiaZheng.jiazheng_resource import WorkerListResource, CertListResource, WorkerResource

app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/worker', methods=['GET'])
def workder():
    employeeno = request.args.get('employeeno')
    print("request parameter employeeno is ", employeeno)
    if employeeno is None:
        employeeno = 0
    return render_template('worker.html', employeeno=employeeno)


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')


api.add_resource(WorkerListResource, '/worker_list')
api.add_resource(CertListResource, '/cert_list')
api.add_resource(WorkerResource, '/worker', '/worker/<int:employeeno>')


if __name__ == '__main__':
    #app.run()
    serve(app, host="0.0.0.0", port=8998)
