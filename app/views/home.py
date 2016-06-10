from flask import render_template, flash, redirect, session, url_for, request, g
from datetime import datetime
from app import app, db, lm, oid
from .models import slack_user, message_channel, message

#Grabs current time for defining how long one day is
def currentDate():
    return datetime.datetime.utcnow()

@app.route('/home')
@login_required
def index():
    #Define how long one day is
    oneDay = currentDate() - datetime.timedelta(days = 1)

    #Query all of the users
    users = slack_user.query.all()
    
    pushedInfo = []

    for user in users:
        #Define user variables
        userNum = user.slack_number
        userFirst = user.slack_first
        userLast = user.slack_last

        #Query message table for individual user for the last day
        messages = message.query.filter(slack_number = userNum, message.date_time > oneDay).all()
        #stores messages for that user
        messageStack = []
        for mess in messages:
            #Channel number, text, and date from message table
            channelNum = mess.channel_number
            messageText = mess.msg
            messageDate = mess.date_time

            #Query the message_channel table to find the channel name
            channel = message_channel.query.filter_by(channel_number = channelNum)
            channelName = channel.channel_name
            #append Message
            messageStack.append(messageText)

        #New dictionary item to store all of a user's information that gets passed into a stack
        individualEntry = {'name': userFirst + ' ' + userLast, 'message': messageStack, 'channel': channelName, 'time': messageDate}
        pushedInfo.append(individualEntry)
        messageStack[:] = []



    return render_template('index.html', title="Today's Messages", message=pushedInfo, )