# -*- coding: utf-8 -*-
# src/models/EntityAppModel.py
"""
                        User Service
    ------------------------------------------------------------------------
                        Entity App Model
    ------------------------------------------------------------------------
    
    
"""

from marshmallow import fields, Schema
import datetime
from . import db, bcrypt


class EntityAppModel(db.Model):
  """
  Apps Entity Model

  """

  # table name
  __tablename__ = 'entityApps'

  id = db.Column(db.Integer, primary_key=True)
  deleted_at = db.Column(db.DateTime, nullable=True)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  deleted_app = db.Column(db.Integer, nullable=True)
  created_app = db.Column(db.Integer, nullable=True)
  modified_app = db.Column(db.Integer, nullable=True)
  owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  entity_id = db.Column(db.Integer, db.ForeignKey('entities.id'), nullable=False)
  app_id = db.Column(db.Integer, db.ForeignKey('apps.id'), nullable=False)
  
 

  def __init__(self, data):
    """
    Class constructor
    """
    self.entity_id= data.get('entity_id')
    self.app_id= data.get('app_id')
    self.owner_id= data.get('owner_id')
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
  def get_all_entityApps(): 
    return EntityAppModel.query.all()
  
  @staticmethod
  def get_one_entityApp(id): 
    return EntityAppModel.query.filter_by(id=id, deleted_at=None).first()
    
  

  def __repr(self):
    return '<id {}>'.format(self.id)





class EntityAppSchema(Schema):
  id = fields.Int(dump_only=True)
  deleted_at= fields.DateTime(required=False)
  created_at = fields.DateTime(dump_only=True)
  modified_at = fields.DateTime(dump_only=True)
  deleted_app = fields.Int(required=False)
  created_app = fields.Int(required=False)
  modified_app = fields.Int(required=False)
  owner_id = fields.Int(required=True)
  entity_id= fields.Int(required= True)
  app_id= fields.Int(required=True)
  