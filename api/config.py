#!/usr/bin/python

import os
import ConfigParser
import logging

def SectionMap(section):
    configs = {}
    options = Config.options(section)
    for option in options:
        try:
            configs[option] = Config.get(section, option)
            if configs[option] == -1:
                print("[!] skip: %s" % option)
        except Exception, error:
            print("[-] Exception on %s! Error: %s." % (option, error))
            configs[option] = None
    return configs

Config = ConfigParser.ConfigParser()
Config.read("%s/veris.app.conf" % os.path.abspath('.'))

log = logging.getLogger(__name__)

handler = logging.FileHandler('%s/log/veris.log' % os.path.abspath('.'))
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
log.setLevel(logging.DEBUG)
log.addHandler(handler)

# Veris Config
json_path = SectionMap('veris')['json_path']

# Mongo Config
mongo_host = SectionMap('mongo')['mongo_host']
mongo_port = SectionMap('mongo')['mongo_port']
mongo_user = SectionMap('mongo')['mongo_user']
mongo_pass = SectionMap('mongo')['mongo_pass']
mongo_mech = SectionMap('mongo')['mongo_mech']
veris_db = SectionMap('mongo')['veris_db']
veris_collection = SectionMap('mongo')['veris_collection']
