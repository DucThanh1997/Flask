from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
import os

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:thanh1997@127.0.0.1/api2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'đố em biết anh đang nghĩ gì'
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['TESTING'] = True
db = SQLAlchemy(app)

# config folder để upload
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
Folder = os.path.join(APP_ROOT, '{}'.format('image'))
if not os.path.isdir(Folder):
    os.mkdir(Folder)

# các đuôi file cho phép
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = Folder


@app.before_first_request
def create_tables():
    db.create_all()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


logging.basicConfig(filename='error.log', level=logging.DEBUG)


import models
import resources

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.UploadImage, '/image', '/image/<string:name>')
api.add_resource(resources.Excel, '/excel', '/excel/<string:name>')
