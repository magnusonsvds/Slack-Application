from datetime import datetime
from slacker import Slacker
from app import db, slackconnect

from app.model import message, slack_user

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Message_Class(object):
    def __init__(self):
    	self.ListOfMessages = []
   
    #Gets messages from Slack from since last timestamp
    def getMessageInfo(self,channel, date):
        responseObject = slackconnect.channels.history(channel, latest = date)
        responseDict = responseObject.body["messages"]

        messageLogInfo = []
        for i in responseDict:
            message = i
            text = message["text"]
            user = message["user"]
            timestamp = message["ts"]
            messageInfo = [user,text,timestamp,channel]
            messageLogInfo.append(messageInfo)
        return messageLogInfo

    #pushes the messages to the database
    def sendMessagesToDatabase(self, messageLogInfo):
        for mess in messageLogInfo:
            userNum = mess[0]
            text = mess[1]
            date = Message_Class.datetimeChange(self, mess[2])
            channelNum = mess[3]

            new_message = message(date, text, userNum, channelNum)
            db.session.merge(new_message)

    #Queries for messages given the filters 
    def queryMessages(self, startDate, channelID, slackID):
        eod = startDate + ' 23:59:59'
        if (channelID  == "None" and slackID == "None"):
            messageObjects = message.query.filter(startDate < message.date_time, message.date_time <eod).all()
        elif ((channelID) == "None"):
            messageObjects = message.query.filter(startDate < message.date_time, message.date_time <eod, message.slack_number == slackID).all()
        elif (slackID == "None"):   
            messageObjects = message.query.filter(startDate < message.date_time, message.date_time <eod, message.channel_number == channelID).all()
        else:
            messageObjects = message.query.filter(startDate < message.date_time, message.date_time <eod, message.channel_number == channelID, message.slack_number == slackID).all()
        return messageObjects

    #Organizes a list of all the messages into a list of lists
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

    #converts timestamp to datetime
    def datetimeChange(self, timestamp):
        return datetime.fromtimestamp(float(timestamp))
