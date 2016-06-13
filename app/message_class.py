from datetime import datetime
from slacker import Slacker
from app import db, slackconnect

from app.model import message

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Message_Class(object):
	def __init__(self):
		messageLogInfo = []

	def getMessageInfo(self,channel):
	    responseObject = slackconnect.channels.history(channel)
	    responseDict = responseObject.body["messages"]
	    #print (responseDict)

	    messageLogInfo = []
	    for i in responseDict:
	        message = i
	        text = message["text"]
	        user = message["user"]
	        timestamp = message["ts"]
	        messageInfo = [user,text,timestamp,channel]
	        messageLogInfo.append(messageInfo)
	    return messageLogInfo

	def sendMessagesToDatabase(self, messageLogInfo):
	    for mess in messageLogInfo:
	        userNum = mess[0]
	        text = mess[1]
	        date = Message_Class.datetimeChange(self, mess[2])
	        channelNum = mess[3]

	        new_message = message(date, text, userNum, channelNum)
	        db.session.add(new_message)

	def datetimeChange(self, timestamp):
	    return datetime.fromtimestamp(float(timestamp))