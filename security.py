import string
import secrets

import hashlib

import config
import hmac

from loader import database
from urllib.parse import parse_qs, unquote, urlencode

import json

TOKEN_LEN = 32

def gen_token():
    characters = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(characters) for _ in range(TOKEN_LEN))
    return token

def hmac_sha256(msg: str, key: str):
    return hmac.new(msg=msg.encode(), key=key.encode(), digestmod=hashlib.sha256)

def parse_data_str(data_str: str, sep: str):
    '''
    Parses `data_str` into a dictionary.
    \n`sep` - separator. Usually '&', but Telegram uses '\n' sometimes
    '''
    data = parse_qs(data_str, separator=sep)

    # none of the properties are lists, but `parse_qs` thinks otherwise.
    result = {key: value[0] for key, value in data.items()}
    return result

def parse_user_data(data_str: str, sep: str) -> dict:
    data = parse_data_str(data_str, sep)

    user_data = json.loads(data["user"])
    return user_data

secret_key = hmac_sha256(config.BOT_TOKEN, "WebAppData").digest()

def format_data_str(data_str: str):
    '''
    Telegram strings are weird. This formats it for verification.
    '''
    data = parse_data_str(data_str, '&')
    #delete the hash property
    del data["hash"]
    #sort the elements by keys
    data = sorted(data.items(), key=lambda x: x[0])
    #convert the dictionary back to the data string
    data_str = urlencode(data)
    data_str = unquote(data_str)
    #replace & with \n for some fkn reason
    data_str = data_str.replace('&', '\n')
    return data_str

def validate(data_str: str):
    hash = parse_data_str(data_str, '&')["hash"]

    data_str = format_data_str(data_str)
    test = hmac.new(msg=data_str.encode(), key=secret_key, digestmod=hashlib.sha256).hexdigest()
    return test == hash

def get_token(user_id: int) -> str | None:
    data = database.read("tokens", filters={"user_id": user_id})
    return data[0]["token"] if len(data) else None

def push_token(user_id: int):
    token = gen_token()
    database.create("tokens", data={"user_id": user_id, "token": token})
    return token

def data_from_token(token: str):
    data = database.read("tokens", filters={"token": token})
    return data[0] if len(data) else None

def verify_token(token: str):
    return data_from_token(token) is not None