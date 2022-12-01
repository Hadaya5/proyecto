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
from utils import remove_oid
from bson import json_util as bson
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


@user.route('/perfil/<userid>',methods = ['GET','PUT'])
@user.route('/perfil/',methods = ['GET','PUT'])
def profile(userid=None):
    uid = checkLogin(request)
    if(not uid):
        lang = request.accept_languages.best_match(supported_languages)    
        return render_template('notloged.html',text=text[lang])

    lang = getLanguage(uid)
    if(userid):
        user = getUser( db.convertId(userid) )
        if(not user):
            return render_template('404.html',text=text[lang])
        else:
            return render_template('profile.html',text=text[lang],user=user,editable=False,posts=db.getFriendsPosts([db.convertId(userid) ]),users=db.getUsersDict(user['friends'] + [user['_id']]))
    else:
        user = getUser(uid)
        return render_template('profile.html',text=text[lang],user=user,editable=True,posts=db.getFriendsPosts([uid]),users=db.getUsersDict(user['friends'] + [user['_id']]))

@user.route('/notifications',methods = ['GET'])
def notifications():
    uid = checkLogin(request)

    if(not uid):
        lang = request.accept_languages.best_match(supported_languages)    
        return render_template('notloged.html',text=text[lang])
    lang = getLanguage(uid)
    notifications = db.getUserNotifications(uid)
    return render_template('notificaciones.html',text=text[lang],notifications=notifications)

@user.route('/manage',methods = ['GET'])
def manage():
    uid = checkLogin(request)
    if(not uid):
        lang = request.accept_languages.best_match(supported_languages)    
        return render_template('notloged.html',text=text[lang])

    user = getUser(uid)
    user['friends'] = db.getUsers(user['friends'])
    user['blocks'] = db.getUsers(user['blocks'])
    if(request.method == 'GET'):
        lang = request.accept_languages.best_match(supported_languages)  
        return render_template('manage.html',text=text[lang],user=user)

@user.route('/search',methods = ['GET'])
def search():
    uid = checkLogin(request)
    if(not uid):
        lang = request.accept_languages.best_match(supported_languages)    
        return render_template('notloged.html',text=text[lang])
    else:
        lang = getLanguage(uid)
    query = request.args.get('query','').lower()
    users = db.getAllUsers()
    user = getUser(uid)
    results = []
    for i in users:
        name = i['name'].lower()
        lastname = i['lastname'].lower()
        full = name + ' ' + lastname
        eprint(query,name)
        if(name.startswith(query) or lastname.startswith(query) ):
            results.append(i)
            eprint('epa si esta')
    
    # return remove_oid( bson.dumps(results) )
    eprint(results)
    return render_template('search.html',text=text[lang],resultUsers=results,friends=user['friends'])
@user.route('/user/<action>',methods = ['GET','POST','PUT','DELETE'])
def friends(action):
    uid = checkLogin(request)
    if(not uid):
        lang = request.accept_languages.best_match(supported_languages)    
        if(not lang):
            lang = 'en'
        return render_template('notloged.html',text=text[lang])

    user = getUser(uid)
    if(action == 'friends'):
        users = user['friends']
    elif(action == 'blocks'):
        users = user['blocks']
    else:
        return '{"result":"error"}'


    # user['blocks'] = db.getUsers(user['blocks'])
    if(request.method == 'GET'):
        users = db.getUsers(users)
        return remove_oid( bson.dumps( users ) ),200,{'Content-Type':'application/json'}

    if(request.method == 'DELETE'):
        friend = request.args.get('user')
        if(not friend):
            return '{"result":"bad request"}',400
        friend = db.convertId(friend)
        if(friend not in users):
            return '{"result":"friend not exist"}',400
        users.remove(friend)
        db.saveFriends(uid,users,action)
        return bson.dumps( db.getUsers(users) )

    if(request.method == 'POST'):
        print(request.json)
        friend = request.json.get('user')
        if(not friend):
            return '{"result":"bad request"}',400
        friend = db.convertId(friend)
        if(friend in users):
            return '{"result":"user already there"}',400
        users.append(friend)
        if(action == 'blocks'):
            friends = user['friends']
            if(friend in friends):
                friends.remove(friend)
                db.saveFriends(uid,friends,'friends')            
            friends = db.getUser(friend)['friends']
            if(uid in friends):
                friends.remove(uid)
                db.saveFriends(friend,friends,'friends')            

        db.saveFriends(uid,users,action)
        if(action == 'friends'):
            db.addFriend(friend,uid)
            db.addNotification(friend,'You got a new friend: ' + user['name'],user['icon'],'/perfil/' + db.convertId(user['_id']))
        
        return bson.dumps( db.getUsers(users) )
    elif(request.method == 'PUT'):
        users = request.json.get('users')
        if(not users):
            return '{"result":"error"}',400
        users = db.convertId(users)
        db.saveFriends(uid,users,action)
        return remove_oid( bson.dumps( db.getUsers(users) ) )
