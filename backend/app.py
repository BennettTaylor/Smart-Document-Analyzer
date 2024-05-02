from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

file = {}


class File(Resource):
    def get(self, file_id):
        return file[file_id]


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
