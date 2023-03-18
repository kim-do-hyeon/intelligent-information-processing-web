# -*- encoding: utf-8 -*-
from flask_login import UserMixin
import datetime
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from apps import db, login_manager

from apps.authentication.util import hash_pass

class Users(db.Model, UserMixin):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.LargeBinary)
    admin = db.Column(db.Integer)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]
            if property == 'password':
                value = hash_pass(value)
            setattr(self, property, value)
    def __repr__(self):
        return str(self.username)
    
class students(db.Model, UserMixin) :
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64))
    lab = db.Column(db.String(64))
    position = db.Column(db.String(64))
    description = db.Column(db.String(64))
    image = db.Column(db.String(64))

class project(db.Model, UserMixin) :
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64))
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    title = db.Column(db.Text)
    abstract = db.Column(db.Text)
    content = db.Column(db.Text)
    image = db.Column(db.String(64))

@login_manager.user_loader
def user_loader(id):
    return Users.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Users.query.filter_by(username=username).first()
    return user if user else None