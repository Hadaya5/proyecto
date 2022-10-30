#!/usr/bin/env python
import flask
from flask import render_template
from pymongo import MongoClient
from flask import request
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

app = flask.Flask(__name__)


def get_database():
 
   CONNECTION_STRING = "mongodb://root:password@mongo:27017/miapp?authSource=admin"
 
   client = MongoClient(CONNECTION_STRING,serverSelectionTimeoutMS=1000)

   return client['facebook']
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/signup',methods = ['GET', 'POST'])
def sign():
    if(request.method == 'GET'):
        return render_template('signup.html')
    try:
        db = get_database()
        collection = db['usuarios']
        usuarios = collection.find()
        return render_template('usuarios.html',usuarios=usuarios)
    except Exception as e:
        eprint(e)
        return "Error conectando con la base de datos"
@app.route('/crear',methods = ['GET', 'POST'])
def crearUsuario():
    if (request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        mail = request.form.get('mail')
        
        db = get_database()
        usuarios = db['usuarios']
        

        if(list(usuarios.find({"username":username})) ):
            return "Error, nombre no disponible"
        elif(list(usuarios.find({"mail":mail})) ):
            return "Error, correo usado"
        user = {
            "username":username,
            "password":password,
            "mail":mail
        }
        try:
            usuarios.insert_many([user]) 
        except Exception as e:
            eprint(e)
            return 'Error conectando con la base de datos'

        return render_template('exito.html')
    else:
        return render_template('crear.html')
@app.route('/login',methods = ['GET', 'POST'])
def login():
    if (request.method == 'POST'):
        password = request.form.get('password')
        mail = request.form.get('mail')
        try:
            db = get_database()
        except Exception as e:
            eprint(e)
            return 'Error conectando con la base de datos'
        
        usuarios = db['usuarios']
        
        users = list(usuarios.find({"mail":mail}))
        print(users)
        if(not users ):
            return "Error, el email no esta registrado"
        user = users[0]

        if(str(user['password']) == str(password) ):
            return "Bienvenido " + user['username'] 
        else:
            return "Error, contraseña incorrecta"
    else:
        return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')     # open for everyone