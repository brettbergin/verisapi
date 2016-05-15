#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib
from flask import request, jsonify, abort, url_for

from api import app
from api.views.auth.authenticator import login_required
from api.config import log


@app.route('/', methods=['GET'])
@login_required
def index():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    return jsonify({'Response': abort(403)})


@app.route('/veris/routes', methods=['GET'])
@login_required
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    return jsonify({'Reponse' : 'Success',
                        'Results' : output })
