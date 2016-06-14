from app.model import slack_user, message_channel, message
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime

from app.message import Message 
from app.user import User
from app.channel import Channel

from app import db

def main():
	ch = Channel()
	usr = USer()
	channels = ch.getChannelInfo()
	people = usr.getUserInformation()
	#messagesForAllChannels = []
	#for chan in channels:
	#	mes =  getMessageinfo(chan)
	#	messagesForAllChannels.append(mes)


	insertData(people, channels)

def insertData(users, channels):
	db.create_all()

	ch = Channel()
	usr = USer()
	ch.sendChannelsToDatabase(channels) 
	usr.sendUsersToDatabase(users)
	db.session.commit()  

if __name__ == '__main__':
	main()