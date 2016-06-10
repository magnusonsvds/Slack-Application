import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from Config import basedir

from datetime import datetime

from model import slack_user, message_channel, message

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI']
slackconnect = Slacker(app.config["slack_api_token"])

from app import views, models