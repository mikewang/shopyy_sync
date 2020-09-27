# -*- coding: utf-8 -*-
from flask_restful import reqparse, Resource
from Service.user_service import UserService


class UserResource(Resource):

    def get(self, OpCode):
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        parser.add_argument('timestamp')
        args = parser.parse_args()
        print("request paramter:", args, OpCode)
        token = args["token"]
        timestamp = args["timestamp"]
        user_service = UserService()
        user_info = user_service.login(OpCode, timestamp, token)
        if user_info is not None:
            return user_info.desc()
        else:
            return {"message": "用户不存在或者密码错"}, 201

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        args = parser.parse_args()
        print("request paramter:", args)
        result = args
        return args
