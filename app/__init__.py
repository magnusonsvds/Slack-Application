import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
#from config import basedir

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from slacker import Slacker
from flask_bootstrap import Bootstrap



app = Flask(__name__)
#app.config.from_object('config')
app.route
Bootstrap(app)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1Svds@123@localhost/slacktestdb'


app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    CSRF_ENABLED = True,
))

#slackconnect = Slacker(app.config["slack_api_token"])
slackconnect = Slacker("xoxp-48585661490-48566956614-52052862306-9480abf35f")

from app import views
from app.channel import Channel
from app.user import User
from app.message_class import Message_Class
from app.model import slack_user, message_channel, message