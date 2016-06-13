from flask import render_template, flash, redirect, session, url_for, request, g
from datetime import datetime
from app import app, db
from app.model import slack_user, message_channel, message
from app.channel import Channel
from app.user import User
from app.message_class import Message_Class
from flask.ext.sqlalchemy import SQLAlchemy

#updateall of the users and channels into the database when someone vistis /index
@app.before_request
def before_request():
    ch = Channel()
    channels = ch.getChannelInfo()
    usr = User()
    users = usr.getUserInformation()

    userQuery = slack_user.query.all()
    if (len(userQuery) > len(users)) :
        # Insert users in the user table
        usr.sendUsersToDatabase(users) 

    channelQuery = message_channel.query.all()
    if (len(channelQuery) > len(channels)) :
        # Insert channels in the channel table
        ch.sendChannelsToDatabase(channels) 
    db.session.commit()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    users = slack_user.query.all()
    names = []
    for user in users:
        userID = user.slack_number
        userFirst = user.first_name
        userLast = user.last_name
        name = userFirst + " " + userLast
        individual = [name, userID]
        names.append(individual)

    return render_template('index.html', title="User Directory", USERS = names)


@app.route('/user/<theUserID>:<userName>', methods=['GET','POST'])
def user(theUserID, userName):
    #grab messages from slack
    msg = Message_Class()
    slackMessages = msg.getMessageInfo("C1EGNU95L")
    #Insert messages in the the user table
    msg.sendMessagesToDatabase(slackMessages)
    #Commit the inserts
    db.session.commit() 

	#Define how long one day is
    #currentDate = datetime.now()
    #oneDay = currentDate - datetime.timedelta(days = 1)
    
    theUserName = userName

    #Define user variables
    userNum = theUserID

    #Query message table for individual user for the last day
    userObjects = message.query.filter(message.slack_number == userNum).all()

    #stores messages for that user
    messageStack = []
    for mess in userObjects:
        #Channel number, text, and date from message table
        channelNum = mess.channel_number
        messageText = mess.msg
        messageDate = mess.date_time

        #Query the message_channel table to find the channel name
        channel = message_channel.query.filter(message_channel.channel_number == channelNum).all()
        channelName = channel[0].channel_name
        #append Message
        individualMessage = [messageText, channelName, messageDate, userNum]
        messageStack.append(individualMessage)

    return render_template('user.html', title= theUserName + "'s messages", messageInfo = messageStack)
