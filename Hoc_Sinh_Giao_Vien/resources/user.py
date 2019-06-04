from flask_restful import reqparse, Resource
from flask import request, jsonify, send_file
import os
from models.user import UserModel
from werkzeug.utils import secure_filename
from config import Config


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "ma",
        type=str,
        required=True,
        help="Không được bỏ trống mã người dùng ",
    )
    parser.add_argument(
        "username",
        type=str,
        required=False,
        help="Không được bỏ trống tên người dùng ",
    )
    parser.add_argument(
        "password",
        type=str,
        required=False,
        help="Không được bỏ trống mật khẩu ",
    )
    parser.add_argument("password", type=str, required=False)
    parser.add_argument("username", type=str, required=False)
    parser.add_argument("ho_ten", type=str, required=False)
    parser.add_argument("ngay_sinh", type=str, required=False)
    parser.add_argument("so_dien_thoai", type=str, required=False)
    parser.add_argument("gioi_tinh", type=str, required=False)
    parser.add_argument("dia_chi", type=str, required=False)
    parser.add_argument("que_quan", type=str, required=False)
    parser.add_argument("email", type=str, required=False)
    parser.add_argument("avatar", type=str, required=False)
    parser.add_argument("image_name", type=str, required=False)
    parser.add_argument("chuc_vu", type=int, required=False)

    def post(self):
        data = User.parser.parse_args()
        print(data["ma"])
        if UserModel.find_by_ma(data["ma"]):
            return {"messages": "người dùng này đã tồn tại"}
        user = UserModel(**data)
        try:
            user.save_to_db()
        except TypeError:
            return {"messages": "Sai về mặt thông tin"}, 500
        except:
            return {"messages": "không lưu được người dùng"}, 500

        return {"messages": "Tạo người dùng thành công"}, 201

    def get(self, ma=None):
        if ma == None:
            list = []
            for user in UserModel.query.all():
                list.append(user.json())
            return list
        user = UserModel.find_by_ma(ma)
        if user is None:
            return {"messages": "không tìm thấy người dùng"}
        return user.json()

    def put(self, ma):
        data = User.parser.parse_args()
        user = UserModel.find_by_ma(ma)
        if user is None:
            return {"messages": "không tìm thấy người dùng"}, 404
        else:
            try:
                if data["ma"]:
                    print(1)
                    user.ma = data["ma"]
                if data["ho_ten"]:
                    user.ho_ten = data["ho_ten"]
                if data["ngay_sinh"]:
                    user.ngay_sinh = data["ngay_sinh"]
                if data["so_dien_thoai"]:
                    user.so_dien_thoai = data["so_dien_thoai"]
                if data["gioi_tinh"]:
                    user.gioi_tinh = data["gioi_tinh"]
                if data["que_quan"]:
                    user.que_quan = data["que_quan"]
                if data["dia_chi"]:
                    user.dia_chi = data["dia_chi"]
                if data["email"]:
                    user.email = data["email"]
                if data["chuc_vu"]:
                    user.chuc_vu = data["chuc_vu"]
                if data["username"]:
                    user.chuc_vu = data["chuc_vu"]
                if data["password"]:
                    user.chuc_vu = data["password"]
                user.save_to_db()
            except:
                return {"messages": "không sửa được dữ liệu được người dùng"}, 500
        return {"messages": "update successfully"}

    def delete(self, ma):
        user = UserModel.find_by_ma(ma)
        if user is None:
            return {"messages": "không tìm thấy người dùng"}, 404
        try:
            user.delete()
        except:
            return {"messages": "không xóa được người dùng"}, 500
        return {"messages": "xóa thành công"}


class UploadAva(Resource):
    def post(self, ma):
        ten_mien = set(["png", "jpg", "jpeg", "gif"])
        try:
            file_list = request.files.getlist("avatar")
        except:
            return jsonify({"message": "không get được file"})
        list_file = []
        for image in file_list:
            filename = image.filename
            print(filename)
            if filename.rsplit(".", 1)[1].lower() in ten_mien:
                print("a")
                list_file.append(image)
            else:
                return jsonify({"message": "1 trong các file của bạn không phải file ảnh"})

        for image in list_file:
            link = os.path.join(
                Config.UPLOAD_FOLDER, secure_filename(filename)
            )
            image.save(link)
            user = UserModel.find_by_ma(ma)
            user.avatar = link
            user.image_name = filename
            user.save_to_db()
            return jsonify({"message": "lưu thành công"})

    def get(self, ma, name):
        # kiểm tra user đăng nhập hiện tại có file name giống mình muốn lấy không. Làm sau login
        try:
            print(2)
            index_path = os.path.join(Config.UPLOAD_FOLDER, name)
            print(index_path)
        except:
            return jsonify({'message': 'Lỗi rồi'})
        return send_file(index_path)
