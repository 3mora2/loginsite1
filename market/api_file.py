import jwt
from functools import wraps

from flask_restful import Resource, request,reqparse
from flask import jsonify
from . import api, app



class Login(Resource):
    def post(self):
        print()
        return {'hello': 'world'}


api.add_resource(Login, '/api/login')
