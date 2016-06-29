import os, configparser
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from slacker import Slacker
from flask_bootstrap import Bootstrap


app = Flask(__name__, instance_relative_config=True)

app.route
Bootstrap(app)
db = SQLAlchemy(app)

#Default config
app.config.from_object('config.default')
#Secret keys in config
app.config.from_pyfile('config.py')
#Enviroment variables. Either production or development.
app.config.from_envvar('APP_CONFIG_FILE')

app.config['SQLALCHEMY_DATABASE_URI']
app.config['CSRF_ENABLED']
app.config['SECRET_KEY']
app.config['DEBUG']

slackconnect = Slacker(app.config['SLACK_API_TOKEN'])

from app import views
from app.channel import Channel
from app.user import User
from app.message_class import Message_Class
from app.model import slack_user, message_channel, message