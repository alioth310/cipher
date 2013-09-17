#! /usr/bin/python
# -*- coding: utf-8 -*-

from basemodel import create_session, drop_db, init_db, User, Level, Setting

def create_user_table(session):
    from hashlib import md5
    from datetime import datetime

    user = User(username='admin', \
            password=md5('password'+'5ja8vz').hexdigest().lower(), \
            email='alioth310@gmail.com', group=1, status=0, \
            regtime=datetime.now(), regip='8.8.8.8', \
            salt='5ja8vz')
    session.add(user)
    user = User(username='gamer', \
            password=md5('123456'+'8vha9g').hexdigest().lower(), \
            email='i@pythoner.com', group=0, status=0, \
            regtime=datetime.now(), regip='8.8.8.8', \
            salt='8vha9g')
    session.add(user)
    user = User(username='forbidden', \
            password=md5('123'+'0ba8ba').hexdigest().lower(), \
            email='i@ibeike.com', group=0, status=1, \
            regtime=datetime.now(), regip='8.8.8.8', \
            salt='0ba8ba')
    session.add(user)
    session.commit()

def create_settings_table(session):
    setting = Setting(name='pagesize', value='50')
    session.add(setting)
    setting = Setting(name='statusname', value=u'0:正常,1:禁止')
    session.add(setting)
    setting = Setting(name='groupname', value=u'0:普通用户,1:管理员')
    session.add(setting)
    setting = Setting(name='typename', value=u'1:普通,2:纯文本,3:跳转')
    session.add(setting)

    session.commit()

if __name__ == "__main__":
    session = create_session()

    drop_db()
    init_db()
    create_user_table(session)
    create_settings_table(session)
