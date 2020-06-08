# -*- coding: utf-8 -*-
# src / app.py
"""
                      User Service API
    ------------------------------------------------------------------------
                        Create app
    ------------------------------------------------------------------------
    

"""

from flask import Flask, render_template

from flask_cors import CORS

from .config import app_config
from .models import db, bcrypt

from .views.UserView import user_api as user_blueprint
from .views.EntityView import entity_api as entity_blueprint
from .views.AddressView import address_api as address_blueprint
from .views.ProfileView import profile_api as profile_blueprint
from .views.AppView import app_api as app_blueprint
from .views.EntityAppView import entityApp_api as entityApp_blueprint

from flask_swagger_ui import get_swaggerui_blueprint


def create_app(env_name):
  """
    param: env_name 

    DOC API USING SWAGGER UI  
    Create app
  """
  
  # app initiliazation
  APP = Flask(__name__)

  CORS(APP)

  APP.config.from_object(app_config[env_name])

  # initializing bcrypt and db
  bcrypt.init_app(APP)
  db.init_app(APP)

  ### swagger specific ###
  SWAGGER_URL = '/apidocs'
  API_URL = '/static/api/api.yml'
  SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "User Service Database API"
    }
  )
  APP.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
  ### end swagger specific ###


  APP.register_blueprint(user_blueprint, url_prefix='/v1/api/users')
  APP.register_blueprint(entity_blueprint, url_prefix='/v1/api/entities')
  APP.register_blueprint(address_blueprint, url_prefix='/v1/api/addresss')
  APP.register_blueprint(profile_blueprint, url_prefix='/v1/api/profiles')
  APP.register_blueprint(app_blueprint, url_prefix='/v1/api/apps')
  APP.register_blueprint(entityApp_blueprint, url_prefix='/v1/api/entityApps')



  @APP.route('/', methods=['GET'])
  def index():
    """
    Home
    """
    return render_template('index.html')

  return APP