from flask import render_template, redirect, session, url_for, request
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
import time

#GLOBAL VARIABLES
usr = User()
ch = Channel()
#Querying the database for all exsisting users and chanels, 
#then returning them as an ordered dictionary
allUserData = usr.userList()
allChannelData = ch.channelList()

#Formating dictionaries into a list of tuples for dropdown fields
def formatDataForDropdown(dataDictionary):
    avaliableSelections = [('None', 'None')]
    for key in dataDictionary:
        selection = (key, key)
        avaliableSelections.append(selection)
    return avaliableSelections


#Form class that holds information on dt(Date FIeld), user and channel fields.
class Select2TagForm(Form):
    dataUser = usr.names
    userOptions = formatDataForDropdown(dataUser)

    dataChannel = ch.allChannels
    channelOptions = formatDataForDropdown(dataChannel)
    userChoice = SelectField(u'Select User: ', choices = userOptions)
    channelChoice = SelectField(u'Select Channel: ', choices = channelOptions)
    dt = DateField('Pick a Date', format="%m/%d/%Y")


#Updates tables that need to be updated before loading a page
@app.before_request
def before_request():
    #Initilizing chanel, user and message objects
    cha = Channel()
    usa = User()
    msg = Message_Class() 
    #Calling slack api for new information
    channels = cha.getChannelInfo()
    users = usa.getUserInformation()

    #Querying the database for all users
    userQuery = slack_user.query.all()
    #Comparing information from slack and query from databse, to see if an update is needed
    if (len(userQuery) < len(users)) :
        #Insert users in the user table
        usr.sendUsersToDatabase(False) 
    #Querying the database for all channels
    channelQuery = message_channel.query.all()
    #Comparing information from slack and query from databse, to see if an update is needed
    if (len(channelQuery) < len(channels)) :
        # Insert channels in the channel table
        ch.sendChannelsToDatabase(False) 
    
    #Querying the message table for the last date time a message was posted
    lastMessageDate = message.query.order_by('date_time').first()
    if lastMessageDate == None:
        #convert date to a timestamp
        lastMessageDate = datetime.strftime(date.today(), '%Y-%m-%d')
        lastMessageTimestamp = time.mktime(datetime.strptime(lastMessageDate,
            "%Y-%m-%d").timetuple())
    else:
        #convert datetime to a timestamp
        lastMessageTimestamp = lastMessageDate.date_time.timestamp()

    #Get messageObjects from slack and send them to the database
    for channelIdNumber in channelQuery:
        slackMessages = msg.getMessageInfo(channelIdNumber.channel_number, lastMessageTimestamp)
        #Insert messages in the the message table
        msg.sendMessagesToDatabase(slackMessages)
    #Commit the inserts
    db.session.commit() 


#Returns the selection choices for date, time and user and handles no entry
def loadChoices(form):
     
    #Checking if no date entered, Display current date as default
    if (form.dt.data != None):
        theDate = form.dt.data.strftime('%Y-%m-%d') 
    else:
        theDate = datetime.strftime(date.today(), '%Y-%m-%d')
    #Checking if no user has been selected
    if (form.userChoice.data != 'None') :
        submittedUser = form.userChoice.data
        userID = allUserData[submittedUser]
    else:
        submittedUser = "None"
        userID = "None"
    #Checks if a channel has been selected
    if(form.channelChoice.data != 'None'):
        submittedChannel = form.channelChoice.data
        channelID = allChannelData[submittedChannel]
    else:
        submittedChannel = "None"
        channelID = "None"
    choices = [theDate, channelID, userID, submittedChannel]
    return choices


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = Select2TagForm(request.form)
    #Create a new form with user, date and channel fields
    selectionChoices = loadChoices(form)
    #call for messages from database (DATE TIME, CHANNEL IDENTIFICATION, USER IDENTIFICATION)
    messageObjects = Message_Class().queryMessages(selectionChoices[0],selectionChoices[1], 
        selectionChoices[2])
    #Store all of the individual messages in an array
    messageStack = []

    #If user does not have any messages for selected date or channel, display a message
    if len(messageObjects) == 0:
        individualMessage = ["There are no messages on " + selectionChoices[0] + " in channel: " +
            selectionChoices[3], "", "", ""]
        messageStack.append(individualMessage)
    else:
        #Takes array of messages, userInformation(GLOBAL VARIABLE), channel selection, user 
        #selection and date selection. Orders them into a list of lists
        messageStack = Message_Class().messageList(messageObjects, allUserData,
            sselectionChoices[1], selectionChoices[2], selectionChoices[0])

    #returns a render template object to pass items onto html templates
    return render_template('index.html', title="User Directory", messageInfo = messageStack,
        form =form)
