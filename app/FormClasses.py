from app import app, db
from flask_wtf import Form
from wtforms import SelectMultipleField, SubmitField, DateField, SelectField


class Select2TagForm(Form):
    dataUser = []
    dataChannel = []
    userChoice = SelectField(u'Select User: ', choices = dataUser)
    channelChoice = SelectField(u'Select Channel: ', choices = dataChannel)
    dt = DateField('Pick a Date', format="%m/%d/%Y")

   