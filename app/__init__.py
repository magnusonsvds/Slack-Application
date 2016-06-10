import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
#from config import basedir

from datetime import datetime


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from slacker import Slacker



app = Flask(__name__)
#app.config.from_object('config')
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1Svds@123@localhost/slacktestdb'

#slackconnect = Slacker(app.config["slack_api_token"])
slackconnect = Slacker("xoxp-48585661490-48566956614-49633690839-8a11581e73")

import app.views.index, app.views.user
from app.channel import Channel
from app.user import User
from app.message import Message
from app.model import slack_user, message_channel, message