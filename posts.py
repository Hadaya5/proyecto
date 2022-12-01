from flask import render_template
from flask import request,Flask
import sys
import json
from db import savePost,checkToken,getUser
from flask import Blueprint,redirect
from config import supported_languages,text,schemas
from jsonschema import validate
from datetime import datetime
import db
import utils
from time import time
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

post = Blueprint('post', __name__)
@post.route('/post',methods = ['POST'])
def upload():
    token = request.cookies.get('token','')
    uid = checkToken(token)
    if(not uid):
        eprint('not authorized')
        return redirect('/')    
    eprint(request.form)
    eprint(request.files)
    post = {
        'content':request.form.get('content'),
        'uid': uid,
        'comments': []
    }
    if(len(request.files)):
        f = request.files.get('file')
        filename = f.filename
        filename = db.convertId(uid) + str(time()).replace('.','') + filename 
        post['media'] = filename
        utils.compressMe(f,filename)
        # return '{"result":"test"}'
        # f.save('static/images/' + filename)
    savePost(uid,post)
    eprint(post)
    return '{"result":"ok"}'

@post.route('/comment',methods = ['POST'])
def comment():
    token = request.cookies.get('token','')
    uid = checkToken(token)
    if(not uid):
        eprint('not authorized')
        return redirect('/')  
    jsRequest = request.json
    print(jsRequest)
    comment = {
        'uid': uid,
        'content':jsRequest['content'],
        'comments': []
    }
    db.addComment(jsRequest['postid'],comment)
    return '{"result":"ok"}'
