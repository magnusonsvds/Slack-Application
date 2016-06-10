from model import slack_user, message_channel, message
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

from message import Message 
from user import User
from channel import Channel

from model import slack_user, message_channel, message
from app import db

def main():
	channels = Channel.getChannelInfo()
	people = User.getUserInformation()
	#messagesForAllChannels = []
	#for chan in channels:
	#	mes =  getMessageinfo(chan)
	#	messagesForAllChannels.append(mes)


	insertData(people, channels)

def insertData(users, channels):
	db.create_all()

    Channel.sendChannelsToDatabase(channels) 
    User.sendUsersToDatabase(users)
    db.session.commit()  

if __name__ == '__main__'
	main()