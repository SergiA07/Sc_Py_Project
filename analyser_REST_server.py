# https://www.codementor.io/@sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

class Employees(Resource):
    def get(self):
        result = {'employees': "TEST"} # analysis TODO
        return jsonify(result)

class REST_server:
    # parameterized constructor
    def __init__(self, analysis):
        self.analysis = analysis
        app = Flask(__name__)
        api = Api(app)
        api.add_resource(Employees, '/employees') # Route_1
        # if _name_ == '_main_':
        app.run(port='5002')
