# -*- coding: utf-8 -*-
# /src/config.py
"""
                              User Service
    ------------------------------------------------------------------------
                        Flask Environment Configuration
    ------------------------------------------------------------------------
    


"""
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(filename="/.env"))

POSTGRES_DEV = {
    'user': os.getenv("DB_USER"),
    'pw': os.getenv("DB_PW"),
    'db': os.getenv("DB_API_DEV"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT") or '5432',
}

POSTGRES_TEST = {
    'user': os.getenv("DB_USER"),
    'pw': os.getenv("DB_PW"),
    'db': os.getenv("DB_API_TEST"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT") or '5432',
}


POSTGRES_PROD = {
    'user': os.getenv("DB_USER"),
    'pw': os.getenv("DB_PW"),
    'db': os.getenv("DB_API"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT") or '5432',
}

class Development(object):
    """
    Development environment configuration
    """
    DEBUG = True
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES_DEV
    #SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class Production(object):
    """
    Production environment configurations
    """
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES_PROD
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

class Testing(object):
    """
    Development environment configuration
    """
    TESTING = True
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES_TEST
    SQLALCHEMY_TRACK_MODIFICATIONS=False

app_config = {
    'development': Development,
    'production': Production,
    'testing': Testing
}
