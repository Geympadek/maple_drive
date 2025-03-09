import api_errors, os
from flask import request, jsonify
import security

from loader import app

from config import FS_PATH

@app.route('/api/register', methods=['POST'])
def register_user():
    data_str = request.query_string.decode()

    if not security.validate(data_str):
        raise api_errors.AccessDeniedError("Provided data is not valid.")

    user_data = security.parse_user_data(data_str, sep='&')
    user_id = user_data["id"]

    token = security.get_token(user_id)
    if token is not None:
        raise api_errors.UserAlreadyExistsError("User with this user_id already exists.")
    
    token = security.push_token(user_id)

    os.makedirs(os.path.join(FS_PATH, f"{user_id}"))

    response = jsonify({"status": "success"})
    response.set_cookie("token", token, httponly=True, secure=True, samesite="None")
    return response

@app.route('/api/auth', methods=['GET'])
def auth_user():
    data_str = request.query_string.decode()

    if not security.validate(data_str):
        raise api_errors.AccessDeniedError("Provided data is not valid.")

    user_data = security.parse_user_data(data_str, sep='&')
    user_id = user_data["id"]

    token = security.get_token(user_id)
    if token is None:
        raise api_errors.UserNotFoundError("The user doesn't exist.")
    
    response = jsonify({"status": "success"})
    response.set_cookie("token", token, httponly=True, secure=True)
    return response