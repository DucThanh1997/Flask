from flask_restful import reqparse, Resource
from django.db import IntegrityError
from models.student_and_class import Student_And_ClassModel
from sqlalchemy import exc
from models.classs import ClasssModel
from models.user import UserModel
from decorators import sv_authenticate

class Student_And_Class(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("id_lop", type=int, required=False)
    parser.add_argument("ma", type=str, required=False)

    def post(self):
        data = Student_And_Class.parser.parse_args()
        if Student_And_ClassModel.find_row(data["id_lop"], data["ma"]):
            return {"messages": "dòng này đã tồn tại"}
        row = Student_And_ClassModel(**data)
        try:
            row.save_to_db()
        except exc.IntegrityError:
            return (
                {
                    "messages": "không lưu được dòng do vấn đề khóa ngoại hãy kiểm tra lại khóa ngoại"
                },
                404,
            )
        except:
            return {"messages": "không sửa được dữ liệu"}, 500
        return {"messages": "Tạo dòng thành công"}, 200

    def get(self, id_lop=None):
        if id_lop == None:
            list = []
            for row in Student_And_ClassModel.query.all():
                list.append(row.json())
            return {"danh sách lớp": list}

        list = Student_And_ClassModel.find_by_id_lop(id_lop)
        list2 = []
        for row in list:
            list2.append(row.json())
        return {"danh sách lớp": list2}

    def put(self, id_lop, ma):
        data = Student_And_Class.parser.parse_args()
        row = Student_And_ClassModel.find_row(id_lop, ma)
        if row is None:
            return {"messages": "không tìm thấy dòng"}, 404
        else:
            try:
                if data["id_lop"]:
                    row.id_lop = data["id_lop"]
                if data["ma"]:
                    row.ma = data["ma"]
                row.save_to_db()
            except exc.IntegrityError:
                return (
                    {
                        "messages": "không lưu được dòng do vấn đề khóa ngoại hãy kiểm tra lại khóa ngoại"
                    },
                    500,
                )
            except:
                return {"messages": "không sửa được dữ liệu"}, 500
        return {"messages": "update successfully"}

    def delete(self, id_lop, ma):
        row = Student_And_ClassModel.find_row(id_lop, ma)
        if row is None:
            return {"messages": "không tìm thấy dòng"}, 404
        try:
            row.delete_from_db()
        except:
            return {"messages": "không xóa được dòng"}, 500
        return {"messages": "xóa thành công"}

