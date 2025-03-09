import database
from flask import Flask

app = Flask("maple_drive")
database = database.FileDatabase('database.db')