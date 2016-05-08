#!/usr/bin/env python

from dateutil import parser
from collections import Counter

from flask import jsonify
from flask import request

from api import app
from api import db
from api.views.auth.authenticator import login_required
from api.config import log

import states


@app.route('/veris/newest', methods=['GET'])
@login_required
def newest():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    query = db.verisbase.find({}, {'plus': 1, '_id': 0})
    create_dates = [res['plus'].get('created') for res in query]

    parsed = sorted(list(set([parser.parse(dates, ignoretz=True) \
        for dates in create_dates if dates is not None])))

    ten_newest = [d.strftime('%H:%M:%S %m/%d/%Y') for d in parsed[-10:]][::-1]

    return jsonify({'Response' : 'Success',
                    'Top Ten Recently Created': ten_newest})


@app.route('/veris/actions/count', methods=['GET'])
@login_required
def action_count():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    actions = []
    query = db.verisbase.find({}, {'action': 1, '_id': 0})
    all_actions = [res['action'].keys() for res in query]

    [actions.extend(act) for act in all_actions if act not in actions]

    return jsonify({ 'Response' : 'Success',
                        'Actions By Count': Counter(actions)})


@app.route('/veris/victims/geo', methods=['GET'])
@login_required
def victims_count():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    query = db.verisbase.find({}, {'victim': 1, '_id': 0})

    all_victims = [res['victim'] for res in query \
                    if res['victim'].get('victim_id') is not None]

    results = {}

    for victim in all_victims:
        vic = victim['victim_id']
        country, state = victim.get('country'), victim.get('state')

        if country and state is not None:
            state = states.states.get('%s' % state)
            results['%s' % vic] = "%s, %s" % (state, country[0])

        else:
            results['%s' % vic] = "country: %s" % country[0]

    return jsonify({ 'Response' : 'Success', 'Results' : results })
