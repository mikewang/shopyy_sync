from flask import Flask, render_template
from flask_restful import Api
from waitress import serve
from flask import request, jsonify, Response
import json

from WOW.wow_resource import UserResource, ProfileResource, RentalResource

app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/signin', methods=['GET'])
def signin():
    return render_template('signin.html')


@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')


@app.route('/customer', methods=['GET'])
def customer():
    return render_template('customer.html')


@app.route('/rental', methods=['GET'])
def rental():
    return render_template('rental.html')


api.add_resource(UserResource, '/user', '/user/<string:username>')
api.add_resource(ProfileResource, '/customer', '/customer/<string:username>')
api.add_resource(RentalResource, '/rental', '/rental/<string:username>')

if __name__ == '__main__':
    #app.run()
    serve(app, host="0.0.0.0", port=8998)
