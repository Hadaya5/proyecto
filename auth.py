from flask import render_template
from flask import request,Flask,redirect
import sys
import json
from db import generateToken, get_database, convertId,revokeToken,checkToken
from flask import Blueprint
from config import supported_languages,text,schemas
from flask_argon2 import Argon2
from jsonschema import validate
from datetime import datetime

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

auth = Blueprint('auth', __name__)

argon2 = Argon2(Flask(__name__))

@auth.route('/signup',methods = ['GET', 'POST'])
def sign():
    lang = request.accept_languages.best_match(supported_languages)
    if(request.method == 'GET'):
        return render_template('signup.html',text=text[lang])
    elif(request.method == 'POST'):
        js = request.json
        try:
            validate(js,schemas['signup.schema.json'])
        except Exception as e:
            eprint(e)
            return '{"result":"invalid"}'

        try:
            db = get_database()
        except Exception as e:
            eprint(e)
            return '{"result":"error"}'
        users = db['users']
        email = js.get('email','')
        if(users.find_one({'email':email})):
            return {"result":"emailused",
                    "message":text[lang]['emailused'] }
        js['password'] = argon2.generate_password_hash(js['password'])
        eprint(json.dumps(js,indent=4))
        e = users.insert_one(js)
        profile = {"_id":e.inserted_id,"cover":"","icon":""}
        config = {"_id":e.inserted_id,"language":lang}
        db['profiles'].insert_one(profile)
        db['config'].insert_one(config)
        eprint(e)
        response = {
            "result":"ok",
            "message":text[lang]['signupsuccess'],
            "submessage":text[lang]['pleaselogin']
        }
        return json.dumps({"result":"ok"})


@auth.route('/login',methods = ['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        password = request.json.get('password')
        email = request.json.get('email')
        try:
            db = get_database()
        except Exception as e:
            eprint(e)
            return '{"result":"server error"}'
        
        
        user = db['users'].find_one({"email":email})
        if(not user):
            return '{"result":"usuario inexistente"}'
        valid = argon2.check_password_hash(user['password'],password)
        if(valid):
            token = generateToken(user['_id'])
            response = {"result":"ok","uid":convertId(user['_id']),"token":token['token'],
                        "expires":token['expires']}
            return json.dumps(response)
        else:
            return '{"result":"invalid password"}'
    else:
        token = request.cookies.get('token','')
        uid = checkToken(token)
        if(uid):
            return redirect('/perfil')
        lang = request.accept_languages.best_match(supported_languages)    

        return render_template('login.html',text=text[lang])

@auth.route('/logout',methods = ['GET','POST'])
def logout():
    lang = request.accept_languages.best_match(supported_languages)    
    if (request.method == 'GET'):
        token = request.cookies.get('token','')
        revokeToken(token)
        return render_template('notloged.html',text=text[lang])
