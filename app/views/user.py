from flask import render_template, flash, redirect, session, url_for, request, g
from datetime import datetime
from app import app, db, lm, oid
from message import Message
from models import slack_user, message_channel, message

#individual user webpage
@app.route('/user/<theUserId>', methods=['POST'])
def index(theUserID):
    #grab messages from slack
    slackMessages = Message.getMessageInfo("C1EGNU95L")
    #Insert messages in the the user table
    sendMessagesToDatabase(slackMessages)
    #Commit the inserts
    db.session.commit() 

	#Define how long one day is
    oneDay = currentDate() - datetime.timedelta(days = 1)
    
    pushedInfo = []

    #Define user variables
    userNum = user.slack_number
    userFirst = user.slack_first
    userLast = user.slack_last
    userName = userFirst + " " +userLast

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
            messageStack.append(messageText, channelName, messageDate, userNum)

    return render_template('user.html', title="Today's Messages", theUser = userName, messageInfo = messageStack)

