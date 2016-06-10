import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from Config import basedir

from datetime import datetime


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from slacker import Slacker
from channel import Channel
from user import User
from message import Message
from model import slack_user, message_channel, message


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']
slackconnect = Slacker(app.config["slack_api_token"])

from app import views, models