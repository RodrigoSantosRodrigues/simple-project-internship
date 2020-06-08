# -*- coding: utf-8 -*-
#/src/views/AppView.py

"""
                        User Service
    ------------------------------------------------------------------------
                        API do App
    ------------------------------------------------------------------------
    

"""
import datetime
from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.AppModel import AppModel, AppSchema
from ..models.UserModel import UserModel, UserSchema

app_api = Blueprint('app_api', __name__)
app_schema = AppSchema()
UserSchema = UserSchema()







@app_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create App Function
  ---
  /v1/api/apps/:
    post:
      summary: Create App Function.
      security:
        - APIKeyHeader: []
      tags:
        - App
      requestBody:
        description: App Functions
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - name
                - description
              properties:
                name:
                  type: string
                description:
                  type: string
                deleted_app:
                  type: integer
                created_app:
                  type: integer
                modified_app:
                  type: integer
      responses:
        '200':
          description: App successfully registered
        '400':
          description: Error in request
        '401':
          description: Missing data
  
  """
  try:
    req_data = request.get_json()
  except:
    return custom_response({'error': 'Not request'}, 400)
  
  req_data['owner_id'] = g.user.get('id')

  try:
    data= app_schema.load(req_data)
  except Exception as error:
    return custom_response(str(error), 401)

  post = AppModel(data)
  post.save()
  data = app_schema.dump(post)
  return custom_response(data, 200)








@app_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
  """
  Get All Apps
  --- 
  /v1/api/apps/:
    get:
      summary: Get all apps Function
      security:
        - APIKeyHeader: []
      tags:
        - Profesion
      
      responses:
        '200':
          description: Returns all apps
        '400':
          description: User not found
        '401':
          description: Permission denied
  """
  post_user= UserModel.get_one_user(g.user.get('id'))
  if not post_user:
    return custom_response({'error': 'user not found'}, 400)
  data_user= UserSchema.dump(post_user)

  if data_user.get('role') != 'Admin':
    return custom_response({'error': 'permission denied'}, 401)

  posts = AppModel.get_all_apps()
  data = app_schema.dump(posts, many=True)
  return custom_response(data, 200)








@app_api.route('/<int:app_id>', methods=['GET'])
@Auth.auth_required
def get_one(app_id):
  """
  Get A App
  ---
  /v1/api/apps/{app_id}:
    get:
      summary: Gets a app by ID.
      security:
        - APIKeyHeader: []
      tags:
        - App
      parameters:
        - in: path
          name: app_id
          required: true
          schema:
            type: integer
            minimum: 1
            description: The app ID.

      responses:
        '200':
          description: Data this app successfully
        '400':
          description: user not found
        '401':
          description: Permission denied
  """
  post = AppModel.get_one_app(app_id)
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = app_schema.dump(post)

  if g.user.get('id') != data.get('owner_id'):
    return custom_response({'error': 'permission denied'}, 401)

  return custom_response(data, 200)








@app_api.route('/<int:app_id>', methods=['PUT'])
@Auth.auth_required
def update(app_id):
  """
  Update A App
  ---
  /v1/api/apps/{app_id}:
    put:
      summary: Update A Profesion.
      security:
        - APIKeyHeader: []
      tags:
        - App
      parameters:
        - in: path
          name: app_id
          required: true
          schema:
            type: integer
            minimum: 1
            description: The app ID.
      requestBody:
        description: App Functions
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - name
                - description
              properties:
                name:
                  type: string
                description:
                  type: string
                deleted_app:
                  type: integer
                created_app:
                  type: integer
                modified_app:
                  type: integer
      responses:
        '200':
          description: Profesion successfully update
        '400':
          description: Error in request
        '401':
          description: App not found
        '402':
          description: Permission denied
        '403':
          description: Missing data
  """
  try:
    req_data = request.get_json()
  except:
    return custom_response({'error': 'Not request'}, 400)

  post = AppModel.get_one_app(app_id)
  if not post:
    return custom_response({'error': 'app not found'}, 401)
  data = app_schema.dump(post)

  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission denied'}, 402)
  
  try:
    data= app_schema.load(req_data, partial=True)
  except Exception as error:
    return custom_response(str(error), 403)
  post.update(data)
  
  data = app_schema.dump(post)
  return custom_response(data, 200)










@app_api.route('/<int:app_id>', methods=['DELETE'])
@Auth.auth_required
def delete(app_id):
  """
  Delete A App
  ---
  /v1/api/apps/{app_id}:
    delete:
      summary: Delete a app by ID.
      security:
        - APIKeyHeader: []
      tags:
        - App
      parameters:
        - in: path
          name: app_id
          required: true
          schema:
            type: integer
            minimum: 1
            description: The app ID.
      responses:
        '200':
          description: App successfully deleted
        '400':
          description: App not found
        '401':
          description: Permission denied
  """
  post = AppModel.get_one_app(app_id)
  if not post:
    return custom_response({'error': 'app not found'}, 400)
  data = app_schema.dump(post)
  
  if data.get('owner_id') != g.user.get('id'):
    if g.user.get('role') != "Admin":
      return custom_response({'error': 'permission denied'}, 401)

  data['deleted_at']= datetime.datetime.utcnow()
  post.update(data)
  #post.delete()
  return custom_response({'message': 'deleted'}, 200)


  




def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )

