from flask import render_template, flash, redirect, session, url_for, request, g
from datetime import datetime, date, timedelta
from app import app, db
from app.model import slack_user, message_channel, message
from app.channel import Channel
from app.user import User
from app.message_class import Message_Class
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import SelectMultipleField, SubmitField, DateField, SelectField

from flask_wtf import Form
from wtforms import DateField
#from app.FormClasses import Select2TagForm

#Initilizing User and Channel as gloabl variables
usr = User()
ch = Channel()
#Querying the database for all exsisting users and chanells, then returning them as an ordered dictionary
allUserData = usr.userList()
allChannelData = ch.channelList()

#Formating dictionaries into a list of tuples for dropdown fields
def formatDataForDropdown(dataDictionary):
    avaliableSelections = [('None', 'None')]
    for key in dataDictionary:
        selection = (key, key)
        avaliableSelections.append(selection)
    return avaliableSelections

#Form class that holds information on dt, user and channel fields.
class Select2TagForm(Form):
    dataUser = usr.names
    userOptions = formatDataForDropdown(dataUser)

    dataChannel = ch.allChannels
    channelOptions = formatDataForDropdown(dataChannel)
    userChoice = SelectField(u'Select User: ', choices = userOptions)
    channelChoice = SelectField(u'Select Channel: ', choices = channelOptions)
    dt = DateField('Pick a Date', format="%m/%d/%Y")



#updateall of the users and channels into the database when someone vistis /index
@app.before_request
def before_request():
    cha = Channel()
    usa = User()
    channels = cha.getChannelInfo()
    users = usa.getUserInformation()

    userQuery = slack_user.query.all()
    if (len(userQuery) < len(users)) :
        #Insert users in the user table
        usr.sendUsersToDatabase() 

    channelQuery = message_channel.query.all()
    if (len(channelQuery) < len(channels)) :
        # Insert channels in the channel table
        ch.sendChannelsToDatabase() 

    #grab messages from slack
    msg = Message_Class() 
    for channelIdNumber in channelQuery:
        slackMessages = msg.getMessageInfo(channelIdNumber.channel_number)
        #Insert messages in the the user table
        msg.sendMessagesToDatabase(slackMessages)
    #Commit the inserts
    db.session.commit() 

#By default channelID should be passed the general channel. Cant search just by date
def queryMessages(startDate, channelID, slackID):
    eod = startDate + ' 23:59:59'
    if ((channelID and slackID) == "None"):
        userObjects = message.query.filter(startDate < message.date_time, message.date_time <eod).all()
    elif ((channelID) == "None"):
        userObjects = message.query.filter(startDate < message.date_time, message.date_time <eod, message.slack_number == slackID).all()
    elif (slackID == "None"):   
        userObjects = message.query.filter(startDate < message.date_time, message.date_time <eod, message.channel_number == channelID).all()
    else:
        userObjects = message.query.filter(startDate < message.date_time, message.date_time <eod, message.channel_number == channelID, message.slack_number == slackID).all()
    return userObjects


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    #Create a new form with user and channel form
    form = Select2TagForm(request.form) 
    
    if (form.dt.data != None):
        theDate = form.dt.data.strftime('%Y-%m-%d') 
    else:
        theDate = datetime.strftime(date.today(), '%Y-%m-%d')
    if (form.userChoice.data != 'None') :
        submittedUser = form.userChoice.data
        userID = allUserData[submittedUser]
    else:
        submittedUser = "None"
        userID = "None"
    if(form.channelChoice.data != 'None'):
        submittedChannel = form.channelChoice.data
        channelID = allChannelData[submittedChannel]
    else:
        submittedChannel = "None"
        channelID = "None"

    # #ChannelPicker
    # formChannel = Select2TagForm(request.form) 
    # formChannel.data = selectableChannelData
    # if formChannel.validate_on_submit():
    #     submittedChannel = formChannel.tags.data()
    #     #current_app.logger.debug(channelForm.tags.data)
    #     channelID = allChannelData[submittedChannel]
    # else:
    #     submittedChannel = 'general'
    #     channelID =  allChannelData['general']

    # #Queries messages for all given fields
    messageObjects = queryMessages(theDate,channelID,userID)
    
    
    #Store all of the individual messages
    messageStack = []
    #Checking if user does not have messages for today
    if len(messageObjects) == 0:
        individualMessage = ["There are no messages on " + theDate + " and channel: " + submittedChannel, "", "", ""]
        messageStack.append(individualMessage)
    else:
        messageStack = Message_Class().messageList(messageObjects, allUserData, submittedChannel, submittedUser, theDate)

    #return render_template('index.html', title="User Directory", USERS = allUserData, messageInfo = messageStack, formDate = formDate, formUser = formUser, formChannel = formChannel )
    return render_template('index.html', title="User Directory", USERS = allUserData, messageInfo = messageStack, form =form, randomInfo =form.userChoice.data)


@app.route('/user/<theUserID>:<userName>', methods=['GET','POST'])
def user(theUserID, userName):
    #Define user variables
    userNum = theUserID

    #Datepicker
    form = DateForm()
    if form.validate_on_submit():
        theDate = form.dt.data.strftime('%Y-%m-%d') 
    else:
        theDate = datetime.strftime(date.today(), '%Y-%m-%d')

    #Query message table for individual user messages for the last day
    channelID = None
    userObjects = queryMessages(theDate, channelID, theUserID)
    #Store all of the individual messages
    messageStack = []

    #Checking if user does not have messages for today
    if len(userObjects) == 0:
        individualMessage = [userName + " did not have any messages on " + theDate, "", "", ""]
        messageStack.append(individualMessage)
    else:
        for mess in userObjects:
            #Channel number, text, and date from message table
            channelNum = mess.channel_number
            messageText = mess.msg
            messageDate = mess.date_time

            messageUser = slack_user.query.filter(slack_user.slack_number == theUserID)

            #Query the message_channel table to find the channel name
            channel = message_channel.query.filter(message_channel.channel_number == channelNum).all()
            channelName = channel[0].channel_name
            #append Message
            individualMessage = [messageText, channelName, messageDate, userName]
            messageStack.append(individualMessage)

    return render_template('user.html', title= userName + "'s messages", messageInfo = messageStack, form = form)
