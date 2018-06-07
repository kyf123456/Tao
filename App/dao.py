#定义数据库的功能函数
from flask_sqlalchemy import BaseQuery
from App.models import db


def query(cls) ->BaseQuery:
    return db.session.query(cls)


def queryAll(cls):
    return query(cls).all()

def getById(cls,id):
    #获取制定id 的数据
    try:
        db.session.query(cls).get(int(id))
    except:
        pass



# def queryByWhere(cls,**where):
#     #queryByWhere((City,Ctiy.regionName==))
#     return query(cls).filter(**where)

def save(obj)-> bool:
    try:
        db.session.add(obj)
        db.session.commit()
    except:
        return  False
    return True

def delete(obj) -> bool:
    try:
        db.session.dalete(obj)
        db.session.commit()
    except:
        return False
    return True

