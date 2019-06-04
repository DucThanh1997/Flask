from flask_restful import reqparse, Resource

from models.classs import ClasssModel


class Classs(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name", type=str, required=True, help="Không được bỏ trống tên lớp"
    )

    def post(self):
        data = Classs.parser.parse_args()
        print(data["name"])
        if ClasssModel.find_by_name(data["name"]):
            return {"messages": "lớp này đã tồn tại"}
        classs = ClasssModel(**data)
        try:
            classs.save_to_db()
        except:
            return {"messages": "không lưu được lớp"}, 500

        return {"messages": "Tạo lớp thành công"}, 201

    def get(self, id=None):
        if id == None:
            list = []
            for classs in ClasssModel.query.all():
                list.append(classs.json())
            return {"danh sách lớp": list}

        classs = ClasssModel.find_by_id(id)
        if classs is None:
            return {"messages": "không tìm thấy lớp"}
        return classs.json()

    def put(self, id):
        data = Classs.parser.parse_args()
        classs = ClasssModel.find_by_id(id)
        if classs is None:
            return {"messages": "không tìm thấy lớp"}, 404
        else:
            try:
                classs.name = data["name"]
                classs.save_to_db()
            except:
                return {"messages": "không sửa được dữ liệu được lớp"}, 500
        return {"messages": "update successfully"}

    def delete(self, id):
        classs = ClasssModel.find_by_id(id)
        if classs is None:
            return {"messages": "không tìm thấy lớp"}, 404
        try:
            classs.delete_from_db()
        except:
            return {"messages": "không xóa được lớp"}, 500
        return {"messages": "xóa thành công"}


