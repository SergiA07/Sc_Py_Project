# https://www.codementor.io/@sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq
from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask_jsonpify import jsonify

class Employees(Resource):
    def __init__(self, analysis):
        self.analysis = analysis
    def get(self):
        print(Resource)
        result = self.analysis
        return jsonify(result)

class REST_server:
    # parameterized constructor
    def __init__(self, analysis):
        self.analysis = analysis
        app = Flask(__name__)
        api = Api(app)
        api.add_resource(Employees(self.analysis), '/employees') # Route_1
        # if _name_ == '_main_':
        app.run(port='5002')


test_analisis = {"key": 1234}
rest_server = REST_server(test_analisis)

print(rest_server.analysis)
