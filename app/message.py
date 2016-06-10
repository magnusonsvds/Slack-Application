from datetime import datetime
from slacker import Slacker
from app import db, slackconnect

from app.model import message

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Message(object):
	def __init__(self):
		self.messageLogInfo = []

	def getMessageInfo(channel):
	    responseObject = slackconnect.channels.history(channel)
	    responseDict = responseObject.body["messages"]
	    #print (responseDict)

	    for i in responseDict:
	        message = i
	        text = message["text"]
	        user = message["user"]
	        timestamp = message["ts"]
	        messageInfo = [user,text,timestamp,channel]
	        self.messageLogInfo.append(messageInfo)
	    return self.messageLogInfo

	def sendMessagesToDatabase():
	    for mess in self.messageLogInfo:
	        userNum = mess[0]
	        text = mess[1]
	        date = datetimeChange(mess[2])
	        channelNum = mess[3]

	        new_message = message(date, text, userNum, channelNum)
	        db.session.add(new_message)

	def datetimeChange(timestamp):
	    return datetime.fromtimestamp(float(timestamp))