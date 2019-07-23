from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models import UserModel, RevokedTokenModel
from flask import jsonify, request, send_file, send_from_directory
import datetime
from run import db
import os
import werkzeug
from werkzeug.utils import secure_filename

from run import app
parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('picture', type=werkzeug.datastructures.FileStorage)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()
        if not data['username'] or not data['password']:
            return {'message': 'thiếu thông tin'}
        if UserModel.find_by_username(data['username']):
            return {'message': 'User {} already exists'. format(data['username'])}

        new_user = UserModel(
            username=data['username'],
            password=UserModel.generate_hash(data['password']))
        try:
            new_user.save_to_db()
            return {
                'expires': str(datetime.timedelta(hours=24)),
                'message': 'User {} was created'.format(data['username']),
            }
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        if not data['username'] or not data['password']:
            return {'message': 'thiếu thông tin'}

        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User không tồn tại'}, 500

        if UserModel.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'], expires_delta=datetime.timedelta(hours=24))
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': 'Sai mạt khẩu'}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, expires_delta=datetime.timedelta(hours=24))
        return {'access_token': access_token}


class UploadImage(Resource):
    @jwt_required
    def post(self):
        ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
        a = 0
        try:
            file_list = request.files.getlist("file")
        except:
            return jsonify({"message": "không get được file"})
        for image in file_list:
            filename = image.filename
            print(filename)
            if filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                print('a')
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename)))
            else:
                a = 1
                pass
        if a == 0:
            return jsonify({"message": "lưu thành công"})
        else:
            return jsonify({"message": "1 trong các file của bạn không phải file ảnh"})

    @jwt_required
    def get(self, name):
        print(1)
        print(name)
        try:
            print(2)
            index_path = os.path.join(app.config['UPLOAD_FOLDER'], name)
            print(index_path)
        except:
            return jsonify({'message': 'Lỗi rồi'})
        return send_file(index_path)


class Excel(Resource):
    @jwt_required
    def post(self):
        ALLOWED_EXTENSIONS = set(['xlsx', 'xlsm', 'xlsb', 'xltx', 'xltm', 'xls',
                                  'xlt', 'xls', 'xml', 'xlam', 'xla', 'xlw', 'xlr', 'csv', 'mpp'])
        a = 0
        try:
            file_list = request.files.getlist("excel")
            print(file_list)
        except:
            return jsonify({"message": "không get được file"})
        for excel in file_list:
            print(excel)
            filename = excel.filename
            print(filename)
            if filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
                print('a')
                excel.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename)))
            else:
                a = 1
                pass
        if a == 0:
            return jsonify({"message": "lưu thành công"})
        else:
            return jsonify({"message": "1 trong các file của bạn không phải file excel"})

    @jwt_required
    def get(self, name):
        return send_from_directory(app.config['UPLOAD_FOLDER'], name)
