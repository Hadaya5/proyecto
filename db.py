#!/usr/bin/env python
from pymongo import MongoClient
from time import time
from config import api_config,db_config,supported_languages
import sys
from bson.objectid import ObjectId
import secrets
from datetime import datetime,date
def convertId(x):
    if(type(x) == ObjectId):
        return x.binary.hex().upper()
    elif(type(x) == list):
        s = []
        for i in x:
            s.append(convertId(i) )
        return s
    else:
        return ObjectId(x)
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_database():
 
    CONNECTION_STRING = f"mongodb://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?authSource=admin"
    eprint(CONNECTION_STRING)
    client = MongoClient(CONNECTION_STRING,serverSelectionTimeoutMS=1000)
    return client[db_config['database']]
def checkToken(token):
    
    db = get_database()    
    tokens = db['tokens']
    token = tokens.find_one({"token":token})
    if(not token):
        return None
    if(datetime.fromisoformat(token['expires']) < datetime.utcnow()):
        tokens.delete_one({"token":token})
        return None
    else:
        token['expires'] = datetime.utcfromtimestamp(datetime.utcnow().timestamp()+api_config['token_duration']).isoformat()
        tokens.update_one({"_id":token['_id']},{"$set":{"expires":token['expires']}})
    return token['uid']
def generateToken(userid,idToken=None):
    db = get_database()    
    tokens = db['tokens']
    if(not idToken):
        token = {
            'uid':userid,
            'expires': datetime.utcfromtimestamp(datetime.utcnow().timestamp()+api_config['token_duration']).isoformat(),
            'token': secrets.token_urlsafe(32)
        }
    else:
        token = {
            'uid':userid,
            'expires': datetime.utcfromtimestamp(datetime.utcnow().timestamp()+api_config['token_duration']).isoformat(),
            'token': idToken
        }

    result = tokens.insert_one(token)
    # return result.inserted_id.binary.hex().upper()
    return token
    
def savePost(uid,post):
    db = get_database()    
    posts = db['posts']
    posts.insert_one(post)
def getUsers(uids):
    db = get_database()
    users = list(db['users'].find({'_id':{'$in':uids} },{'idToken':0,'firebaseId':0} ))
    # eprint(users)
    return users
def getFriendsPosts(uids):
    db = get_database()
    posts = db['posts'].find({"uid":{"$in":uids},"privacity":0})
    friends = db['profiles'].find({'_id': {'$in':uids } })
    return {'posts':posts,'friends':friends}
def getUser(userid):
    db = get_database()
    s = {'_id':userid}
    eprint(s)
    return db['users'].find_one(s)
    
def getUserProfile(userid):
    db = get_database()
    return db['profiles'].find_one({'_id':userid})
def revokeToken(token):
    db = get_database()
    tokens = db['tokens']
    tokens.delete_one({"token":token})
def getLanguage(userid):
    db = get_database()
    config = db['config'].find_one({'_id':userid})
    if(not config):
        eprint('error no userid')
        eprint(userid)
    lang = config.get('language','es')
    if(lang not in supported_languages):
        for l in supported_languages:
            if(l in lang):
                return l
    else:
        return lang
    return 'en'
def setConfig(userid,config):
    db = get_database()
    config = db['config'].update_one({'_id':userid},{'$set':config })
def setUserConfig(userid,config):
    db = get_database()
    config = db['users'].update_one({'_id':userid},{'$set':config })
def saveFriends(uid,friends,action='friends'):
    db = get_database()
    db['users'].update_one({'_id':uid},{'$set':{action:friends}})
# def saveBlocks(uid,blocks):
#     db = get_database()
#     db['users'].update_one({'_id':uid},{'$set':{'blocks':blocks}})