#声明数据库表对应的模型类
from datetime import datetime

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Float
from sqlalchemy.orm import relationship, backref


db=SQLAlchemy()
migrate=Migrate()


def init_db(app):
    db.init_app(app)
    Migrate(app,db)



class Letter(db.Model):
    __tablename__='t_letter'
    id = Column(Integer, primary_key=True)
    name=Column(String(10))



class City(db.Model):
    __tablename__ = 't_city'
    id=Column(Integer,primary_key=True)
    parentId=Column(Integer,default=0)
    regionName=Column(String(20))
    cityCode=Column(Integer)
    pinYin=Column(String(50))

    letter_id=Column(Integer,ForeignKey(Letter.id))
    letter=relationship('Letter',
                        backref=backref('citys',lazy=True))


class User(db.Model):
    __tablename__ = 't_user'
    id=Column(Integer,primary_key=True)
    name=Column(String(50),unique=True)
    password=Column(String(50))
    nickname=Column(String(50))
    email=Column(String(50),unique=True)
    phone=Column(String(50),unique=True)
    is_active=Column(Boolean,default=False)
    is_life=Column(Boolean,default=True)
    regist_time=Column(DateTime,default=datetime.now())
    last_login_time=Column(DateTime)

    photo_1=Column(String(200),nullable=True)  #原图
    photo_2=Column(String(200),nullable=True)  #小图

# name,city,district,address,phone,score,hallnum,servicecharge,astrict,flag,isdelete
class Cinemas(db.Model):
    id = Column(Integer, primary_key=True,autoincrement=True)
    name=Column(String(50))
    city=Column(String(50))
    district=Column(String(200))
    address=Column(String(200))
    phone=Column(String(200))
    score=Column(Float(10,1))
    hallnum=Column(Integer)
    servicecharge=Column(String(10))
    astrict=Column(String(10))
    flag=Column(String(10))
    isdelete=Column(Boolean,default=0)

# id, showname, shownameen, director, leadingRole, type, country, language, duration, screeningmodel, openday, backgroundpicture, flag, isdelete)
class Movies(db.Model):
    id=Column(Integer, primary_key=True,
              autoincrement=True)
    showname=Column(String(200))
    shownameen=Column(String(200))
    director=Column(String(200))
    leadingRole=Column(String(300))
    type=Column(String(200))
    country=Column(String(200))
    language=Column(String(200))
    duration=Column(Integer)
    screeningmodel=Column(String(200))
    openday=Column(String(200))
    screeningmodel=Column(String(200))
    openday=Column(DateTime)
    backgroundpicture=Column(String(200))
    flag=Column(Integer)
    isdelete=Column(Boolean)

