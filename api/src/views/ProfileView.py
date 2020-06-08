# -*- coding: utf-8 -*-
#/src/views/ProfileView.py

"""
                        User Service Api
    ------------------------------------------------------------------------
                        API do Profile
    ------------------------------------------------------------------------
    

"""
import datetime
from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.ProfileModel import ProfileModel, ProfileSchema
from ..models.EntityModel import EntityModel, EntitySchema
from ..models.UserModel import UserModel, UserSchema

profile_api = Blueprint('profile_api', __name__)
profile_schema = ProfileSchema()
entity_schema= EntitySchema()
user_schema = UserSchema()


@profile_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
  """
  Create Profile Function
  ---
  /v1/api/profiles/:
    post:
      summary: Create Profile Function.
      security:
        - APIKeyHeader: []
      tags:
        - Profile
      requestBody:
        description: Profile Functions
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - career
                - birthDate
                - sex
                - telephone
              properties:
                career:
                  type: string
                birthDate:
                  type: string
                sex:
                  type: string
                telephone:
                  type: string
                married:
                  type: boolean
                cpf:
                  type: integer
                rg:
                  type: integer
                deleted_app:
                  type: integer
                created_app:
                  type: integer
                modified_app:
                  type: integer
                  
      responses:
        '200':
          description: Profile successfully registered
        '400':
          description: Error in request
        '401':
          description: Account in post not found
        '402':
          description: Missing data

  """
  try:
    req_data = request.get_json()
  except Exception as error:
    return custom_response({'error': 'not request:'+str(error)}, 400 )
  
  req_data['owner_id'] = g.user.get('id')

  post_entity= EntityModel.get_entity_by_user(g.user.get('id'))
  if not post_entity:
    return custom_response({'error': 'account in post not found'}, 401)
  data_entity = entity_schema.dump(post_entity)

  req_data['entity_id']= data_entity['id']

  try:
    data = profile_schema.load(req_data)
  except Exception as error:
    return custom_response(str(error), 402)

  post = ProfileModel(data)
  post.save()
  data = profile_schema.dump(post)
  return custom_response(data, 200)







@profile_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
  """
  Get All Profiles
  --- 
  /v1/api/profiles/:
    get:
      summary: Get all profiles Function
      security:
        - APIKeyHeader: []
      tags:
        - Profile
      
      responses:
        '200':
          description: Returns all profiles
        '400':
          description: Profile not found
        '401':
          description: Permission denied
  """
  post_user= UserModel.get_one_user(g.user.get('id'))
  if not post_user:
    return custom_response({'error': 'profiles not found'}, 400)
  data_user= user_schema.dump(post_user)

  if data_user.get('role') != 'Admin':
    return custom_response({'error': 'permission denied'}, 401)

  posts = ProfileModel.get_all_profiles()
  data = profile_schema.dump(posts, many=True)
  return custom_response(data, 200)







@profile_api.route('/<int:profile_id>', methods=['GET'])
@Auth.auth_required
def get_one(profile_id):
  """
  Get A Profile
  ---
  /v1/api/profiles/{profile_id}:
    get:
      summary: Gets a profile by ID.
      security:
        - APIKeyHeader: []
      tags:
        - Profile
      parameters:
        - in: path
          name: profile_id
          required: true
          schema:
            type: integer
            minimum: 1
            description: The profile ID.

      responses:
        '200':
          description: Data this profile successfully
        '400':
          description: Profile not found
        '401':
          description: Permission denied
  """
  post = ProfileModel.get_one_profile(profile_id)
  if not post:
    return custom_response({'error': 'post not found'}, 400)
  data = profile_schema.dump(post)

  if g.user.get('id') != data.get('owner_id'):
    return custom_response({'error': 'permission denied'}, 401)

  return custom_response(data, 200)







@profile_api.route('/<int:profile_id>', methods=['PUT'])
@Auth.auth_required
def update(profile_id):
  """
  Update A Profile
  ---
  /v1/api/profiles/{profile_id}:
    put:
      summary: Update A Profile.
      security:
        - APIKeyHeader: []
      tags:
        - Profile
      parameters:
        - in: path
          name: profile_id
          required: true
          schema:
            type: integer
            minimum: 1
            description: The user ID.
      requestBody:
        description: Profile Functions
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - career
                - birthDate
                - sex
                - telephone
              properties:
                career:
                  type: string
                birthDate:
                  type: string
                sex:
                  type: string
                telephone:
                  type: string
                married:
                  type: boolean
                cpf:
                  type: integer
                rg:
                  type: integer
                deleted_app:
                  type: integer
                created_app:
                  type: integer
                modified_app:
                  type: integer
      responses:
        '200':
          description: Profile successfully update
        '400':
          description: Error in request
        '401':
          description: Not found
        '402':
          description: Permission denied
        '403':
          description: Missing data
  """
  try:
    req_data = request.get_json()
  except:
    return custom_response({'error': 'not request'}, 400)

  post = ProfileModel.get_one_profile(profile_id)
  if not post:
    return custom_response({'error': 'profile not found'}, 401)
  data = profile_schema.dump(post)
  if data.get('owner_id') != g.user.get('id'):
    return custom_response({'error': 'permission denied'}, 402)
  
  try:
    data = profile_schema.load(req_data, partial=True)
  except Exception as error:
    return custom_response(str(error), 403)

  post.update(data)
  
  data = profile_schema.dump(post)
  return custom_response(data, 200)







@profile_api.route('/<int:profile_id>', methods=['DELETE'])
@Auth.auth_required
def delete(profile_id):
  """
  Delete A Profile
  ---
  /v1/api/profiles/{profile_id}:
    delete:
      summary: Delete a profile by ID.
      security:
        - APIKeyHeader: []
      tags:
        - Profile
      parameters:
        - in: path
          name: profile_id
          required: true
          schema:
            type: integer
            minimum: 1
            description: The profile ID.
      responses:
        '200':
          description: Profile successfully deleted
        '400':
          description: Profile not found
        '401':
          description: Permission denied
  """
  post = ProfileModel.get_one_profile(profile_id)
  if not post:
    return custom_response({'error': 'profile not found'}, 400)
  data = profile_schema.dump(post)
  
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

