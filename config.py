import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1Svds@123@localhost/slacktestdb'

slack_api_token = "xoxp-48585661490-48566956614-49633690839-8a11581e73"