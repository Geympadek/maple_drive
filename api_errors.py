from loader import app
from flask import jsonify

success = ({"status": "success"}, 200)

class APIError(Exception):
    def __init__(self, msg: str, code: int, desc: str):
        super().__init__(desc)

        self.msg = msg
        self.code = code
        self.desc = desc

class APIKeyError(APIError):
    def __init__(self, desc: str = ""):
        super().__init__(msg="Request is missing a key.", code=400, desc=desc)

class UserNotFoundError(APIError):
    def __init__(self, desc: str = ""):
        super().__init__(msg="User not found.", code=404, desc=desc)

class UserAlreadyExistsError(APIError):
    def __init__(self, desc: str = ""):
        super().__init__(msg="User already exists.", code=400, desc=desc)

class FormatError(APIError):
    def __init__(self, desc: str = ""):
        super().__init__(msg="Value is in wrong format.", code=400, desc=desc)

class WrongPathError(APIError):
    def __init__(self, desc: str = ""):
        super().__init__(msg="The given path is wrong.", code=400, desc=desc)


@app.errorhandler(APIError)
def handle_api_error(error: APIError):
    data = {
        "message": error.msg,
        "code": error.code
    }
    if error.desc != "":
        data["description"] = error.desc

    response = jsonify(data)
    response.status_code = error.code

    return response