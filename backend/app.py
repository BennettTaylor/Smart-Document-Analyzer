from flask import Flask, request
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

file = {}


class File(Resource):
    def get(self, file_id):
        return file[file_id]


if __name__ == "__main__":
    app.run(debug=True)
