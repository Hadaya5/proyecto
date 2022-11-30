from flask import render_template
from flask import request,Flask
import sys
import json
from db import checkToken, getUser, getUserProfile, getLanguage,setConfig
import db
from flask import Blueprint
from config import supported_languages,text,schemas
from jsonschema import validate
from datetime import datetime
from config import text,firebaseApiKey
import requests
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

user = Blueprint('user', __name__)

def checkLogin(request):
    token = request.cookies.get('token','')
    uid = checkToken(token)
    return uid


@user.route('/config',methods = ['GET', 'POST'])
def configuracion():
    uid = checkLogin(request)
    if(not uid):
        lang = request.accept_languages.best_match(supported_languages)    
        return render_template('notloged.html',text=text[lang])
    if(request.method == 'GET'):
        lang = getLanguage(uid)
        user = getUser(uid)
        return render_template('configuracion.html',text=text[lang],lang=lang,user=user)
    elif(request.method == 'POST'):
        config = request.json.get('config')
        setConfig(uid,config)
        response = {
            "result":"ok",
            "message":""
        }
        return json.dumps(response)
@user.route('/edit',methods = ['POST'])
def edit():
    uid = checkLogin(request)
    if(not uid):
        lang = request.accept_languages.best_match(supported_languages)    
        return render_template('notloged.html',text=text[lang])
    if(request.method == 'POST'):
        config = request.json.get('config')
        idToken = request.cookies.get('token','')
        if('password' in config):
            response = requests.post(f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={firebaseApiKey}",{
                'idToken': idToken,
                'password': config['password'],
                'returnSecureToken': True
            })
            eprint(idToken)
            eprint(response.content)
            if(response.status_code != 200):
                return {
                    "result":"error",
                    "message":response.json().get('error',{}).get('message','')
                }
            else:
                try:
                    jsResponse = json.loads(response.text)
                except Exception as e:
                    eprint(e)
                    eprint('json not accepted')
                    raise e
                idToken = jsResponse['idToken']
                token = db.generateToken(uid,idToken)
                return {
                    'result':"ok",
                    'token':token
                }

        eprint(config)
        db.setUserConfig(uid,config)
        response = {
            "result":"ok",
            "message":""
        }
        return json.dumps(response)


@user.route('/perfil',methods = ['GET','PUT'])
def profile():
    uid = checkLogin(request)
    if(not uid):
        lang = request.accept_languages.best_match(supported_languages)    
        return render_template('notloged.html',text=text[lang])

    user = getUser(uid)
    profile = getUserProfile(uid)
    lang = getLanguage(uid)
    return render_template('profile.html',text=text[lang],user=getUser(uid),profile=getUserProfile(uid))
@user.route('/notifications',methods = ['GET'])
def notifications():
    uid = checkLogin(request)

    if(not uid):
        lang = request.accept_languages.best_match(supported_languages)    
        return render_template('notloged.html',text=text[lang])
    lang = getLanguage(uid)

    return render_template('notificaciones.html',text=text[lang])
