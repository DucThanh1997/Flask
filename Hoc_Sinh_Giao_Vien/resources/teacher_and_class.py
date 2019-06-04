from flask_restful import reqparse, Resource
from sqlalchemy import exc
from models.teacher_and_class import Teacher_And_ClassModel

BLANK_ERROR = "Không được bỏ trống trường {}"
ITEMS_NOT_FOUND = "Không tìm thấy"


class Teacher_And_Class(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "id_lop", type=int, required=False, help=BLANK_ERROR.format("id lớp")
    )
    parser.add_argument(
        "ma", type=str, required=False, help="Không được bỏ trống trường"
    )

    def post(self):
        data = Teacher_And_Class.parser.parse_args()
        if Teacher_And_ClassModel.find_row(data["id_lop"], data["ma"]):
            return {"messages": "dòng này đã tồn tại"}
        row = Teacher_And_ClassModel(**data)
        try:
            row.save_to_db()
        except exc.IntegrityError:
            return (
                {
                    "messages": "không lưu được dòng do vấn đề khóa ngoại hãy kiểm tra lại khóa ngoại"
                },
                500,
            )
        except:
            return {"messages": "không lưu được dòng"}, 500

        return {"messages": "Tạo dòng thành công"}, 201

    def get(self, id_lop=None):
        if id_lop == None:
            list = []
            for row in Teacher_And_ClassModel.query.all():
                list.append(row.json())
            return {"danh sách lớp": list}

        list = Teacher_And_ClassModel.find_by_id_lop(id_lop)
        list2 = []
        for row in list:
            list2.append(row.json())
        return {"danh sách lớp": list2}

    def put(self, id_lop, ma):
        data = Teacher_And_Class.parser.parse_args()
        row = Teacher_And_ClassModel.find_row(id_lop, ma)
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
        row = Teacher_And_ClassModel.findd(id_lop, ma)
        if row is None:
            return {"messages": "không tìm thấy dòng"}, 404
        try:
            row.delete_from_db()
        except:
            return {"messages": "không xóa được dòng"}, 500
        return {"messages": "xóa thành công"}


