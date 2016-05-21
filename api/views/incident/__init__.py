#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dateutil import parser
from collections import Counter

from flask import jsonify, request

from api import app, db
from api.views.auth import login_required
from api.config import log

from api.models import Incident


@app.route('/veris/incidents', methods=['GET'])
@login_required
def incidents():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    try:
        query = db.verisbase.find({}, {'_id': 0})
        incidents = [Incident(incident).incident_id for incident in query]

        log.debug('[!] %d Incident Ids Found.' % len(incidents))
        return jsonify({'Response' : 'Success', 'Incident Ids': incidents}), 200

    except Exception, error:
        log.error('[-] Error Handling %s. %s' % (request.path, error))
        return jsonify({ 'Response' : 'Error' }), 500


@app.route('/veris/incident', methods=['POST'])
@login_required
def by_incident():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    try:
        req = request.form.get('incident')
        log.debug('[!] Request Input From Form: %s' % req)

        if req is not None:
            incidents = db.verisbase.find({}, {'_id': 0})

            results = []
            for i in incidents:

                if req == Incident(i).incident_id:
                    results.append(i)

            log.debug('[!] %d incidents Found.' % len(results))
            return jsonify({ 'Response' : 'Success', 'Results' : results }), 200

        else:
            return jsonify({'Response':'Error',
                'Message':'Missing {incident} parameter. Not found'}), 400

    except Exception, error:
        log.error('[-] Error Handling %s. %s' % (request.path, error))
        return jsonify({ 'Response' : 'Error' }), 500


@app.route('/veris/incident/industry', methods=['POST'])
@login_required
def by_vertical():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    try:
        req = request.form.get('industry')
        if req is not None:
            incidents = db.verisbase.find({}, {'_id': 0})

            results = []
            for i in incidents:

                if req == Incident(i).victim.industry:
                    results.append(i)

            log.debug('[!] %d Matching Industries.' % len(results))
            return jsonify({ 'Response' : 'Success', 'Results' : results }), 200

        else:
            return jsonify({'Response':'Error',
                'Message':'Missing {industry} parameter. Not found.'}), 400

    except Exception, error:
        log.error('[-] Error Handling %s. %s' % (request.path, error))
        return jsonify({ 'Response': 'Error' }), 500


@app.route('/veris/incidents/newest', methods=['GET'])
@login_required
def newest():
    log.debug('[!] %s Request To: %s From: %s' % \
        (request.method, request.path, request.remote_addr))

    try:
        query = db.verisbase.find({}, {'plus': 1, '_id': 0})
        create_dates = [res['plus'].get('created') for res in query]

        parsed = sorted(list(set([parser.parse(dates, ignoretz=True) \
            for dates in create_dates if dates is not None])))

        ten_newest = [d.strftime('%H:%M:%S %m/%d/%Y') for d in parsed[-10:]][::-1]

        log.debug('[!] %d Newest Records Found.' % len(ten_newest))
        return jsonify({'Response' : 'Success',
            'Top Ten Recently Created': ten_newest}), 200

    except Exception, error:
        log.error('[-] Error Handling %s. %s' % (request.path, error))
        return jsonify({'Response' : 'Error' }), 500
