# -*- coding: utf-8 -*-
#/src/views/UserView

"""
                         User Service
    ------------------------------------------------------------------------
                        User EndPoints
    ------------------------------------------------------------------------
    

"""
import datetime
from flask import request, json, Response, Blueprint, g
from ..models.UserModel import UserModel, UserSchema
from ..shared.Authentication import Auth

user_api = Blueprint('user_api', __name__) 
user_schema = UserSchema()




@user_api.route('/', methods=['POST'])
def create():
  """
  

  Create User Function
  --- 
  /v1/api/users/:
    post:
      summary: Create a user Function. It will return the JWT token if the request was successful
      tags:
        - User
      requestBody:
        description: User Functions
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - name
                - email
                - password
                - role
                - deleted_app
                - created_app
                - modified_app
              properties:
                name:
                  type: string
                email:
                  type: string
                password:
                  type: string
                role:
                  type: string
                active:
                  type: boolean
                deleted_app:
                  type: integer
                created_app:
                  type: integer
                modified_app:
                  type: integer
  
      responses:
        '200':
          description: User successfully registered
        '400':
          description: Error in request
        '401':
          description: Missing data
        '402':
          description: User already exist, please supply another email address

  """
  try:
    req_data = request.get_json()
  except:
    return custom_response({'erro': 'Not request'}, 400) 

  try:
    data = user_schema.load(req_data)
  except Exception as error:
    return custom_response(str(error), 401)
  
  user_in_db = UserModel.get_user_by_email(data.get('email'))
  if user_in_db:
    message = {'error': 'User already exist, please supply another email address'}
    return custom_response(message, 402)
  
  user = UserModel(data)
  user.save()
  ser_data = user_schema.dump(user)
  token = Auth.generate_token(ser_data.get('id'))
  return custom_response({'jwt_token': token}, 200)







@user_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
  """


  Get all users
   --- 
  /v1/api/users/:
    get:
      summary: Get all users Function
      security:
        - APIKeyHeader: []
      tags:
        - User
      
      responses:
        '200':
          description: Returns all users
        '400':
          description: User not found
        '401':
          description: Permission denied
  """
  post_user= UserModel.get_one_user(g.user.get('id'))
  if not post_user:
    return custom_response({'error': 'user not found'}, 400)
  data_user= user_schema.dump(post_user)

  if data_user.get('role') != 'Admin':
    return custom_response({'error': 'permission denied'}, 401)

  users = UserModel.get_all_users()
  ser_users = user_schema.dump(users, many=True)
  return custom_response(ser_users, 200)






@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id):
  """
  Get a single user
  ---
  /v1/api/users/{user_id}:
    get:
      summary: Gets a user by ID.
      security:
        - APIKeyHeader: []
      tags:
        - User
      parameters:
        - in: path
          name: user_id
          required: true
          schema:
            type: integer
            minimum: 1
            description: The user ID.

      responses:
        '200':
          description: Data this user successfully
        '400':
          description: user not found
        '401':
          description: Permission denied
  """
  user = UserModel.get_one_user(user_id)
  if not user:
    return custom_response({'error': 'user not found'}, 400)
  data = user_schema.dump(user)

  if g.user.get('id') != data.get('id'):
    if g.user.get('role') != 'Admin':
      return custom_response({'error': 'permission denied'}, 401)
  
  return custom_response(data, 200)







