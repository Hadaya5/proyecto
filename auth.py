from flask import render_template
from flask import request,Flask,redirect
import sys
import json
from db import generateToken, get_database, convertId,revokeToken,checkToken
from flask import Blueprint
from config import supported_languages,text,schemas, firebaseApiKey
from flask_argon2 import Argon2
from jsonschema import validate
from datetime import datetime
import requests

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
        # if(users.find_one({'email':email})):
        #     return {"result":"emailused",
        #             "message":text[lang]['emailused'] }
        # password_argon2 = argon2.generate_password_hash(js['password'])
        eprint(json.dumps(js,indent=4))
        response = requests.post(f'https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={firebaseApiKey}',json.dumps({
            'email':email,
            'password': js['password'],
            "returnSecureToken": True 
        }))
        eprint(response.content)
        if(response.status_code != 200):
            if(response.json().get('error')['message'] == 'EMAIL_EXISTS'):
                return {"result": 'emailused',"message": text[lang]['emailused']}

        eprint(json.dumps(response.json(),indent=4))
        user = {
            'email':email,
            "cover":"",
            "icon":"",
            "name":js['name'],
            "lastname":js['lastname'],
            "birthday":js['birthday'],
            'gender':js['gender'],
            'description':'',
            'color':'',
            'book': '',
            'music': '',
            'videogames': '',
            'languages': '',
            'idToken': response.json().get('idToken'),
            'firebaseId': response.json().get('localId'),
            'friends': []
        }
        e = users.insert_one(user)
        # db.credentials.insert_one({'_id':e.inserted_id,'idToken':'' })
        config = {"_id":e.inserted_id,"language":lang}
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
        
        response = requests.post(f'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={firebaseApiKey}',json.dumps({
            'email':email,
            'password': password,
            "returnSecureToken": True 
        }))
        eprint(response.content)
        jsResponse = response.json() 
        if(response.status_code != 200):
            if(jsResponse['error']['message'] == 'INVALID_PASSWORD'):
                return '{"result":"invalid password"}'
            elif(jsResponse['error']['message'] == 'EMAIL_NOT_FOUND'):
                return '{"result":"usuario inexistente"}'
            else:
                return '{"result":"no se"}'
        email = response.json()['email']
        eprint(email)
        user = db['users'].find_one({"email":email})
        eprint(user)
        if(not user):
            return '{"result":"usuario inexistente"}'

        # token = generateToken(user['_id'])
        token = generateToken(user['_id'],jsResponse.get('idToken'))
        response = {"result":"ok","uid":convertId(user['_id']),"token":token['token'],
                    "expires":token['expires']}
        eprint(response)
        return json.dumps(response)
        # valid = argon2.check_password_hash(user['password'],password)
        # if(valid):
        #     token = generateToken(user['_id'])
        #     response = {"result":"ok","uid":convertId(user['_id']),"token":token['token'],
        #                 "expires":token['expires']}
        #     return json.dumps(response)
        # else:
        #     return '{"result":"invalid password"}'
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

@auth.route('/reset-password',methods = ['POST'])
def reset_password():
    email = request.json.get('email','')
    response = requests.post(f'https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={firebaseApiKey}',
    json.dumps({"requestType":"PASSWORD_RESET","email":email}))
    if(response.status_code == 200):
        return json.dumps({'result':'ok'})
    else:
        return json.dumps({'result':'error','error':response.json()})
