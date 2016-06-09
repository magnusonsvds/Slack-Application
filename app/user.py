from slacker import Slacker
from slack_entries_database import db

from slack_entries_database import slack_user, message_channel, message

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1Svds@123@localhost/slacktestdb'
db = SQLAlchemy(app)

slackconnect = Slacker("xoxp-48585661490-48566956614-49307999364-419b3ccfc5")
class User(object):
    def __init__(self):
        self.userInfo = []

    def getUserInformation():
        responseObject = slackconnect.users.list()
        responseMemberList = responseObject.body["members"]
        for member in responseMemberList:
            idCode = member["id"]
            profile = member["profile"]
            firstName = profile["first_name"]
            LastName = profile["last_name"]
            memberInfo = [idCode, firstName, LastName]
            self.userInfo.append(memberInfo)
        return self.userInfo


    def sendUsersToDatabase():
        for user in self.userInfo:
            userNum = user[0]
            userFirst = user[1]
            userLast = user[2]

            new_user = slack_user(userNum, userFirst, userLast)
            db.session.add(new_user)