from db import db


class UserModel(db.Model):
    __tablename__ = "user"
    ma = db.Column(db.String(80), primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))
    ho_ten = db.Column(db.String(80))
    ngay_sinh = db.Column(db.String(80))
    so_dien_thoai = db.Column(db.String(10))
    gioi_tinh = db.Column(db.String(10))
    dia_chi = db.Column(db.String(100))
    que_quan = db.Column(db.String(50))
    avatar = db.Column(db.String(200))
    email = db.Column(db.String(80))
    image_name = db.Column(db.String(80))
    teach = db.relationship("Teacher_And_ClassModel")
    learn = db.relationship("Student_And_ClassModel")
    chuc_vu = db.Column(db.Integer)
    # 1: sinh viên
    # 2: giáo viên

    def __init__(
        self,
        ma,
        avatar,
        ho_ten,
        ngay_sinh,
        so_dien_thoai,
        gioi_tinh,
        dia_chi,
        que_quan,
        email,
        password,
        username,
        image_name,
        chuc_vu
    ):
        self.ma = ma
        self.ho_ten = ho_ten
        self.ngay_sinh = ngay_sinh
        self.so_dien_thoai = so_dien_thoai
        self.gioi_tinh = gioi_tinh
        self.dia_chi = dia_chi
        self.que_quan = que_quan
        self.email = email
        self.avatar = avatar
        self.username = username
        self.password = password
        self.image_name = image_name
        self.chuc_vu = chuc_vu

    def json(self):
        return {
            "mã ": self.ma,
            "họ và tên": self.ho_ten,
            "ngày sinh": self.ngay_sinh,
            "số điện thoại": self.so_dien_thoai,
            "giới tính": self.gioi_tinh,
            "quê quán": self.que_quan,
            "địa chỉ": self.dia_chi,
            "email": self.email,
            "avatar": self.avatar,
            "username": self.username
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_ma(cls, ma):
        user = cls.query.filter_by(ma=ma).first()
        return user

    @classmethod
    def find_by_username(cls, username):
        user = cls.query.filter_by(username=username).first()
        return user
