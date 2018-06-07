from flask_restful import Api

from App.apis.account import AccountApi
from App.apis.city import CityApi
from App.apis.movies import MoviesApi
from App.apis.user import UserApi


api=Api()

def init_api(app):
    api.init_app(app)



api.add_resource(CityApi,'/city/')
api.add_resource(UserApi,'/user/')
api.add_resource(AccountApi,'/account/')
api.add_resource(MoviesApi,'/movies/')

