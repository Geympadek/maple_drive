from loader import app, database
from flask import render_template, request
import auth
import filesystem as fs
import security
import api_errors
import os
import config

@app.route('/')
def index():
    return render_template("index.html")

def verify_session():
    token = request.cookies.get("token", None)
    if not security.verify_token(token) or token is None:
        raise api_errors.AccessDeniedError("Provided token is invalid!")
    return token

@app.route('/api/list', methods=["GET"])
def ls():
    token = verify_session()
    user_data = security.data_from_token(token)
    user_id = user_data["user_id"]

    rel_path = request.args["path"][1:-1]
    if fs.is_violating(user_id, rel_path):
        raise api_errors.WrongPathError("The given path is violating.")

    return fs.ls(user_id, rel_path)