#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from pymongo import MongoClient

import config

app = Flask(__name__)

mongo_conn = 'mongodb://' + config.mongo_host + ':' + config.mongo_port + '/'
mongo = MongoClient(mongo_conn)

db = mongo.veris # where veris = databasename

db.authenticate(config.mongo_user,
                config.mongo_pass,
                mechanism=config.mongo_mech)

import views.base.base
import views.auth.authenticator
import views.load.loader
import views.incident.incidents
import views.victims.victims
import views.trends.trends
