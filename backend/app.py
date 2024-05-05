from flask import Flask
from flask import jsonify
from flask import request

from uuid import uuid4

from flask_bcrypt import Bcrypt

from flask_cors import CORS

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from flask_sqlalchemy import SQLAlchemy

import pathlib
from pypdf import PdfReader

ALLOWED_EXTENSIONS = {'pdf', 'txt'}


# Make API
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()


def get_uuid():
    return uuid4().hex


# Define the user and file model and thier relation
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(345), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    files = db.relationship("File", backref="user")


class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    name = db.Column(db.String(80), unique=False, nullable=False)
    content = db.Column(db.Text)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'))


# Create the database tables
bcrypt = Bcrypt(app)
db.init_app(app)

with app.app_context():
    db.create_all()

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "Bennett-Taylor"
jwt = JWTManager(app)


# Define functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_extention(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Define routes

# Login route
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
    
    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token), 200
    

# Register route
@app.route("/register", methods=["POST"])
def register():
    name = request.json.get("name", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user_exists = User.query.filter_by(email=email).first() is not None
    if user_exists:
        return jsonify({"error": "User already exists."}), 409
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(email=email, password=hashed_password, name=name)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        "id": new_user.id,
        "email": new_user.email,
        "name": new_user.name
    }), 200


@app.route('/upload_file', methods=['POST'])
@jwt_required()
def upload_file():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    if 'file' not in request.files:
        return jsonify({"msg": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400

    if file and allowed_file(file.filename):
        # Save file metadata to the database
        text = ""
        if pathlib.Path(file.filename).suffix == '.pdf':
            reader = PdfReader(file)
            for i in range(len(reader.pages)):
                page = reader.pages[i]
                text.append(page.extract_text)
        else:
            text = file.read()
        new_file = File(name=file.filename, content=text, user_id=user.id)
        db.session.add(new_file)
        db.session.commit()

    return jsonify({"msg": "File uploaded successfully"}), 200


@app.route('/get_filenames', methods=['GET'])
@jwt_required()
def get_filenames():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    file_names = []
    for file in user.files:
        file_names.append(file.name)
    return jsonify({"file_names": file_names}), 200


# Run API
if __name__ == "__main__":
    app.run(debug=True)
