from db import db


class Student_And_ClassModel(db.Model):
    __tablename__ = "class_and_student"

    id = db.Column(db.Integer, primary_key=True)
    id_lop = db.Column(db.Integer, db.ForeignKey("class.id"), nullable=False)
    lop = db.relationship("ClasssModel")
    ma = db.Column(db.String(80), db.ForeignKey("user.ma"), nullable=False)
    learn = db.relationship("UserModel")

    def __init__(self, id_lop, ma):
        self.id_lop = id_lop
        self.ma = ma

    def json(self):
        return {"id_lop": self.id_lop, "ma": self.ma}

    @classmethod
    def find_row(cls, id_lop, ma):  # vẫn cần giữ
        return cls.query.filter_by(id_lop=id_lop, ma=ma).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id)

    @classmethod
    def find_by_id_lop(cls, id_lop):
        return cls.query.filter_by(id_lop=id_lop).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
