# -*- coding: utf-8 -*-
#/src/views/EntityView.py

"""
                         User Service
    ------------------------------------------------------------------------
                        API do Entity
    ------------------------------------------------------------------------


"""
import datetime
from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.EntityModel import EntityModel, EntitySchema
from ..models.UserModel import UserModel, UserSchema

entity_api = Blueprint('entity_api', __name__)
entity_schema = EntitySchema()
UserSchema = UserSchema()



@entity_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create Entity Function
   ---
  /v1/api/entities/:
    post:
      summary: Create Profession Function.
      security:
        - APIKeyHeader: []
      tags:
        - Entity
      requestBody:
        description: Entity Functions
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              required:
                - entity
              properties:
                entity:
                  type: object
                  properties:
                    name:
                      type: string
                    document:
                      type: string
                    deleted_app:
                      type: integer
                    created_app:
                      type: integer
                    modified_app:
                      type: integer
                image:
                  type: array
                  items:
                    type: string
                    format: binary          
      responses:
        '200':
          description: Entity successfully registered
        '400':
          description: Error in request
        '401':
          description: Error in request image
        '402':
          description: Missing data
        '403':
          description: Document already exists for this user, please supply another document
        '404':
          description: There is already a registration for this user
  """
  try:
    req_data = json.loads(request.form['entity'])
  except:
    return custom_response({'error': 'Not request'}, 400)
  
  try:
    if request.files:
      req_data['img_request']= request.files['image']
  except:
    return custom_response({'error': 'Not request'}, 401)
      
  req_data['owner_id'] = g.user.get('id')

  try:
    data= entity_schema.load(req_data)
  except Exception as error:
    return custom_response(str(error), 402)
  
  document_in_db = EntityModel.get_entity_by_documento(data.get('document'))
  if document_in_db:
    message = {'error': 'Document already exists for this user, please supply another document'}
    return custom_response(message, 403)
  
  user_in_db = EntityModel.get_entity_by_user(data.get('owner_id'))
  if user_in_db:
    message = {'error': 'There is already a registration for this user'}
    return custom_response(message, 404)

  post = EntityModel(data)
  post.save()
  data = entity_schema.dump(post)
  return custom_response(data, 200)








@entity_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
  """
  Get All Entitys
  --- 
  /v1/api/entities/:
    get:
      summary: Get all entities Function
      security:
        - APIKeyHeader: []
      tags:
        - Entity
      responses:
        '200':
          description: Returns all entities
        '400':
          description: Entity not found
        '401':
          description: Permission denied
  """
  post_user= UserModel.get_one_user(g.user.get('id'))
  if not post_user:
    return custom_response({'error': 'entity not found'}, 400)
  data_user= UserSchema.dump(post_user)
  print(data_user)
  if data_user.get('role') != 'Admin':
    return custom_response({'error': 'permission denied'}, 401)

  posts = EntityModel.get_all_Entities()
  data = entity_schema.dump(posts, many=True)
  return custom_response(data, 200)







@entity_api.route('/<int:entity_id>', methods=['GET'])
@Auth.auth_required
def get_one(entity_id):
  """
  Get A Entity
  ---
  /v1/api/entities/{entity_id}:
    get:
      summary: Gets a entity by ID.
      security:
        - APIKeyHeader: []
      tags:
        - Entity
      parameters:
        - in: path
          name: entity_id
          required: true
          schema:
            type: integer
            minimum: 1
            description: The entity ID.

      responses:
        '200':
          description: Data this entity successfully
        '400':
          description: Entity not found
        '401':
          description: Permission denied
  """
  post = EntityModel.get_one_entity(entity_id)
  if not post:
    return custom_response({'error': 'post not found'}, 400)
  data = entity_schema.dump(post)

  if g.user.get('id') != data.get('owner_id'):
    return custom_response({'error': 'permission denied'}, 401)

  return custom_response(data, 200)








@entity_api.route('/<int:entity_id>', methods=['PUT'])
@Auth.auth_required
def update(entity_id):
  """
  Update A Entity
  ---
  /v1/api/entities/{entity_id}:
    put:
      summary: Update A Entity.
      security:
        - APIKeyHeader: []
      tags:
        - Entity
      parameters:
        - in: path
          name: entity_id
          required: true
          schema:
            type: integer
            minimum: 1
            description: The Entity ID.
      requestBody:
        description: Entity Functions
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              required:
                - entity
              properties:
                entity:
                  type: object
                  properties:
                    name:
                      type: string
                    document:
                      type: string
                    deleted_app:
                      type: integer
                    created_app:
                      type: integer
                    modified_app:
                      type: integer
                image:
                  type: array
                  items:
                    type: string
                    format: binary 
      responses:
        '200':
          description: Entity successfully update
        '400':
          description: Error in request
        '401':
          description: Error in request image
        '402':
          description: Entity not found
        '403':
          description: Permission denied
        '404':
          description: Missing data
        '405':
          description: Document already exists for this user, please supply another document
        '406':
          description: There is already a registration for this user
  """
  try:
    req_data = json.loads(request.form['entity'])
  except:
    return custom_response({'error': 'Not request'}, 400)

  try:
    if request.files:
      req_data['img_request']= request.files['image']
  except:
    return custom_response({'error': 'Not request'}, 401)

  post = EntityModel.get_one_entity(entity_id)
  if not post:
    return custom_response({'error': 'entity not found'}, 402)
  data = entity_schema.dump(post)

  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission denied'}, 403)
  print(req_data)
  try:
    data= entity_schema.load(req_data, partial=True)
  except Exception as error:
    return custom_response(str(error), 404)
  post.update(data)

  document_in_db = EntityModel.get_entity_by_documento(data.get('documento'))
  if document_in_db:
    message = {'error': 'Document already exists for this user, please supply another document'}
    return custom_response(message, 405)
  
  user_in_db = EntityModel.get_entity_by_user(data.get('owner_id'))
  if user_in_db:
    message = {'error': 'There is already a registration for this user'}
    return custom_response(message, 406)
  
  data = entity_schema.dump(post)
  return custom_response(data, 200)









@entity_api.route('/<int:entity_id>', methods=['DELETE'])
@Auth.auth_required
def delete(entity_id):
  """
  Delete A Entity
  ---
  /v1/api/entities/{entity_id}:
    delete:
      summary: Delete a entity by ID.
      security:
        - APIKeyHeader: []
      tags:
        - Entity
      parameters:
        - in: path
          name: entity_id
          required: true
          schema:
            type: integer
            minimum: 1
            description: The entity ID.
      responses:
        '200':
          description: Entity successfully deleted
        '400':
          description: Entity not found
        '401':
          description: Permission denied
  """
  post = EntityModel.get_one_entity(entity_id)
  if not post:
    return custom_response({'error': 'entity not found'}, 400)
  data = entity_schema.dump(post)

  if data.get('owner_id') != g.user.get('id'):
    if g.user.get('role') != "Admin":
      return custom_response({'error': 'permission denied'}, 401)

  data['deleted_at']= datetime.datetime.utcnow()
  print(data)
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

