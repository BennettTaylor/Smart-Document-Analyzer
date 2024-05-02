from flask import Flask, render_template
from app import app
from user.models import User

@app.route('/user/signup', methods=['GET'])
def signup():
    return User.signup

