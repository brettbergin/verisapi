#!/usr/bin/env python

from flask import jsonify
from flask import request

from api import app
from api import db
from api.views.auth.authenticator import login_required
from api.config import log


@app.route('/veris/incidents', methods=['GET'])
@login_required
def incidents():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    incidents = db.verisbase.find({}, {'incident_id': 1, '_id': 0})
    return jsonify({'Response' : 'Success',
                    'Incident Ids': [str(i['incident_id']) for i in incidents]})


@app.route('/veris/incident', methods=['POST'])
@login_required
def by_incident():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    req = request.form.get('incident')
    if req is not None:
        incidents = db.verisbase.find({'incident_id': req}, {'_id': 0})
        return jsonify({'Response' : 'Success',
                        'Incident' : req,
                        'Results' : [i for i in incidents]})
    else:
        return jsonify({'Response':'Error',
                        'Message':'Missing "incident" parameter. Not found.'})
