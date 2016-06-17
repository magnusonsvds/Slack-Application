from app.model import message_channel
from datetime import datetime
from slacker import Slacker
from app import db, slackconnect
from app.model import message_channel

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class Channel(object):
    def __init__(self):
       self.channelInfo = []
       self.table = message_channel
       self.allChannels = {}

    def getChannelInfo(self):
        responseObject = slackconnect.channels.list()
        responseChannelList = responseObject.body["channels"]
        for channel in responseChannelList:
            channelId = channel["id"]
            channelName = channel["name"]
            chanInfo = [channelId, channelName]
            self.channelInfo.append(chanInfo)
        return self.channelInfo

    def sendChannelsToDatabase(self):
        for channel in self.channelInfo:
            channelNum = channel[0]
            channelName = channel[1]

            new_channel = message_channel(channelNum, channelName)
            db.session.merge(new_channel)

    #similar to getChannelInfo but returns in a different format
    def channelList(self):
        query = self.table.query.all()
        for channel in query:
            channelID = channel.channel_number
            channelName = channel.channel_name
            self.allChannels[channelName] = channelID
        return self.allChannels