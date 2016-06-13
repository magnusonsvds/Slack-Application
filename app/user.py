from slacker import Slacker
from flask import Flask
from app.model import slack_user
from app import app, db, slackconnect
from flask_sqlalchemy import SQLAlchemy


class User(object):
    def __init__(self):
        self.userInfo = []

    def getUserInformation(self):
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


    def sendUsersToDatabase(self):
        for user in self.userInfo:
            userNum = user[0]
            userFirst = user[1]
            userLast = user[2]

            new_user = slack_user(userNum, userFirst, userLast)
            db.session.add(new_user)