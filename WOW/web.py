from flask import Flask, render_template
from flask_restful import Api
from waitress import serve
from flask import request, jsonify, Response
import json

from WOW.wow_resource import UserResource, ProfileResource

app = Flask(__name__)
api = Api(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.html')

@app.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html')






api.add_resource(UserResource, '/user', '/user/<string:username>')
api.add_resource(ProfileResource, '/customer', '/customer/<string:username>')

if __name__ == '__main__':
    app.run()
    #serve(app, host="0.0.0.0", port=8998)
