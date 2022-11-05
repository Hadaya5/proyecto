from flask import render_template
from flask import request,Flask
import sys
import json
from db import generateToken, get_database, convertId,checkToken
from flask import Blueprint
from config import supported_languages,text,schemas
from jsonschema import validate
from datetime import datetime
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

post = Blueprint('post', __name__)
