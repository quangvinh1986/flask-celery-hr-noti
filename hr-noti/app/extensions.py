# -*- coding: utf-8 -*-
from webargs.flaskparser import FlaskParser
from flask_sqlalchemy import SQLAlchemy
from flask_restplus_patched import Api
# from app.sys_libs.flask_restplus_patched import Api
from flask_cors import CORS
from app.sys_libs.flask_walrus import WalrusDatabase

db = SQLAlchemy()
parser = FlaskParser()
cors = CORS()
redis_db = WalrusDatabase()

api = Api(version='1.0', title='Our Application', description="This is our website")
