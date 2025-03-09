from loader import app
from flask import jsonify

success = ({"status": "success"}, 200)

class APIError(Exception):
    def __init__(self, type: str, msg: str, code: int):
        super().__init__(msg)

        self.msg = msg
        self.code = code
        self.type = type

class APIKeyError(APIError):
    def __init__(self, msg: str = ""):
        super().__init__(type=self.__class__.__name__, msg=msg, code=400)

class UserNotFoundError(APIError):
    def __init__(self, msg: str = ""):
        super().__init__(type=self.__class__.__name__, msg=msg, code=404)

class UserAlreadyExistsError(APIError):
    def __init__(self, msg: str = ""):
        super().__init__(type=self.__class__.__name__, msg=msg, code=400)

class FormatError(APIError):
    def __init__(self, msg: str = ""):
        super().__init__(type=self.__class__.__name__, msg=msg, code=400)

class WrongPathError(APIError):
    def __init__(self, msg: str = ""):
        super().__init__(type=self.__class__.__name__, msg=msg, code=400)

class AccessDeniedError(APIError):
    def __init__(self, msg: str = ""):
        super().__init__(type=self.__class__.__name__, msg=msg, code=401)

@app.errorhandler(APIError)
def handle_api_error(error: APIError):
    data = {
        "message": error.msg,
        "code": error.code,
        "type": error.type
    }

    response = jsonify(data)
    response.status_code = error.code

    return response