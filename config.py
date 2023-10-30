import os

# MySQL 설정
host='127.0.0.1'
port='3305'
user='root'
password='Sunbreath!!'
db_name='flo'
charset='utf8'

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(user, password, host, port, db_name)
SQLALCHEMY_TRACK_MODIFICATIONS = False


# CSRF 토큰
SECRET_KEY = "F!0j2Ct"


# 메일
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'junmyeonaaa@gmail.com'
MAIL_PASSWORD = 'fokm slpr hitv opfp'
MAIL_KEY = 'mailtest'
MAIL_SECRET = 'F!0j2Ct'