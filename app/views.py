from flask import render_template, request
from datetime import datetime, date, timedelta
from app import app, db
from app.model import slack_user, message_channel, message
from app.channel import Channel
from app.user import User
from app.message_class import Message_Class
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import SubmitField, DateField, SelectField
from sqlalchemy import desc
from flask_wtf import Form
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
    avaliableSelections = [('None', 'All')]
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
    #User dropdown bar
    userChoice = SelectField(u'Select User: ', choices = userOptions)
    #Channel dropdown bar
    channelChoice = SelectField(u'Select Channel: ', choices = channelOptions)
    #Date dropdown bar
    dt = DateField('Pick a Date', format="%m/%d/%Y")

#Returns the selection choices for date, time and user and handles no entry
def loadChoices(form):
    #Checking if no date entered, Display current date as default
    if (form.dt.data != None):
        theDate = form.dt.data.strftime('%s') 
        theDate = int(theDate)
    else:
        dateTimeToday = date.today()
        theDate =  dateTimeToday.strftime('%s')
        theDate = int(theDate)
    #Checking if no user has been selected
    if (form.userChoice.data != 'None') :
        submittedUser = form.userChoice.data
        userID = allUserData[submittedUser]
    else:
        submittedUser = 'None'
        userID = 'None'
    #Checks if a channel has been selected
    if(form.channelChoice.data != 'None'):
        submittedChannel = form.channelChoice.data
        channelID = allChannelData[submittedChannel]
    else:
        submittedChannel = 'None'
        channelID = 'None'
    choices = [theDate, channelID, userID, submittedChannel, submittedUser]
    return choices

#Index page of website
@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST','GET'])
def index():
    #Create a new form with user, date and channel fields
    form = Select2TagForm(request.form)

    #all of the selection choices, specified by the user in the dropdown
    selectionChoices = loadChoices(form)

    #call for messages from database (DATE TIME, CHANNEL IDENTIFICATION, USER IDENTIFICATION)
    messageObjects = Message_Class().queryMessages(selectionChoices[0],selectionChoices[1], 
        selectionChoices[2])
    
    #Takes array of messages, userInformation(GLOBAL VARIABLE), channel selection, user 
    #selection date selection and dict of channelIDS. Orders them into a list of lists
    messageStack = Message_Class().messageList(messageObjects, allUserData,
        selectionChoices[3], selectionChoices[4], selectionChoices[0], ch.reverseChannelLookup)

    #returns a render template object to pass items onto html templates
    return render_template('index.html', title="User Directory", messageInfo = messageStack,
        form =form, user = selectionChoices[4])
