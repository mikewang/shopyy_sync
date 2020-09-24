# -*- coding: utf-8 -*-
from flask_restful import reqparse, Resource
from OrderAPI.Service.user_service import UserService


class UserResource(Resource):

    def get(self, OpCode):
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        args = parser.parse_args()
        print("request paramter:", args, OpCode)
        token = args["token"]
        user_service = UserService()
        user_info = user_service.login(OpCode, 1001, token)
        if user_info is not None:
            return user_info.desc()
        else:
            return {"message": "用户不存在"}, 201

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('token')
        args = parser.parse_args()
        print("request paramter:", args)
        result = args
        return args
