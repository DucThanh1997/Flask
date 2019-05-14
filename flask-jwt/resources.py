from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from models import UserModel, RevokedTokenModel, TaskModel
from flask import jsonify
import datetime
from run import db

parser = reqparse.RequestParser()
parser.add_argument('username')
parser.add_argument('password')
parser.add_argument('name')
parser.add_argument('description')
parser.add_argument('status')


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


class Tasks(Resource):
    # @jwt_required
    def get(self, id=None):
        if not id:
            try:
                Task_inf = TaskModel.return_all()
                Task_list = Task_inf['task_list']
                length = Task_inf['task_len']
            except:
                return jsonify({'message': 'lỗi'}), 500
            return jsonify({'length': length, 'data': Task_list})
        else:
            try:
                data = TaskModel.query.get(id)
                Task = {
                'name': data.name,
                'description': data.description,
                'status': data.status}
            except:
                return jsonify({'message': 'lỗi'}), 500
            return jsonify({'data': Task})

    @jwt_required
    def post(self):
        data = parser.parse_args()
        if not data['name'] or not data['description'] or not data['status']:
            return jsonify({'message': 'thiếu thông tin'})
        new_task = TaskModel(
            name=data['name'],
            description=data['description'],
            status=data['status'])

        try:
            TaskModel.save_to_db(new_task)
        except:
            return jsonify({'message': 'fail'}), 500
        return {'message': 'Task {} was created'.format(data['name'])}

    @jwt_required
    def put(self, id):
        data = parser.parse_args()
        if not data['name'] or not data['description'] or not data['status']:
            return jsonify({'message': 'thiếu thông tin'})
        try:
            Task = TaskModel.query.get(id)
            Task.name = data['name']
            Task.description = data['description']
            Task.status = data['status']
            db.session.commit()
        except:
            return jsonify({'message': 'fail'}), 500
        return jsonify({'message': 'Task {} was updated'.format(data['name'])})


    @jwt_required
    def delete(self, id):
        try:
            TaskModel.query.filter_by(id=id).delete()
            db.session.commit()
        except:
            return jsonify({'message': 'fail'}), 500
        return jsonify({'message': 'xóa task thành công'})


