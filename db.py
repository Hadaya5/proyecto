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
    else:
        return ObjectId(x)
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_database():
 
    CONNECTION_STRING = f"mongodb://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}?authSource=admin"
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
def generateToken(userid):
    db = get_database()    
    tokens = db['tokens']
    token = {
        'uid':userid,
        'expires': datetime.utcfromtimestamp(datetime.utcnow().timestamp()+api_config['token_duration']).isoformat(),
        'token': secrets.token_urlsafe(32)
    }
    result = tokens.insert_one(token)
    # return result.inserted_id.binary.hex().upper()
    return token
    
def savePost(post):
    db = get_database()    
    posts = db['posts']
    post['timestamp'] = int(time())
    posts.insert_one(post)
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