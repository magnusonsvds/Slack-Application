from datetime import datetime
from slacker import Slacker
from app import db, slackconnect

from app.model import message, slack_user

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Message_Class(object):
    def __init__(self):
    	messageLogInfo = []
    	self.ListOfMessages = []

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
    def messageList(self, messageObjects, userObjects, channel, user, theDate):
        messageStack = []
        messagedUsers = userObjects
        for mess in messageObjects:
            #Channel number, text, and date from message table
            channelNum = mess.channel_number
            messageText = mess.msg
            messageDate = mess.date_time
            messageUserID = mess.slack_number

            slackUserID = slack_user.query.filter(slack_user.slack_number == messageUserID).all()
            userName = slackUserID[0].first_name + " " + slackUserID[0].last_name

            userName = userName.title()
            if(userName in messagedUsers):
            	del(messagedUsers[userName])

            #Query the message_channel table to find the channel name
            channelName = channel
            #append Message
            individualMessage = [messageText, channelName, messageDate, userName]
            messageStack.append(individualMessage)

        if (user == None):
            for user in messagedUsers:
                individualMessage = [" ", channel, theDate, user]
                messageStack.append(individualMessage)

        else: pass

        return messageStack
    def datetimeChange(self, timestamp):
        return datetime.fromtimestamp(float(timestamp))
