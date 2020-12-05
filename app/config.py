import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost:5432/queue'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_BROKER_URL = os.environ.get('BROKER_URL')
