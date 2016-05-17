#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dateutil import parser
from collections import Counter

from flask import jsonify, request

from api import app, db
from api.views.auth.authenticator import login_required
from api.config import log
from api.models.models import Victim, Action

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


@app.route('/veris/actions/types', methods=['GET'])
@login_required
def types_actions():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    query = db.verisbase.find({}, {'action': 1, '_id': 0})
    all_actions = [Action(action) for action in query]

    actions = {}
    for action in all_actions:

        if actions.has_key(action.type):
            actions[action.type].append({ 'vector' : action.vector, 'variety' : action.variety })
        else:
            actions[action.type] = [{ 'vector' : action.vector, 'variety' : action.variety }]

    return jsonify({ 'Response':'Success', 'Results': actions })


@app.route('/veris/victims/geo', methods=['GET'])
@login_required
def victims_count():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    query = db.verisbase.find({}, {'victim': 1, '_id': 0})
    victims = [Victim(res) for res in query]

    results = {}
    for vic in victims:
        if vic.country and vic.state is not None:
            _state = states.states.get('%s' % vic.state)
            _location = '%s, %s' % (_state, vic.country)

            if results.has_key(_location):
                results[_location].append('%s' % vic.victim_id)
            else:
                results[_location] = ['%s' % vic.victim_id]

        else:
            results['country: %s' % vic.country] = ['%s' % vic.victim_id]
    return jsonify({ 'Response' : 'Success', 'Results' : results })
