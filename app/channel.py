from app.model import message_channel
from datetime import datetime
from slacker import Slacker
from app import db, slackconnect
from app.model import message_channel

from flask import Flask


class Channel(object):
    def __init__(self):
       self.channelInfo = []
       self.table = message_channel
       self.allChannels = {}
       self.reverseChannelLookup = {}

    #Retrives channel information through Slack web-api call
    def getChannelInfo(self):
        #Api call retrives all of the channels
        responseObject = slackconnect.channels.list()
        responseChannelList = responseObject.body["channels"]
        for channel in responseChannelList:
            channelId = channel["id"]
            channelName = channel["name"]
            chanInfo = [channelId, channelName]
            self.channelInfo.append(chanInfo)
        return self.channelInfo

    #Push all of the channels into the database
    def sendChannelsToDatabase(self, populate):
        for channel in self.channelInfo:
            channelNum = channel[0]
            channelName = channel[1]

            new_channel = message_channel(channelNum, channelName)
            if populate:
                db.session.add(new_channel)
            else:
                db.session.merge(new_channel)

    #Queries the database for all channel information
    def channelList(self):
        query = self.table.query.all()
        for channel in query:
            channelID = channel.channel_number
            channelName = channel.channel_name
            self.allChannels[channelName] = channelID
            self.reverseChannelLookup[channelID] = channelName
        return self.allChannels