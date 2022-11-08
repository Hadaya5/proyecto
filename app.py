#!/usr/bin/env python
import flask
from flask import render_template
from pymongo import MongoClient
from flask import request,redirect
import sys
import json
from config import text,supported_languages
from db import get_database,checkToken, getUser, getUserProfile, getLanguage
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
    token = request.cookies.get('token','')
    uid = checkToken(token)
    if(uid):
        return redirect('/feed')    
    lang = request.accept_languages.best_match(supported_languages)    
    return render_template('home.html',text=text[lang])

@app.route('/post',methods = ['GET', 'POST'])
def post():
    if(request.method == 'GET'):
        return render_template('publicacion.html')

@app.route('/manage',methods = ['GET'])
def manage():
    if(request.method == 'GET'):
        lang = request.accept_languages.best_match(supported_languages)  
        return render_template('manage.html',text=text[lang])

@app.route('/aboutus',methods = ['GET'])
def aboutus():
    if(request.method == 'GET'):
        lang = request.accept_languages.best_match(supported_languages)  
        return render_template('aboutus.html',text=text[lang])

@app.route('/feed',methods = ['GET'])
def feed():
    if(request.method == 'GET'):
        token = request.cookies.get('token','')
        uid = checkToken(token)
        if(not uid):
            return redirect('/')    
        user = getUser(uid)
        profile = getUserProfile(uid)
        lang = getLanguage(uid)
        return render_template('feed.html', text=text[lang], profile = profile, user = user)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)     # open for everyone