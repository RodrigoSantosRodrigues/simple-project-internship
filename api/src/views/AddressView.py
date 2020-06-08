# -*- coding: utf-8 -*-
#/src/views/AddressView.py

"""
                        User Service
    ------------------------------------------------------------------------
                        API do Address
    ------------------------------------------------------------------------
    

  
"""
import datetime
from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.AddressModel import AddressModel, AddressSchema
from ..models.EntityModel import EntityModel, EntitySchema
from ..models.UserModel import UserModel, UserSchema

address_api = Blueprint('address_api', __name__)
address_schema = AddressSchema()
entity_schema= EntitySchema()
user_schema = UserSchema()




@address_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create Address Function
  ---
  /v1/api/addresss/:
    post:
      summary: Create Adress Function.
      security:
        - APIKeyHeader: []
      tags:
        - Address
      requestBody:
        description: Adress Functions
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - street
                - city
                - zipCode
                - state
                - number
              properties:
                street:
                  type: string
                city:
                  type: integer
                zipCode:
                  type: integer
                state:
                  type: string
                number:
                  type: integer
                deleted_app:
                  type: integer
                created_app:
                  type: integer
                modified_app:
                  type: integer
      responses:
        '200':
          description: Address successfully registered
        '400':
          description: Error in request
        '401':
          description: Entity Error
        '402':
          description: Missing data
 
  """
  try:
    req_data = request.get_json()
  except:
    return custom_response({'error': 'Not request'}, 400)

  req_data['owner_id'] = g.user.get('id')

  post_entity= EntityModel.get_entity_by_user(g.user.get('id'))
  if not post_entity:
    return custom_response({'error': 'there is no entity for this user'}, 401)
  data_entity = entity_schema.dump(post_entity)

  req_data['entity_id']= data_entity['id']

  try:
    data= address_schema.load(req_data)
  except Exception as error:
    return custom_response(str(error), 402)

  post = AddressModel(data)
  post.save()
  data = address_schema.dump(post)
  return custom_response(data, 200)









@address_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
  """
  Get All Addresss
  --- 
  /v1/api/addresss/:
    get:
      summary: Get all address Function
      security:
        - APIKeyHeader: []
      tags:
        - Address
      
      responses:
        '200':
          description: Returns all address
        '400':
          description: Address not found
        '401':
          description: Permission denied
  """
  
  post_user= UserModel.get_one_user(g.user.get('id'))
  if not post_user:
    return custom_response({'error': 'address not found'}, 400)
  data_user= user_schema.dump(post_user)

  if data_user.get('role') != 'Admin':
    return custom_response({'error': 'permission denied'}, 401)

  posts = AddressModel.get_all_addresss()
  data = address_schema.dump(posts, many=True)
  return custom_response(data, 200)







@address_api.route('/<int:address_id>', methods=['GET'])
@Auth.auth_required
def get_one(address_id):
  """
  Get A Address
  ---
  /v1/api/addresss/{address_id}:
    get:
      summary: Gets a address by ID.
      security:
        - APIKeyHeader: []
      tags:
        - Address
      parameters:
        - in: path
          name: address_id
          required: true
          schema:
            type: integer
            minimum: 1
            description: The address ID.

      responses:
        '200':
          description: Data this address successfully
        '400':
          description: Address not found
        '401':
          description: Permission denied
  """
  post = AddressModel.get_one_address(address_id)
  if not post:
    return custom_response({'error': 'post not found'}, 400)
  data = address_schema.dump(post)
  
  if g.user.get('id') != data.get('owner_id'):
    return custom_response({'error': 'permission denied'}, 401)
  
  return custom_response(data, 200)








@address_api.route('/<int:address_id>', methods=['PUT'])
@Auth.auth_required
def update(address_id):
  """
  Update A Address
  ---
  /v1/api/addresss/{address_id}:
    put:
      summary: Update A Address.
      security:
        - APIKeyHeader: []
      tags:
        - Address
      parameters:
        - in: path
          name: address_id
          required: true
          schema:
            type: integer
            minimum: 1
            description: The Address ID.
      requestBody:
        description: Adress Functions
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - street
                - city
                - zipCode
                - state
                - number
              properties:
                street:
                  type: string
                city:
                  type: integer
                zipCode:
                  type: integer
                state:
                  type: string
                number:
                  type: integer
                deleted_app:
                  type: integer
                created_app:
                  type: integer
                modified_app:
                  type: integer
      responses:
        '200':
          description: Address successfully update
        '400':
          description: Error in request
        '401':
          description: Address not found
        '402':
          description: Permission denied
        '403':
          description: Missing data


  """
  try:
    req_data = request.get_json()
  except:
    return custom_response({'error': 'Not request'}, 400)

  post = AddressModel.get_one_address(address_id)
  if not post:
    return custom_response({'error': 'address not found'}, 401)
  data = address_schema.dump(post)

  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission denied'}, 402)
  
  try:
    data= address_schema.load(req_data, partial=True)
  except Exception as error:
    return custom_response(str(error), 404)

  post.update(data)
  data = address_schema.dump(post)
  return custom_response(data, 200)








@address_api.route('/<int:address_id>', methods=['DELETE'])
@Auth.auth_required
def delete(address_id):
  """
  Delete A Address
  ---
  /v1/api/addresss/{address_id}:
    delete:
      summary: Delete a address by ID.
      security:
        - APIKeyHeader: []
      tags:
        - Address
      parameters:
        - in: path
          name: address_id
          required: true
          schema:
            type: integer
            minimum: 1
            description: The address ID.
      responses:
        '200':
          description: Address successfully deleted
        '400':
          description: Address not found
        '401':
          description: Permission denied
  """
  post = AddressModel.get_one_address(address_id)
  if not post:
    return custom_response({'error': 'address not found'}, 400)
  data = address_schema.dump(post)

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

