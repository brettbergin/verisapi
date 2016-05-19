#!/usr/bin/env python

import os
import glob
import subprocess
import json
from pymongo import Connection

from api import db
from api.config import json_path, log, veris_db, veris_collection


class SaveVerisData(object):
    def __init__(self):
        pass

    def _json_files(self):
        return glob.glob1(json_path, '*.json')

    def _read_json(self, infile):
        with open('{}'.format(json_path + infile), 'r') as fp:
            json_data = fp.read()
        return json_data

    def save(self):
        ctr = 0
        for json_file in self._json_files():
            ctr += 1
            log.debug("[+] Processing %d/%d: %s." % \
                (ctr, len(self._json_files()), json_file))
            db.verisbase.insert(json.loads(self._read_json(json_file)))
        return

    def clear_collection(self):
        c = Connection()
        c['%s' % veris_db].drop_collection('%s' % veris_collection)
        return
