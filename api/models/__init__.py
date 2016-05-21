#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Asset(object):

    def __init__(self, assets):

        self.assets = assets.get('assets')

        if self.assets is not None:
            self.variety = [i.get('variety') for i in self.assets]
        else:
            self.variety = None


class Victim(object):

    def __init__(self, victim):

        self.victim_id = victim.get('victim_id')
        self.country = victim.get('country')[0]
        self.state = victim.get('state')
        self.region = victim.get('region')
        self.employee_count = victim.get('employee_count')
        self.industry = victim.get('industry')


class Action(object):

    def __init__(self, action):

        self.type = action.keys()[0]

        if action['%s' % self.type].get('vector') is not None:
            self.vector = action['%s' % self.type]['vector'][0]
        else:
            self.vector = None

        if action['%s' % self.type].get('variety') is not None:
            self.variety = action['%s' % self.type]['variety'][0]
        else:
            self.variety = None


class Timeline(object):

    def __init__(self, timeline):

        self.incident = timeline.get('incident')
        self.day = self.incident.get('day')
        self.month = self.incident.get('month')
        self.year = self.incident.get('year')

        if self.day and self.month and self.year is not None:
            self.full_date = '%s-%s-%s' % (self.month, self.day, self.year)
        else:
            self.full_date = None


class Plus(object):

    def __init__(self, plus):

        self.dbir_year = plus.get('dbir_year')
        self.created = plus.get('created')
        self.modified = plus.get('modified')
        self.analysis_status = plus.get('analysis_status')
        self.master_id = plus.get('master_id')
        self.analyst = plus.get('analyst')


class Actor(object):

    def __init__(self, actor):

        self.actor_type = actor.keys()[0]

        if actor['%s' % self.actor_type].get('motive') is not None:
            self.motive = actor['%s' % self.actor_type].get('motive')[0]
        else:
            self.motive = None

        if actor['%s' % self.actor_type].get('country') is not None:
            self.country = actor['%s' % self.actor_type].get('country')[0]
        else:
            self.country = None

        if actor['%s' % self.actor_type].get('region') is not None:
            self.region = actor['%s' % self.actor_type].get('region')[0]
        else:
            self.region = None

        if actor['%s' % self.actor_type].get('variety') is not None:
            self.variety = actor['%s' % self.actor_type].get('variety')[0]
        else:
            self.variety = None


class Attribute(object):

    def __init__(self, attr):

        self.availability = attr.get('availability')
        self.confidentiality = attr.get('confidentiality')
        self.state = attr.get('state')
        self.data_victim = attr.get('data_victim')
        self.data_disclosure = attr.get('data_disclosure')


class Incident(object):

    def __init__(self, incident):

        self.incident_id = incident.get('incident_id')
        self.reference = incident.get('reference')
        self.discovery_method = incident.get('discovery_method')
        self.summary = incident.get('summary')
        self.source_id = incident.get('source_id')
        self.security_incident = incident.get('security_incident')
        self.schema_version = incident.get('schema_version')

        self.victim = Victim(incident.get('victim'))
        self.action = Action(incident.get('action'))
        self.asset = Asset(incident.get('asset'))
        self.timeline = Timeline(incident.get('timeline'))
        self.plus = Plus(incident.get('plus'))
        self.actor = Actor(incident.get('actor'))
        self.attr = Attribute(incident.get('attribute'))
