import os


class Config():
    ENV='development'
    DEBUG='True'

    #配置数据库链接
    SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:root@127.0.0.1:3306/Tao'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #配置邮箱
    MAIL_SERVER='smtp.163.com'  #邮箱服务器
    MAIL_USERNAME='disenqf@163.com'
    MAIL_PASSWORD='disen8888'  #授权码


    #配置安全密钥
    SECRET_KEY='ssssss'

# 设置上传文件存放的位置
BASE_DIR = os.path.dirname(os.path.abspath(__name__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
MEDIA_DIR = os.path.join(STATIC_DIR, 'uploads')