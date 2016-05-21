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

import views.base
import views.incident
import views.auth
import views.load
import views.victims
import views.actions
import views.asset
