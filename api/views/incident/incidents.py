#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request

from api import app, db
from api.views.auth.authenticator import login_required
from api.config import log

from api.models.models import Incident

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
                        'Message':'Missing {incident} parameter. Not found'})


@app.route('/veris/incident/industry', methods=['POST'])
@login_required
def by_vertical():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    req = request.form.get('industry')
    if req is not None:
        incidents = db.verisbase.find({'victim.industry': req}, {'_id': 0})

        all_incidents = [Incident(inc) for inc in incidents]

        incidents = {}
        for incident in all_incidents:

            if incidents.has_key(incident.industry):
                incidents[incident.industry].append(incident.company)
            else:
                incidents[incident.industry] = [incident.company]

        return jsonify({ 'Response' : 'Success', 'Results' : incidents })
    else:
        return jsonify({'Response':'Error',
                        'Message':'Missing "industry" parameter. Not found.'})
