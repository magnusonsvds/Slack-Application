from flask import render_template, flash, redirect, session, url_for, request, g
from datetime import datetime
from app import app, db, lm, oid
from model import slack_user, message_channel, message
from channel import Channel
from user import User


#update
 all of the users and channels into the database when someone vistis /index
@app.before_request
def before_request():
	channels = Channel.getChannelInfo()
	users = User.getUserInformation()

	userQuery = slack_user.query.all()
    if (len(userQuery) > len(users)):
        # Insert users in the user table
        sendUsersToDatabase(users) 

    channelQuery = message_channel.query.all()
    if (len(channelQuery) > len(channels)):
        # Insert channels in the channel table
        sendChannelsToDatabase(channels) 
    db.session.commit()

@app.route('/')
@app.route('/index')
def home():
    users = slack_user.query.all()
    names = []
    for user in users:
        userFirst = users.First
        userLast = user.Last
        name = userFirst + " " + userLast
        names.append(name)

    return render_template('index.html', title="User Directory", USERS = names)