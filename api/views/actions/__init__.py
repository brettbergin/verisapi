#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter

from flask import jsonify, request

from api import app, db
from api.views.auth import login_required
from api.config import log

from api.models import Incident

@app.route('/veris/actions/count', methods=['GET'])
@login_required
def action_count():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    try:
        incidents = db.verisbase.find({}, {'_id': 0})
        actions = [Incident(i).action.type for i in incidents]
        log.debug('[!] %d=len(actions)' % len(actions))
        return jsonify({ 'Response' : 'Success',
            'Actions By Count': Counter(actions)}), 200

    except Exception, error:
        log.error('[-] Error Handling %s. %s' % (request.path, error))
        log.debug('[!] %d=len(actions), %d=len([i for i in incidents])' % \
            (len(actions), len([i for i in incidents])))

        return jsonify({ 'Response' : 'Error' }), 500


@app.route('/veris/actions/types', methods=['GET'])
@login_required
def types_actions():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    try:
        incidents = db.verisbase.find({}, {'_id': 0})
        all_actions = [Incident(i).action for i in incidents]

        log.debug('[!] %d Total actions found.' % len(all_actions))

        actions = {}
        for action in all_actions:

            if actions.has_key('%s' % action.type):
                actions['%s' % action.type].append({ 'vector' : action.vector, 'variety' : action.variety })
            else:
                actions['%s' % action.type] = [{ 'vector' : action.vector, 'variety' : action.variety }]

        log.debug('[!] %d Action Types Found.' % len(actions.keys()))
        return jsonify({ 'Response':'Success', 'Results': actions }), 200

    except Exception, error:
        log.error('[!] Error Handling %s. %s' % (request.path, error))
        return jsonify({ 'Response' : 'Error' }), 500
