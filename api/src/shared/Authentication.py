# -*- coding: utf-8 -*-
#src/shared/Authentication
"""
                            User Service
    ------------------------------------------------------------------------
                        Authentication
    ------------------------------------------------------------------------
    

"""

import jwt
import os
import datetime
from flask import json, Response, request, g
from functools import wraps
from ..models.UserModel import UserModel, UserSchema

user_schema = UserSchema()

class Auth():
  """
  Auth Class
  """

  @staticmethod
  def generate_token(user_id):
    """
    Generate Token Method
    """
    try:
      payload = {
        #exp -> data do token como 1 dia após sua criação
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=int(60)),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
      }
      return jwt.encode(
        payload,
        os.getenv('JWT_SECRET_KEY'),
        'HS256'
      ).decode("utf-8")
    except Exception as e:
      return Response(
        mimetype="application/json",
        response=json.dumps({'error': 'error in generating user token:'+str(e)}),
        status=400
      )

  @staticmethod
  def decode_token(token):
    """
    Decode token method
    """
    re = {'data': {}, 'error': {}}
    try:
      payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'))
      re['data'] = {'user_id': payload['sub']}
      return re
    except jwt.ExpiredSignatureError as e1:
      re['error'] = {'message': 'token expired, please login again'}
      return re
    except jwt.InvalidTokenError:
      re['error'] = {'message': 'Invalid token, please try again with a new token'}
      return re

  @staticmethod
  def auth_required(func):
    """
    Auth decorator
    """
    @wraps(func)
    def decorated_auth(*args, **kwargs):
      if 'api-token' not in request.headers:
        return Response(
          mimetype="application/json",
          response=json.dumps({'error': 'Authentication token is not available, please request to get one'}),
          status=400
        )
      token = request.headers.get('api-token')
      data = Auth.decode_token(token)
      if data['error']:
        return Response(
          mimetype="application/json",
          response=json.dumps(data['error']),
          status=401
        )
        
      user_id = data['data']['user_id']
      check_user = UserModel.get_one_user(user_id)
      if not check_user:
        return Response(
          mimetype="application/json",
          response=json.dumps({'error': 'user does not exist, invalid token'}),
          status=402
        )
      data_user = user_schema.dump(check_user)
      g.user = {'id': user_id,
                'role': data_user.get('role')}
      return func(*args, **kwargs)
    return decorated_auth
