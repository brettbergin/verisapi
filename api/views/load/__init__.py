#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request
from api import app
from api.views.auth import login_required
from api.backends import SaveVerisData
from api.config import log


@app.route('/veris/load', methods=['GET'])
@login_required
def load_veris():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    try:
        log.debug('[!] Running Veris Data Ingest.')

        loader = SaveVerisData()
        loader.clear_collection()
        loader.save()

        log.debug('[!] Ingest Complete.')
        return jsonify({'LoaderResponse' : 'Successfully Loaded.'}), 200

    except Exception, error:
        log.error('[-] Error Handling %s. %s' % (request.path, error))
        return jsonify({ 'Response' : 'Error' }), 500
