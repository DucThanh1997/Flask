from flask import Flask
from db import db
from flask_jwt_extended import JWTManager
import pymysql
from flask_restful import Api

from resources.user import *
from resources.classs import *
from resources.student_and_class import *
from resources.teacher_and_class import *
from config import Config
pymysql.install_as_MySQLdb()



app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Classs, "/class", "/class/<int:id>")
api.add_resource(User, "/user", "/user/<string:ma>")

api.add_resource(
    Student_And_Class, "/danhsach",
                       "/danhsach/<int:id_lop>",
                       "/danhsach/<int:id_lop>",
                       "/danhsach/<int:id_lop>/<string:ma>"
)

api.add_resource(Teacher_And_Class, "/teach", "/teach/<int:id_lop>/<string:ma>", "/teach/<int:id_lop>")
api.add_resource(UploadAva, "/upload/<string:ma>", "/upload/<string:ma>/<string:filename>")

if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
