#!/usr/bin/env python
import flask
from flask import render_template
from pymongo import MongoClient
from flask import request
import sys
import json
from config import text,supported_languages
from db import get_database
from auth import auth
from posts import post
from user import user
    
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

app = flask.Flask(__name__)
app.register_blueprint(auth,name="auth")
app.register_blueprint(post,name="post")
app.register_blueprint(user,name="user")

@app.errorhandler(404)
def not_found(e):
    
    lang = request.accept_languages.best_match(supported_languages)    
    return render_template("404.html",text=text[lang])
@app.route('/')
def home():
    
    lang = request.accept_languages.best_match(supported_languages)    
    return render_template('home.html',text=text[lang])

@app.route('/post',methods = ['GET', 'POST'])
def post():
    if(request.method == 'GET'):
        return render_template('publicacion.html')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)     # open for everyone