# -*- coding: utf-8 -*-
# src/models/EntityModel.py
"""
                            User Service
    ------------------------------------------------------------------------
                        Entity Model
    ------------------------------------------------------------------------
    

    
"""

from marshmallow import fields, Schema
import datetime
from . import db, bcrypt
from .AddressModel import AddressSchema
from .ProfileModel import ProfileSchema

class EntityModel(db.Model):
  """
  User Entity
  """

  # table name
  __tablename__ = 'entities'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  document = db.Column(db.String(50), nullable=False, unique=True)
  image= db.Column(db.Text, nullable=True)
  deleted_at = db.Column(db.DateTime, nullable=True)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  deleted_app = db.Column(db.Integer, nullable=True)
  created_app = db.Column(db.Integer, nullable=True)
  modified_app = db.Column(db.Integer, nullable=True)
  owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
  address = db.relationship('AddressModel', backref='adresss', lazy=True)
  Profile = db.relationship('ProfileModel', backref='profiles', lazy=True)

  def __init__(self, data):
    """
    Class constructor
    """
    self.name= data.get('name')
    self.document= data.get('document')
    self.image= data.get('image')
    self.owner_id= data.get('owner_id')
    self.deleted_at = data.get('deleted_at')
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()
    self.deleted_app = data.get('deleted_app')
    self.created_app = data.get('created_app')
    self.modified_app = data.get('modified_app')


  def save(self):
    db.session.add(self)
    db.session.commit()

 
  def update(self, data):
    for key, item in data.items():
      setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  @staticmethod
  def get_all_Entities(): 
    return EntityModel.query.all()
  
  @staticmethod
  def get_one_entity(id): 
    return EntityModel.query.filter_by(id=id, deleted_at=None).first()
  
  @staticmethod
  def get_entity_by_user(owner_id):
    return EntityModel.query.filter_by(owner_id=owner_id, deleted_at=None).first()
  
  @staticmethod
  def get_entity_by_documento(document):
    return EntityModel.query.filter_by(document=document, deleted_at=None).first()


  def __repr(self):
    return '<id {}>'.format(self.id)




class EntitySchema(Schema):
  id = fields.Int(dump_only=True)
  name= fields.Str(required=True)
  document= fields.Str(required=True)
  image= fields.Str(required=False)
  deleted_at= fields.DateTime(required=False)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  deleted_app = fields.Int(required=False)
  created_app = fields.Int(required=False)
  modified_app = fields.Int(required=False)
  owner_id = fields.Int(required=True)
  #address = fields.Nested(AddressSchema, many=True)
  #profile = fields.Nested(ProfileSchema, many=True)
  
