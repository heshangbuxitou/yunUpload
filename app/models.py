from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64))
    time = db.Column(db.DateTime(timezone=True),default=datetime.now)
    uuidpath = db.Column(db.String(200),unique=True)
    other = db.Column(db.String(64))

    def __repr__(self):
        return '<File {}>'.format(self.filename)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),unique=True, index=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)