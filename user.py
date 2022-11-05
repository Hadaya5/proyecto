from flask import render_template
from flask import request,Flask
import sys
import json
from db import checkToken, getUser, getUserProfile, getLanguage,setConfig
from flask import Blueprint
from config import supported_languages,text,schemas
from jsonschema import validate
from datetime import datetime
from config import text
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
        return render_template('configuracion.html',text=text[lang],lang=lang)
    elif(request.method == 'POST'):
        config = request.json.get('config')
        setConfig(uid,config)
        response = {
            "result":"ok",
            "message":""
        }
        return json.dumps(response)
@user.route('/perfil',methods = ['GET'])
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
