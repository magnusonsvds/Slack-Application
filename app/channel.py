from datetime import datetime
from slacker import Slacker
from slack_entries_database import db

from slack_entries_database import slack_user, message_channel, message

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1Svds@123@localhost/slacktestdb'
db = SQLAlchemy(app)

slackconnect = Slacker("xoxp-48585661490-48566956614-49307999364-419b3ccfc5")
class Channel(object):
	def __init__(self):
		self.channelInfo = []

	def getChannelInfo():
	    responseObject = slackconnect.channels.list()
	    responseChannelList = responseObject.body["channels"]
	    for channel in responseChannelList:
	        channelId = channel["id"]
	        channelName = channel["name"]
	        chanInfo = [channelId, channelName]
	        self.channelInfo.append(chanInfo)
	    return self.channelInfo

	def sendChannelsToDatabase():
	    for channel in self.channelInfo:
	        channelNum = channel[0]
	        channelName = channel[1]

	        new_channel = message_channel(channelNum, channelName)
	        db.session.add(new_channel)
