# -*- coding: utf-8 -*-
# src/models/UserModel.py
"""
                        User Service
    ------------------------------------------------------------------------
                        User Model
    ------------------------------------------------------------------------
    

"""

from marshmallow import fields, Schema
import datetime
from . import db, bcrypt
from .EntityModel import EntitySchema

class UserModel(db.Model):
  """
  User Model
  """

  # table name
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  email = db.Column(db.String(50), unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=False)
  role = db.Column(db.String(30), nullable=False)
  active = db.Column(db.Boolean, nullable=True)
  deleted_at = db.Column(db.DateTime, nullable=True)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  deleted_app = db.Column(db.Integer, nullable=True)
  created_app = db.Column(db.Integer, nullable=True)
  modified_app = db.Column(db.Integer, nullable=True)
  entities = db.relationship('EntityModel', backref='entities', lazy=True)
 


  def __init__(self, data):
    """
    Class constructor
    """
    self.name = data.get('name')
    self.email = data.get('email')
    self.password = self.__generate_hash(data.get('password'))
    self.role = data.get('role')
    self.active = data.get('active')
    self.deleted_at = data.get('deleted_at')
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()
    self.deleted_app = data.get("deleted_app")
    self.created_app = data.get("created_app")
    self.modified_app = data.get("modified_app")


  def save(self):
    db.session.add(self)
    db.session.commit()
  
 
  def update(self, data):
    for key, item in data.items():
      if key == 'password':
        self.password = self.__generate_hash(item)
      setattr(self, key, item)
    self.modified_at = datetime.datetime.utcnow()
    db.session.commit()
  
  def delete(self):
    db.session.delete(self)
    db.session.commit()
  
  @staticmethod
  def get_all_users(): 
    return UserModel.query.all()

  @staticmethod
  def get_one_user(id): 
    return UserModel.query.filter_by(id=id, deleted_at=None).first()
  
  @staticmethod
  def get_user_by_email(value):
    return UserModel.query.filter_by(email=value, deleted_at=None).first()
  

  def __generate_hash(self, password):
    return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")
  
  def check_hash(self, password):
    return bcrypt.check_password_hash(self.password, password)

  def __repr(self):
    return '<id {}>'.format(self.id)

class UserSchema(Schema):
  id = fields.Int(dump_only=True)
  name = fields.Str(required=True)
  email = fields.Email(required=True)
  password = fields.Str(required=True, load_only=True)
  active = fields.Boolean(required= True)
  role = fields.Str(required=True)
  deleted_at= fields.DateTime(required=False)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  deleted_app= fields.Int(required=False)
  created_app = fields.Int(required=False)
  modified_app = fields.Int(required=False)
  entities = fields.Nested(EntitySchema, many=True)
 