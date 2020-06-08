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
from ..models.EntityAppModel import EntityAppModel, EntityAppSchema
from ..models.UserModel import UserModel, UserSchema

entityApp_api = Blueprint('entityApp_api', __name__)
entityApp_schema = EntityAppSchema()
UserSchema = UserSchema()







@entityApp_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create App Function
  ---
  /v1/api/entityApps/:
    post:
      summary: Create entityapps Function.
      security:
        - APIKeyHeader: []
      tags:
        - App
      requestBody:
        description: entityapps Functions
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - entity_id
                - app_id
              properties:
                entity_id:
                  type: integer
                app_id:
                  type: integer
                deleted_app:
                  type: integer
                created_app:
                  type: integer
                modified_app:
                  type: integer
      responses:
        '200':
          description: Entityapps successfully registered
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
    data= entityApp_schema.load(req_data)
  except Exception as error:
    return custom_response(str(error), 401)

  post = EntityAppModel(data)
  post.save()
  data = entityApp_schema.dump(post)
  return custom_response(data, 200)








@entityApp_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
  """
  Get All Apps
  --- 
  /v1/api/entityApps/:
    get:
      summary: Get all entityApps Function
      security:
        - APIKeyHeader: []
      tags:
        - Profesion
      
      responses:
        '200':
          description: Returns all entityApps
        '400':
          description: Entityapps not found
        '401':
          description: Permission denied
  """
  post_user= UserModel.get_one_user(g.user.get('id'))
  if not post_user:
    return custom_response({'error': 'Entityapps not found'}, 400)
  data_user= UserSchema.dump(post_user)

  if data_user.get('role') != 'Admin':
    return custom_response({'error': 'permission denied'}, 401)

  posts = EntityAppModel.get_all_entityApps()
  data = entityApp_schema.dump(posts, many=True)
  return custom_response(data, 200)








@entityApp_api.route('/<int:entityApp_id>', methods=['GET'])
@Auth.auth_required
def get_one(entityApp_id):
  """
  Get A App
  ---
  /v1/api/entityApps/{entityApp_id}:
    get:
      summary: Gets a entityapps by ID.
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
            description: The entityapps ID.

      responses:
        '200':
          description: Data this entityapps successfully
        '400':
          description: Entityapps not found
        '401':
          description: Permission denied
  """
  post = EntityAppModel.get_one_entityApp(entityApp_id)
  if not post:
    return custom_response({'error': 'post not found'}, 404)
  data = entityApp_schema.dump(post)

  if g.user.get('id') != data.get('owner_id'):
    return custom_response({'error': 'permission denied'}, 401)

  return custom_response(data, 200)








@entityApp_api.route('/<int:entityApp_id>', methods=['PUT'])
@Auth.auth_required
def update(entityApp_id):
  """
  Update A App
  ---
  /v1/api/entityApps/{entityApp_id}:
    put:
      summary: Update A entityApps.
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
            description: The entityapps ID.
      requestBody:
        description: App Functions
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - entity_id
                - app_id
              properties:
                entity_id:
                  type: integer
                app_id:
                  type: integer
                deleted_app:
                  type: integer
                created_app:
                  type: integer
                modified_app:
                  type: integer
      responses:
        '200':
          description: Entityapps successfully update
        '400':
          description: Error in request
        '401':
          description: Entityapps not found
        '402':
          description: Permission denied
        '403':
          description: Missing data
  """
  try:
    req_data = request.get_json()
  except:
    return custom_response({'error': 'Not request'}, 400)

  post = EntityAppModel.get_one_entityApp(entityApp_id)
  if not post:
    return custom_response({'error': 'entityapps not found'}, 401)
  data = entityApp_schema.dump(post)

  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission denied'}, 402)
  
  try:
    data= entityApp_schema.load(req_data, partial=True)
  except Exception as error:
    return custom_response(str(error), 403)
  post.update(data)
  
  data = entityApp_schema.dump(post)
  return custom_response(data, 200)










@entityApp_api.route('/<int:entityApp_id>', methods=['DELETE'])
@Auth.auth_required
def delete(entityApp_id):
  """
  Delete A App
  ---
  /v1/api/entityApps/{entityApp_id}:
    delete:
      summary: Delete a entityapps by ID.
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
            description: The entityapps ID.
      responses:
        '200':
          description: Entityapps successfully deleted
        '400':
          description: Entityapps not found
        '401':
          description: Permission denied
  """
  post = EntityAppModel.get_one_entityApp(entityApp_id)
  if not post:
    return custom_response({'error': 'entityapps not found'}, 400)
  data = entityApp_schema.dump(post)
  
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

