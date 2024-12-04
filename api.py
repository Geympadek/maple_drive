from loader import app
import os
from os.path import join

from flask import request

from api_errors import APIKeyError, UserNotFoundError, UserAlreadyExistsError, success, FormatError

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

@app.route('/api/auth', methods=['GET'])
def auth_user():
    data = request.get_json()

    try:
        user_id = int(get_value(data, "user_id"))
    except ValueError:
        raise FormatError("Unable to parse user_id.")

    if os.path.exists(join(DB_PATH, f"{user_id}")):
        return success
    raise UserNotFoundError(f"User with id '{user_id}' doesn't exist")

@app.route('/api/list_dir', methods=['GET'])
def list_dir():
    data = request.get_json()

    user_id = get_value(data, "user_id")

    rel_path = get_value(data, "path")
    full_path = join(DB_PATH, str(user_id), rel_path)

    for entry in os.listdir(full_path):
        print(entry)
    
    return success