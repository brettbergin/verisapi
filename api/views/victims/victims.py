#!/usr/bin/env python

from flask import jsonify
from flask import request

from api import app
from api import db
from api.views.auth.authenticator import login_required
from api.models.models import Victim
from api.config import log

@app.route('/veris/victims', methods=['GET'])
@login_required
def victims():
    vics = {}
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    victims = db.verisbase.find({}, {'victim.': 1, '_id': 0})
    for v in victims:
        vic = Victim(v)
        vics['%s' % vic.industry] = '%s' % vic.victim_id

    return jsonify({'Response' : 'Success', 'Victims': vics})

@app.route('/veris/industry', methods=['POST'])
@login_required
def by_industry():
    vics = []
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    req_industry = request.form.get('victim')
    if req_industry is not None:
        records = db.verisbase.find({}, {'_id': 0})
        for record in records:

            industry = record.get('victim').get('industry')
            if req_industry == industry:
                vics.append(record)

        return jsonify({'Response' : 'Success',
                       'Incident' : req_industry,
                       'Results' : vics})
    else:
        return jsonify({'Response':'Error',
                        'Message':'Missing "victim" parameter. Not found.'})
