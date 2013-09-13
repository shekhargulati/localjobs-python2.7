import os
from flask import Flask
import pymongo
from pymongo import MongoClient
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SECRET_KEY'] = 'secret_key'

MONGODB_DB_URL = os.environ.get('OPENSHIFT_MONGODB_DB_URL') if os.environ.get('OPENSHIFT_MONGODB_DB_URL') else 'mongodb://localhost:27017/'
MONGODB_DB_NAME = os.environ.get('OPENSHIFT_APP_NAME') if os.environ.get('OPENSHIFT_APP_NAME') else 'localjobs'

client = MongoClient(MONGODB_DB_URL)
db = client[MONGODB_DB_NAME]

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'signin'

import views
import models