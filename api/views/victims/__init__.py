#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections

from flask import jsonify, request

from api import app, db
from api.views.auth import login_required

from api.models import Incident
from api.models import states

from api.config import log


@app.route('/veris/victims', methods=['GET'])
@login_required
def victims():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    try:
        vics = {}
        victims = db.verisbase.find({}, {'_id': 0})
        for v in victims:
            vic = Incident(v).victim

            if vic.victim_id is not None:
                vics['%s' % vic.industry] = '%s' % vic.victim_id

        vic_list = collections.defaultdict(list)

        for ind, vic in vics.iteritems():
            vic_list['%s' % ind].append('%s' % vic)

        sorted_vics = sorted([d for d in vic_list.values()])
        log.debug('[!] %d Found Victims, Returning 200 Response.' % \
            len(sorted_vics))

        return jsonify({ 'Response' : 'Success', 'Victims': sorted_vics }), 200

    except Exception, error:
        log.error('[-] Error Handling: %s. %s' % (request.path, error))
        return jsonify({ 'Response' : 'Error' }), 500


@app.route('/veris/victim', methods=['POST'])
@login_required
def victim():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    try:
        req = request.form.get('victim')
        log.debug('[!] Request Input From Form: %s' % req)

        if req is not None:
            vics = {}

            details = db.verisbase.find({"victim.victim_id":{"$regex":'%s' % \
                req, "$options": "-i"}}, {'_id': 0})

            victim = [d for d in details]
            log.debug('[!] %d Victims Found.' % len(victim))
            if len(victim) > 0:
                return jsonify({'Response':'Success',
                    'Victim Search Result': victim}), 200

            else:
                return jsonify({'Response':'Success',
                    'Victim Search Result': 'No Result Found.'}), 200

        else:
            return jsonify({'Response':'Error',
                'Message':'Missing {victim} parameter. Not found.'}), 400

    except Exception, error:
        log.error('[-] Error Handling %s. %s' % (request.path, error))
        return jsonify({ 'Response' : 'Error' }), 500


@app.route('/veris/victims/industry', methods=['POST'])
@login_required
def by_industry():
    vics = []
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    try:
        req_industry = request.form.get('industry')
        log.debug('[!] Request Input From Form: %s' % req_industry)

        if req_industry is not None:
            records = db.verisbase.find({}, {'_id': 0})
            for record in records:

                industry = record.get('victim').get('industry')
                if req_industry == industry:
                    vics.append(record)

            log.debug('[!] %d Victim Matches Found.' % len(vics))
            return jsonify({'Response' : 'Success',
                'Incident' : req_industry, 'Results' : vics}), 200
        else:
            return jsonify({'Response':'Error',
                'Message':'Missing {industry} parameter. Not found.'}), 400

    except Exception, error:
        log.error('[-] Error Handling %s. %s' % (request.path, error))
        return jsonify({ 'Response' : 'Error' }), 500


@app.route('/veris/victims/geo', methods=['GET'])
@login_required
def victims_count():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    try:
        query = db.verisbase.find({}, {'_id': 0})
        victims = [Incident(res).victim for res in query]

        results = {}
        for vic in victims:

            if vic.country and vic.state is not None:
                _state = states.state_map.get('%s' % vic.state)
                _location = '%s, %s' % (_state, vic.country)

                if results.has_key('%s' % _location):
                    results['%s' % _location].append('%s' % vic.victim_id)
                else:
                    results['%s' % _location] = ['%s' % vic.victim_id]

            else:
                results['country: %s' % vic.country] = ['%s' % vic.victim_id]

        log.debug('[!] %d Locations Found.' % len(results.keys()))
        return jsonify({ 'Response' : 'Success', 'Results' : results }), 200

    except Exception, error:
        log.error('[-] Error Handling %s. %s' % (request.path, error))
        return jsonify({ 'Response' : 'Error' }), 500
