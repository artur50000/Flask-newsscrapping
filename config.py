import os

SECRET_KEY='topsecret'
#SQLALCHEMY_DATABASE_URI='postgresql://postgres:123456@localhost/news'
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS=False