@user_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
  """
  Update me
  ---
  /v1/api/users/{me}:
    put:
      summary: Update-me.
      security:
        - APIKeyHeader: []
      tags:
        - User
      parameters:
        - in: path
          name: me
          required: true
          schema:
            type: string
            description: The user ID.
      requestBody:
        description: User Functions
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - name
                - email
                - password
                - role
                - deleted_app
                - created_app
                - modified_app
              properties:
                name:
                  type: string
                email:
                  type: string
                password:
                  type: string
                role:
                  type: string
                active:
                  type: boolean
                deleted_app:
                  type: integer
                created_app:
                  type: integer
                modified_app:
                  type: integer
      responses:
        '200':
          description: User successfully update
        '400':
          description: Not request
        '401':
          description: Missing data
      
  """
  try:
    req_data = request.get_json()
  except:
    return custom_response({'erro': 'Not request'}, 400) 

  try:
    data = user_schema.load(req_data, partial= True)
  except Exception as error:
    return custom_response(str(error), 401)

  user = UserModel.get_one_user(g.user.get('id'))
  user.update(data)
  ser_user = user_schema.dump(user)
  return custom_response(ser_user, 200)






@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
  """
  Delete a user
  ---
  /v1/api/users/me:
    delete:
      summary: Return your user data.
      security:
        - APIKeyHeader: []
      tags:
        - User
      responses:
        '200':
          description: An Access Token API to be used in Boleto Viewer
  """
  user = UserModel.get_one_user(g.user.get('id'))
  user['deleted_at']= datetime.datetime.utcnow()
  user.update(data)
  #user.delete()
  return custom_response({'message': 'deleted'}, 200)



@user_api.route('/<int:user_id>', methods=['DELETE'])
@Auth.auth_required
def delete_user(user_id):
  """
  Delete A Profile
  ---
  /v1/api/users/{user_id}:
    delete:
      summary: Delete a user by ID.
      security:
        - APIKeyHeader: []
      tags:
        - User
      parameters:
        - in: path
          name: user_id
          required: true
          schema:
            type: integer
            minimum: 1
            description: The user ID.
      responses:
        '200':
          description: User successfully deleted
        '400':
          description: User not found
        '401':
          description: Permission denied
  """
  post = userModel.get_one_profile(user_id)
  if not post:
    return custom_response({'error': 'user not found'}, 400)
  data = user_schema.dump(post)
  
  if data.get('owner_id') != g.user.get('id'):
    if g.user.get('role') != "Admin":
      return custom_response({'error': 'permission denied'}, 401)

  data['deleted_at']= datetime.datetime.utcnow()
  post.update(data)
  #post.delete()
  return custom_response({'message': 'deleted'}, 200)




@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
  """
  Get me
  ---
  /v1/api/users/me:
    get:
      summary: Return your user data.
      security:
        - APIKeyHeader: []
      tags:
        - User
      responses:
        '200':
          description: An Access Token API to be used in Boleto Viewer
        '400':
          description: user in post not found
  """
  user = UserModel.get_one_user(g.user.get('id'))
  ser_user = user_schema.dump(user)
  return custom_response(ser_user, 200)








@user_api.route('/login', methods=['POST'])
def login():
  """
  User Login Function

  /v1/api/users/login:
    post:
      summary: 'User Login Function In API, return a token API.'
      tags:
        - User
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                password:
                  type: string
      responses:
        '200':
          description: An Access Token API to be used in Boleto Viewer
        '400':
          description: Error in request
        '401':
          description: Missing data
        '402':
          description: Missing credentiais
        '403':
          description: Email are not valid
        '404':
          description: Password are not valid
  """
  try:
    req_data = request.get_json() 
  except:
    return custom_response({'erro': 'Not request'}, 400) 

  try:
    data = user_schema.load(req_data, partial=True)
  except Exception as error:
    return custom_response(str(error), 401)

  if not data.get('email') or not data.get('password'):
    return custom_response({'error': 'you need email and password to sign in'}, 402)
 
  user = UserModel.get_user_by_email(data.get('email'))
  if not user:
    return custom_response({'error': 'invalid email'}, 403)


  if not user.check_hash(data.get('password')):
    return custom_response({'error': 'invalid password'}, 404)

  ser_data = user_schema.dump(user)
  token = Auth.generate_token(ser_data.get('id'))
  return custom_response({'jwt_token': token}, 200)

  



def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
