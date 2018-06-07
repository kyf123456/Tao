from flask_restful import Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import BaseQuery

from App import dao
from App.models import Movies


class MoviesApi(Resource):
    # 定制输入参数
    parser=reqparse.RequestParser()
    parser.add_argument('flag',type=int,required=True,help='电影名不能为空')
    parser.add_argument('city',default='')
    parser.add_argument('region',default='')
    parser.add_argument('orderby',default='openday')
    parser.add_argument('sort',type=int,default=1) #1降序
    parser.add_argument('page',type=int,default=1,help='每页显示')
    parser.add_argument('limit',type=int,default=10,help='每页显示的大小数值')

    # 定制输出字段
    out_fields={
        'returnCode':fields.String(default='0'),
        'returnValue':fields.Nested({
            "backgroundPicture":fields.String(attribute='backgroundpicture'),
            "country":fields.String,
            "director":fields.String,
            "showName":fields.String(attribute='shoename'),
            "showNameEn":fields.String(attribute='shownameen'),
            'openTime':fields.DateTime(attribute='openday')
        })
    }

    @marshal_with(out_fields)
    def get(self):
        #验证请求参数
        args=self.parser.parse_args()
        flag=args.get('flag')
        qs:BaseQuery=dao.query(Movies).filter(Movies.flag==flag)

        sort=args.get('sort')
        qs:BaseQuery=qs.order_by(('-' if sort == 1 else '')+args.get('orderby'))
        #分页
        pager=qs.paginate(args.get('page'),args.get('limit'))

        print('获得的影片数量:',len(qs.all()))


        return {'returnvalue':pager.items}

