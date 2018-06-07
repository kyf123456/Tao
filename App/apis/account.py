from datetime import datetime

from flask import request, session
from flask_restful import Resource, reqparse, fields, marshal

import App
from App import dao, helper
from App.models import User


class AccountApi(Resource):
    # 从请求参数中获取opt和token参数值
    # 如果opt 为active ，则从redis缓存中查询token对应的user.id
    # 再通过 user.id查询数据库中用户， 最后更新用户的is_active状态为True

    parser=reqparse.RequestParser()
    parser.add_argument('opt',required=True,help="没有声明opt")
    # parser.add_argument('token')


    def get(self):
        args=self.parser.parse_args()
        opt=args.get('opt')
        if opt=='active':
            activeParser=self.parser.copy()
            activeParser.add_argument('token',required=True,help='没有激活的token')
            args=activeParser.parse_args()
            token=args.get('token')
            #进一步处理
            user_id=App.ext.cache.get('token')
            if user_id:
                #查询用户，并设置用户激活状态
                user=dao.getById(User,user_id)
                user.is_active=True

                dao.save(user)

                return {'msg',user.nickname+'用户激活成功!'}
            else:
                #重新申请用户激活
                reactive_url=request.host_url+'account/?opt=reactive'

                return {'msg': ' 本次激活已过期，需要重新申请激活: '+ reactive_url}

        elif opt=='login':
            return self.login()
            # return {'msg': '用户激活成功'}
        elif opt=='reactive':
            return self.reactive()
        elif opt=='logout':
            return self.logout()


    def login(self):
        #GET请求时，opt为login时
        loginParser=self.parser.copy()
        loginParser.add_argument('name',required=True,help='必须提供用户名')
        loginParser.add_argument('password',required=True,help='必须提供口令')
        #验证登陆参数
        args=loginParser.parse_args()

        name=args.get('name')
        password=args.get('password')
        # 查询用户(用户必须是激活状态)
        print(name,password)


        qs=dao.query(User).filter(User.name==name,
                                  User.password==(helper.md5_crypt(password)),
                                  User.is_active==True,
                                  User.is_life==True)
        if not qs.count():
            return {'status': 600,
                    'msg': '用户登陆失败，用户名或口令不正确'}

        u:User=qs.first()
        u.last_login_time=datetime.today()
        dao.save(u)
        token=helper.getToken()

        # 将token存放session中

        session[token]=u.id

        out_user_fields={
            'name':fields.String,
            'email':fields.String,
            'phone':fields.String,
            'photo':fields.String(attribute='photo_1')
        }
        out_fields={
            'msg':fields.String,
            'data':fields.Nested(out_user_fields),
            'access_token':fields.String
        }
        data={
            'msg':'登陆成功',
            'data':u,
            'access_token':token
        }
        # 通过marshal 将返回的data数据按输出字段转成json字符
        return marshal(data,out_fields)

    def reactive(self):
        # 重新申请用户激活
        reactiveParser=self.parser.copy()
        reactiveParser.add_argument('email',required=True,help='必须提供正确邮箱')
        args=reactiveParser.parse_args()

        email=args.get('email')
        qs=dao.query(User).filter(User.email==email)
        if not qs.count():
            #重新发送邮件

            return {
                'status':700,
                'msg':email+'邮箱未被注册'
            }
        # 重新发送邮箱
        helper.sendEmail(qs.first())
        return {'msg':'重新申请用户激活，请点击邮箱进行激活'}

    def logout(self):
        myParser=self.parser.copy()
        myParser.add_argument('token',required=True,help='请提供token')

        args=myParser.parse_args()
        token=args.get('token')
        user_id=session.get(token)
        if not user_id:
            return {'status':701,'msg':'用户未登录，请先登录'}
        u=dao.getById(User,user_id)
        if not u:
            return {'status': 702, 'msg': '用户退出失败，token无效!'}
        session.pop(token)
        return {'status': 200, 'msg': '退出成功!'}


