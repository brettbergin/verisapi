#!/usr/bin/env python

import os
import glob
import subprocess
import json

from api import db
from api.config import json_path
from api.config import log


class SaveVerisData(object):
    def __init__(self):
        pass

    def _json_files(self):
        return glob.glob1(json_path, '*.json')

    def _read_json(self, infile):
        fp = open("%s" % (json_path + infile), 'r')
        json_data = fp.read()
        fp.close()
        return json_data

    def save(self):
        ctr = 0
        for json_file in self._json_files():
            ctr += 1
            print("[+] Processing %d/%d: %s." % \
                (ctr, len(self._json_files()), json_file))
            db.verisbase.insert(json.loads(self._read_json(json_file)))
        return
