from flask import Flask, jasonify


class User:
    def signUp(self):
        user = {
            "_id": "",
            "name": "",
            "email": "",
            "password": ""
        }
        return jasonify(user), 200
