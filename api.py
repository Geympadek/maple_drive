from loader import app
import os
from os.path import join

import shutil

from flask import request, jsonify, send_file

import security

import api_errors
from config import DB_PATH

def get_value(data: dict, key: str):
    try:
        return data[key]
    except KeyError:
        raise api_errors.APIKeyError(f"Missing {key} value.")

def user_exists(user_id: int | str):
    return os.path.exists(join(DB_PATH, f"{user_id}"))

def info_from_path(full_path: str):
    _, filename = os.path.split(full_path)
    name, ext = os.path.splitext(filename)
    return {
        "name": filename,
        "path": full_path,
        "type": "file" if ext else "directory"
    }

def verify_session():
    token = request.cookies.get("token", None)
    if not security.verify_token(token) or token is None:
        raise api_errors.AccessDeniedError("Provided token is invalid!")
    return token

def is_inside(path: str, folder: str):
    '''
    Check if the path is inside the folder
    '''
    path = os.path.abspath(path)
    folder = os.path.abspath(folder)

    return path.startswith(folder)

@app.route('/api/list_dir', methods=['GET'])
def list_dir():
    token = verify_session()

    user_data = security.data_from_token(token)
    user_id = user_data["user_id"]

    data = request.get_json()

    if not user_exists(user_id):
        raise api_errors.UserNotFoundError(f"User with id '{user_id}' doesn't exist")

    rel_path = get_value(data, "path")
    user_folder = join(DB_PATH, str(user_id))
    full_path = join(user_folder, rel_path)

    if not is_inside(full_path, user_folder):
        raise api_errors.WrongPathError("The specified path is violating.")

    try:
        listdir = os.listdir(full_path) 
    except FileNotFoundError:
        raise api_errors.WrongPathError("The specified path is invalid.")

    files = []
    for entry in listdir:
        entry_path = join(rel_path, entry)
        files.append(info_from_path(entry_path))
    
    response = jsonify(files)
    response.status_code = 200
    return response

@app.route("/api/download", methods=["GET"])
def download_file():
    token = verify_session()

    user_data = security.data_from_token(token)
    user_id = user_data["user_id"]

    data = request.get_json()

    rel_path: str = get_value(data, "path")
    user_folder = join(DB_PATH, str(user_id))
    full_path = join(user_folder, rel_path)

    if not is_inside(full_path, user_folder):
        raise api_errors.WrongPathError("The specified path is violating.")

    if os.path.isfile(full_path):
        return send_file(full_path, as_attachment=True)
    
    shutil.make_archive('tmp/archive', 'zip', full_path)
    return send_file('tmp/archive.zip', as_attachment=True)