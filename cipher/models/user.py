#! /usr/bin/python
# -*- coding: utf-8 -*-

import base64
import uuid
from hashlib import md5
from datetime import datetime

import tornado.locale
_ = tornado.locale.get('zh_CN').translate

from models.basemodel import User

def login_validation(session, username, password):
    user_info = get_user_info_by_name(session, username)
    
    if user_info is None:
        return _("Username does not exist!")

    if contrast_password(password, user_info.password, user_info.salt):
        return _("Password you entered is incorrect!")

    if user_info.status == 1:
        return _("Forbidden user!")
    
    return ""

def update_last_visit(session, username, ip):
    user_info = get_user_info_by_name(session, username)
    user_info.lasttime = datetime.now()
    user_info.lastip = ip
    session.commit()

def signup_validation(session, username):
    user_info = get_user_info_by_name(session, username)
    if user_info is not None:
        return _("Username already exist!")
    return ""

def signup(session, username, email, password, ip):
    salt = generate_salt()
    user = User(username=username, 
            password=md5(password+salt).hexdigest(),
            email=email, group = 0, status=0,
            regtime=datetime.now(),
            regip=ip,
            salt=salt
    )
    session.add(user)
    session.commit()

def password_validation(session, uid, password):
    user_info = get_user_info_by_id(session, uid)

    if contrast_password(password, user_info.password, user_info.salt):
        return _("Old password you entered is incorrect!")
    else:
        return ""

def change_password(session, uid, password):
    user_info = get_user_info_by_id(session, uid)
    salt = generate_salt()
    user_info.salt = salt
    user_info.password = md5(password + salt).hexdigest()
    session.commit()

def get_user_info_by_name(session, username):
    user_info = session.query(User).filter(User.username==username).first()
    return user_info

def get_user_info_by_id(session, id):
    user_info = session.query(User).filter(User.id==id).first()
    return user_info

def contrast_password(input_password, db_password, salt):
    code = 1 if md5(input_password + salt).hexdigest() != db_password else 0
    return code

def generate_salt():
    return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)[18: 24]
