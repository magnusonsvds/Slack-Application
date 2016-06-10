from flask import render_template, flash, redirect, session, url_for, request, g
from datetime import datetime
from app import app, db, lm, oid
from .models import slack_user, message_channel, message


#displays all of the users
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