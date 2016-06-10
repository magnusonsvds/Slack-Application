import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import basedir

from datetime import datetime
from slacker import Slacker
from channel import Channel
from user import User
from message import Message

from slack_entries_database import slack_user, message_channel, message

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI']
slackconnect = Slacker(app.config["slack_api_token"])

from app import views, models

#populate the table with channels and users if no data exsists currently
def insertData(messages, users, channels):
    Channel.sendChannelsToDatabase(channels) 
    User.sendUsersToDatabase(users)
    db.session.commit()  

#put all of the data into the database
def pushData(messages, users, channels):

    userQuery = slack_user.query.all()
    if (len(userQuery) > len(users)):
        # Insert users in the user table
        sendUsersToDatabase(users) 

    channelQuery = message_channel.query.all()
    if (len(channelQuery) > len(channels)):
        # Insert channels in the channel table
        sendChannelsToDatabase(channels) 

    #Insert messages in the the user table
    sendMessagesToDatabase(messages)
      
    #Commit the inserts
    db.session.commit()     

#run the script
if __name__ == '__main__':
    channels = Channel.getChannelInfo()
    messages = Message.getMessageInfo("C1EGNU95L")
    users = User.getUserInformation()
    #insertData(messages, users, channels)
    pushData(messages, users, channels)

