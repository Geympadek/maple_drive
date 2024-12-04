from loader import app
import os
from os.path import join

from flask import request, jsonify

from api_errors import APIKeyError, UserNotFoundError, UserAlreadyExistsError, success, FormatError, WrongPathError

DB_PATH = "database"

def get_value(data: dict, key: str):
    try:
        return data[key]
    except KeyError:
        raise APIKeyError(f"Missing {key} value.")

@app.route('/api/register', methods=['POST'])
def register_user():
    data = request.get_json()

    try:
        user_id = int(get_value(data, "user_id"))
    except ValueError:
        raise FormatError("Unable to parse user_id.")

    try:
        os.makedirs(join(DB_PATH, f"{user_id}"), exist_ok=False)
    except OSError:
        raise UserAlreadyExistsError(f"Directory '{user_id}' already exists.")
    return success

def user_exists(user_id: int | str):
    return os.path.exists(join(DB_PATH, f"{user_id}"))

@app.route('/api/auth', methods=['GET'])
def auth_user():
    data = request.get_json()

    try:
        user_id = int(get_value(data, "user_id"))
    except ValueError:
        raise FormatError("Unable to parse user_id.")

    if not user_exists(user_id):
        raise UserNotFoundError(f"User with id '{user_id}' doesn't exist")
    return success

def info_from_path(full_path: str):
    _, filename = os.path.split(full_path)
    name, ext = os.path.splitext(filename)
    return {
        "name": filename,
        "path": full_path,
        "type": "file" if ext else "directory"
    }

@app.route('/api/list_dir', methods=['GET'])
def list_dir():
    data = request.get_json()

    user_id = get_value(data, "user_id")

    if not user_exists(user_id):
        raise UserNotFoundError(f"User with id '{user_id}' doesn't exist")

    rel_path = get_value(data, "path")
    full_path = join(DB_PATH, str(user_id), rel_path)

    try:
        listdir = os.listdir(full_path) 
    except FileNotFoundError:
        raise WrongPathError()

    files = []
    for entry in listdir:
        entry_path = join(rel_path, entry)
        files.append(info_from_path(entry_path))
    
    response = jsonify(files)
    response.status_code = 200
    return response