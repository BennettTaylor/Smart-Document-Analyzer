from flask import Flask, jasonify, request
import uuid


class User:
    def signup(self):
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }
        return jasonify(user), 200
