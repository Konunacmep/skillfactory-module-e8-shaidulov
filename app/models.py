from app import db
from enum import Enum
from datetime import datetime


class Results(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    address = db.Column(db.String(300), unique=False, nullable=True)
    words_count = db.Column(db.Integer, unique=False, nullable=True)
    http_status_code = db.Column(db.Integer)
    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            'id': self.id,
            'address': self.address,
            'words_count': self.words_count,
            'http_status_code': self.http_status_code
        }


class TaskStatus(Enum):
    NOT_STARTED = 1
    PENDING = 2
    FINISHED = 3


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(300), unique=False, nullable=True)
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow)
    task_status = db.Column(db.Enum(TaskStatus))
    http_status = db.Column(db.Integer, nullable=True)
