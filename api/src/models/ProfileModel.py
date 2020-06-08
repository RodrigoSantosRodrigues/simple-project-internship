# -*- coding: utf-8 -*-
# src/models/ProfileModel.py
"""
                              User Service 
    ------------------------------------------------------------------------
                        Profile Model
    ------------------------------------------------------------------------
    

    
"""

from marshmallow import fields, Schema
import datetime
from . import db, bcrypt

class ProfileModel(db.Model):
  """
  User Profile

  """

  # table name
  __tablename__ = 'profiles'

  id = db.Column(db.Integer, primary_key=True)
  career = db.Column(db.String(128), nullable=False)
  birthDate = db.Column(db.Date, nullable=False)
  sex = db.Column(db.String(20), nullable=False)
  telephone = db.Column(db.String(50), nullable=False)
  married = db.Column(db.Boolean, nullable=True)
  cpf = db.Column(db.Integer, nullable=True)
  rg= db.Column(db.Integer, nullable=True)
  deleted_at = db.Column(db.DateTime, nullable=True)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  deleted_app = db.Column(db.Integer, nullable=True)
  created_app = db.Column(db.Integer, nullable=True)
  modified_app = db.Column(db.Integer, nullable=True)
  owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  entity_id = db.Column(db.Integer, db.ForeignKey('entities.id'), nullable=False)
 

 
  def __init__(self, data):
    """
    Class constructor
    """
    self.career= data.get('career')
    self.birthDate= data.get('birthDate')
    self.sex = data.get('sex')
    self.telephone= data.get('telephone')
    self.married= data.get('married')
    self.cpf= data.get('cpf')
    self.rg= data.get('rg')
    self.owner_id= data.get('owner_id')
    self.entity_id= data.get('entity_id')
    self.deleted_at = data.get('deleted_at')
    self.deleted_app = data.get('deleted_app')
    self.created_app = data.get('created_app')
    self.modified_app = data.get('modified_app')
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()

 
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
  def get_all_profiles():
    return ProfileModel.query.all()
  
  @staticmethod
  def get_one_profile(id): 
    return ProfileModel.query.filter_by(id=id, deleted_at=None).first()
    

  
 
  def __repr(self):
    return '<id {}>'.format(self.id)





class ProfileSchema(Schema):
  id = fields.Int(dump_only=True)
  career= fields.Str(required= True)
  birthDate= fields.Date(required=True)
  sex = fields.Str(required= True)
  telephone= fields.Str(required= True)
  married= fields.Boolean(required= True)
  cpf= fields.Integer(required= True)
  rg= fields.Integer(required= True)
  deleted_at= fields.DateTime(required=False)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  deleted_app = fields.Int(required=False)
  created_app = fields.Int(required=False)
  modified_app = fields.Int(required=False)
  owner_id = fields.Int(required=True)
  entity_id= fields.Int(required=True)
 