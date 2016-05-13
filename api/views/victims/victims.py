#!/usr/bin/env python

import re
import collections

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
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    vics = {}
    victims = db.verisbase.find({}, {'victim': 1, '_id': 0})
    for v in victims:
        vic = Victim(v)

        if vic.victim_id is not None:
            vics['%s' % vic.industry] = '%s' % vic.victim_id

    vic_list = collections.defaultdict(list)

    for ind, vic in vics.iteritems():
        vic_list['%s' % ind].append('%s' % vic)

    sorted_vics = sorted([d for d in vic_list.values()])
    return jsonify({'Response' : 'Success', 'Victims': sorted_vics})


@app.route('/veris/victim', methods=['POST'])
@login_required
def victim():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    req = request.form.get('victim')
    if req is not None:
        vics = {}

        details = db.verisbase.find({"victim.victim_id":{"$regex":'%s' % req,
                                        "$options": "-i"}}, {'_id': 0})

        victim = [d for d in details]
        if len(victim) > 0:
            return jsonify({'Response':'Success',
                                'Victim Search Result': victim})

        else:
            return jsonify({'Response':'Success',
                        'Search Result': 'No Result Found.'})
    else:
        return jsonify({'Response':'Error',
                        'Message':'Missing {victim} parameter. Not found.'})        


@app.route('/veris/industry', methods=['POST'])
@login_required
def by_industry():
    vics = []
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    req_industry = request.form.get('industry')
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
                        'Message':'Missing {industry} parameter. Not found.'})
