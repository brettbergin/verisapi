#!/usr/bin/env python


class Victim(object):

    def __init__(self, victim):
        self.victim = victim.get('victim')
        self.victim_id = self.victim.get('victim_id')
        self.country = self.victim.get('country')[0]
        self.state = self.victim.get('state')
        self.region = self.victim.get('region')
        self.employee_count = self.victim.get('employee_count')
        self.industry = self.victim.get('industry')


class Action(object):

    def __init__(self, action):
        self.action = action.get('action')
        self.type = self.action.keys()[0]

        if self.action['%s' % self.type].get('vector') is not None:
            self.vector = self.action['%s' % self.type]['vector'][0]
        else:
            self.vector = None

        if self.action['%s' % self.type].get('variety') is not None:
            self.variety = self.action['%s' % self.type]['variety'][0]
        else:
            self.variety = None


class Incident(object):
    
    def __init__(self, incident):
        self.victim = incident.get('victim')
        self.incident_id = incident.get('incident_id')
        self.company = self.victim.get('victim_id')
        self.industry = self.victim.get('industry')
