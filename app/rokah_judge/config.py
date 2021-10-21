import os

DEBUG = True
USERNAME = "roka"
PASSWORD = "pass"
SECRET_KEY = "secret"
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8'.format(
    **{
      'user': os.getenv('DB_USER', 'root'),
      'password': os.getenv('DB_PASSWORD', 'password'),
      'host': os.getenv('DB_HOST', 'mysql'),
      'database': os.getenv('DB_DATABASE', 'rokah_judge'),
    })
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
