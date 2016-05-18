#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request
from api import app
from api.views.auth import login_required
from api.backends.LoadMongoWithVeris import SaveVerisData
from api.config import log


@app.route('/veris/load', methods=['GET'])
@login_required
def load_veris():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    loader = SaveVerisData()
    loader.clear_collection()
    loader.save()
    return jsonify({'LoaderResponse' : 'Successfully Loaded.'})
