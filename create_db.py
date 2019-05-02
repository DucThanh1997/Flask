import sqlalchemy
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref


engine = sqlalchemy.create_engine('mysql://root:thanh1997@127.0.0.1') # connect to server
engine.execute("CREATE DATABASE test1") #create db
engine.execute("USE test1") # select new db

Base = declarative_base()

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column(String(15), unique=True)
    password = Column(String(16))

    def __init__(self, username, password):
        self.username = username
        self.password = password


Base.metadata.create_all(engine)

