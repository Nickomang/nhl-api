from flask import Flask
from flask_restful import Api
from myapi.resources.foo import Foo
from myapi.resources.bar import Bar
from myapi.resources.baz import Baz

app = Flask(__name__)
api = Api(app)

api.add_resource(Foo, '/Foo', '/Foo/<str:id>')
api.add_resource(Bar, '/Bar', '/Bar/<str:id>')
api.add_resource(Baz, '/Baz', '/Baz/<str:id>')