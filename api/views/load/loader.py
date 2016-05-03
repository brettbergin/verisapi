#!/usr/bin/env python

from flask import jsonify

from verisapi import app
from verisapi.views.auth.authenticator import login_required
from verisapi.backends.LoadMongoWithVeris import SaveVerisData

from verisapi.config import log

@app.route('/veris/load', methods=['GET'])
@login_required
def load_veris():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))
        
    loader = SaveVerisData()
    loader.save()
    return jsonify({'LoaderResponse' : 'Successfully Loaded.'})
