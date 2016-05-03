#!/usr/bin/env python

from flask import request
from flask import jsonify
from flask import abort

from api import app
from api.views.auth.authenticator import login_required
from api.config import log

@app.route('/', methods=['GET'])
@login_required
def index():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    return jsonify({'Response': abort(403)})
