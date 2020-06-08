#src/models/__init__.py

"""
                    User Service
    ------------------------------------------------------------------------
                        __init__
    ------------------------------------------------------------------------
    
"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# initialize db
db = SQLAlchemy()
bcrypt = Bcrypt()


from .UserModel import UserModel, UserSchema
from .EntityModel import EntityModel, EntitySchema
from .ProfileModel import ProfileModel, ProfileSchema
from .AddressModel import AddressModel, AddressSchema
from .AppModel import AppModel, AppSchema
from .EntityAppModel import EntityAppModel, EntityAppSchema
