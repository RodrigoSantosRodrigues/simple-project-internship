# -*- coding: utf-8 -*-
# encoding: utf-8
# /run.py
"""
                          User Service API
    ------------------------------------------------------------------------
                         Initialize server
    ------------------------------------------------------------------------
    
"""
import os
from dotenv import load_dotenv, find_dotenv

from src.app import create_app

load_dotenv(find_dotenv(filename='.env'))

app = create_app(os.getenv('FLASK_ENV'))

if __name__ == '__main__':
  port = os.getenv('APP_PORT')
  host = os.getenv('APP_HOST')
  # run app
 
  app.run(host=host, port=port)
