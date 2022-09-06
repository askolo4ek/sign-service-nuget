from os import path as os_path

from flask import Flask
from flask_restful import Api

from .resources import SignNugetResource


def create_app() -> Flask:
    app: Flask = Flask(__name__)
    app.static_folder = os_path.abspath("static")

    api: Api = Api(app)

    api.add_resource(SignNugetResource, "/nuget")

    return app
