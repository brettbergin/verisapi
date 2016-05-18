#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request, Response

from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

from api import app, db
from api.config import log


@app.route('/veris/register', methods=['POST'])
def register():
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
