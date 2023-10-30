import os

# MySQL 설정
host=''
port=''
user=''
password=''
db_name=''
charset=''

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(user, password, host, port, db_name)
SQLALCHEMY_TRACK_MODIFICATIONS = False


# CSRF 토큰
SECRET_KEY = ""


# 메일
MAIL_SERVER = ''
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_KEY = ''
MAIL_SECRET = ''