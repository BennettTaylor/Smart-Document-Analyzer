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
from nlp import perform_nlp, generate_summary

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
    content = db.Column(db.String)
    sentiment_score = db.Column(db.Float)
    document_summary = db.Column(db.String)
    keywords = db.Column(db.String)
    user_id = db.Column(db.String(32), db.ForeignKey('users.id'))
    paragraphs = db.relationship("Paragraph", backref="user")


class Paragraph(db.Model):
    __tablename__ = 'paragraphs'
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    content = db.Column(db.String)
    sentiment_score = db.Column(db.Float)
    document_summary = db.Column(db.String)
    keywords = db.Column(db.String)
    file_id = db.Column(db.String(32), db.ForeignKey('files.id'))


# Create the database tables
bcrypt = Bcrypt(app)
db.init_app(app)

with app.app_context():
    db.create_all()

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "Bennett-Taylor"
jwt = JWTManager(app)


# Define functions
def convertFiletoText(file):
    text = ""
    if pathlib.Path(file.filename).suffix == '.pdf':
        reader = PdfReader(file)
        for i in range(len(reader.pages)):
            page = reader.pages[i]
            text.append(page.extract_text)
    else:
        text = file.read()
        text = str(text)
        text = text.replace(text[0], "", 1)
        text = text.replace(text[0], "", 1)
        text = text.replace(text[-1], "", 1)
    return str(text)


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
        text = convertFiletoText(file)
        paragraphs = text.split("\\n\\n")
        sentiment, keywords = perform_nlp(text)
        summary = generate_summary(text)
        new_file = File(name=str(file.filename),
                        content=str(text),
                        user_id=user.id,
                        sentiment_score=sentiment,
                        keywords=str(keywords[0]),
                        document_summary=str(summary))
        db.session.add(new_file)
        db.session.commit()
        for paragraph in paragraphs:
            sentiment, keywords = perform_nlp(paragraph)
            new_paragraph = Paragraph(
                content=str(paragraph),
                sentiment_score=sentiment,
                keywords=str(keywords[0]),
                file_id=new_file.id
            )
            db.session.add(new_paragraph)
            db.session.commit()
    return jsonify({"msg": "File uploaded successfully"}), 200


@app.route('/get_files', methods=['GET'])
@jwt_required()
def get_filenames():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    files = []
    for file in user.files:
        files.append({"name": file.name,
                      "id": file.id})
    return jsonify({"files": files}), 200


@app.route('/get_file_details/<file_id>', methods=['GET'])
@jwt_required()
def get_file_details(file_id):
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    for files in user.files:
        if files.id == file_id:
            file = files
    if file is None:
        return jsonify({"error": "Document does not exist"}), 400
    paragraphs = []
    for paragraph in file.paragraphs:
        paragraphs.append({
            "text": str(paragraph.content),
            "sentiment_score": paragraph.sentiment_score,
            "keywords": paragraph.keywords,
            })
    return jsonify({"fileDetails": {
        "filename": str(file.name),
        "text": str(file.content),
        "document_summary": str(file.document_summary),
        "sentiment_score": file.sentiment_score,
        "keywords": file.keywords,
        "paragraphs": paragraphs
    }})


# Run API
if __name__ == "__main__":
    app.run(debug=True)
