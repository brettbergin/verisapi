#!/usr/bin/env python


class Victim(object):
    def __init__(self, victim):
        self.victim = victim.get('victim')
        self.victim_id = self.victim.get('victim_id')
        self.country = self.victim.get('country')
        self.state = self.victim.get('state')
        self.region = self.victim.get('region')
        self.employee_count = self.victim.get('employee_count')
        self.industry = self.victim.get('industry')
