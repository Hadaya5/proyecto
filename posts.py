from flask import render_template
from flask import request,Flask
import sys
import json
from db import savePost,checkToken,getUser
from flask import Blueprint,redirect
from config import supported_languages,text,schemas
from jsonschema import validate
from datetime import datetime
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
        'uid': uid
    }
    if(len(request.files)):
        post['file'] = request.files.get('file')  
    post['privacity'] = request.form.get("privacity")
    savePost(post)
    eprint(post)
    return ''