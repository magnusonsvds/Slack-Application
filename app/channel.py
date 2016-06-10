from model import message_channel
from datetime import datetime
from slacker import Slacker
from app import db, slackconnect

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
