from app import app, db
import app.views
from app.user import User
from app.channel import Channel

class DisplayData(object):
    usr =User()
    ch = Channel()
    allUserData = User().userList()
    allChannelData = Channel().channelList()