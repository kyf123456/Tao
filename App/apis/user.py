import os
import uuid

from flask import request
from flask_mail import Message
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

from App import helper, dao, settings
import App.ext
from App.models import User


class UserApi(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('name',
                        required=True,
                        help='用户名不能为空'
                        )

    def post(self):
        #从基本的请求解析器中复制请求参数说明
        registParser=self.parser.copy()
        #再注册时使用
        registParser.add_argument('password',
                            required=True,
                            help='密码不能为空',
                            dest='pwd')
        registParser.add_argument('email',
                            required=True,
                            help='邮箱不能为空'
                            )
        registParser.add_argument('phone',
                            required=True,
                            help='电话不能为空'
                            )
        registParser.add_argument('nickname',
                            required=True,
                            help='昵称不能为空'
                            )
        registParser.add_argument('photo_1',
                                  type=FileStorage,
                                  location='files',
                                  required=True,
                                  help='必须提供一个photo'
                                  )


        # 验证请求参数是满足要求
        args=registParser.parse_args()

        u=User()
        u.name=args.get('name')
        u.nickname=args.get('nickname')
        u.phone=args.get('phone')
        u.email=args.get('email')
        u.password=helper.md5_crypt(args.get('pwd'))

        uFile: FileStorage = args.get('photo_1')
        print('上传的文件名：', uFile.filename)

        newFileName = str(uuid.uuid4()).replace('-', '')
        newFileName += '.' + uFile.filename.split('.')[-1]

        uFile.save(os.path.join(settings.MEDIA_DIR, newFileName))


        if dao.save(u):
            helper.sendEmail(u)

            return {'status':200,
                    'msg':'上传成功,用户注册成功',
                    'path': '/static/uploads/{}'.format(newFileName)}

        return {'status':201,
                    'msg':'用户注册失败'}

    def get(self):
        #验证用户名是否已注册
        args=self.parser.parse_args()

        name=args.get('name')
        qs=dao.query(User).filter(User.name==name)
        if qs.count():

            return {'status':202,'msg':name+'用户名已被注册'}

        return {'status': 200, 'msg': name + '用户名注册成功'}



