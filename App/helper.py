import hashlib
import uuid

from flask import request, render_template
from flask_mail import Message

import App


def md5_crypt(txt):
    m=hashlib.md5()
    m.update(txt.encode())

    return m.hexdigest()


def getToken():
    return md5_crypt(str(uuid.uuid4()))


def sendEmail(u):
    token = getToken()
    # 将token设置到redis缓存中
    App.ext.cache.set(token,u.id,timeout=60*10)# 允许100分钟内来激活用户
    active_url = request.host_url + 'account/?opt=active&taken=' + token
    print(active_url)
    #   发送邮件
    msg=Message(subject='淘票票激活用户',
                recipients=[u.email],
                sender='disenqf@163.com')
    msg.html="<h1>{}注册成功！</h1><h3>请先<a href='{}'>激活注册帐号</a>"\
             "</h3><h2>或者复制地址到浏览器: {}</h2><br>"\
                .format(u.name,active_url,active_url)
    # msg.html = render_template('msg.html', username=u.name, active_url=active_url)

    try:
        App.ext.mail.send(msg)

    except Exception as e:
        print(e)
        print('邮件发送失败')


