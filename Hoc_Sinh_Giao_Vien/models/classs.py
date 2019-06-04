from db import db
class ClasssModel(db.Model):
    __tablename__ = "class"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    lop = db.relationship("Student_And_ClassModel")
    day = db.relationship("Teacher_And_ClassModel")

    def __init__(self, name):
        self.name = name

    def json(self):
        return {"id": self.id, "name": self.name}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
