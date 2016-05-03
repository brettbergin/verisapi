#!/usr/bin/env python

from flask import jsonify
from flask import request
from flask import Response

from functools import wraps
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from verisapi import app
from verisapi import db

from verisapi.config import log

@app.route('/veris/signup', methods=['POST'])
def signup():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    if request.form.get('username') is not None:
        if request.form.get('password') is not None:

            db.users.insert({'username': request.form.get('username'),
            'password': generate_password_hash(request.form.get('password'))})
            
            return jsonify({'Response': 'User Successfully Created.'})

        else:
            return jsonify({'Response': 'Password Was Not Supplied.'})
    else:
        return jsonify({'Response': 'Username Was Not Supplied.'})

def check_auth(username, password):
    res = db.users.find_one({'username': username})
    if res is not None:
        chk = check_password_hash(res['password'], password)
        if chk:
            return chk

def authenticate():
    return Response(
    'Invalid Credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated
