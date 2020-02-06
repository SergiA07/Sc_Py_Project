# https://www.codementor.io/@sagaragarwal94/building-a-basic-restful-api-in-python-58k02xsiq
import time
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from json import dumps
from flask_jsonpify import jsonify


class Analysis(Resource):
    def __init__(self, analysis):
        self.analysis = analysis

    def get(self):
        result = self.analysis
        return jsonify(result)


class server_REST:
    def __init__(self, analysis):
        app = Flask(__name__)
        CORS(app)
        api = Api(app)
        api.add_resource(Analysis, '/analysis',
                         resource_class_kwargs={'analysis': analysis})
        app.run(port='5002')
