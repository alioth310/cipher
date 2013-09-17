#! /usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Column, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, SmallInteger, Boolean, DateTime, \
        String, Text

DB_CONNECT_STRING = 'mysql+mysqldb://root:Passw0rd@127.0.0.1/cipher?charset=utf8'
engine = create_engine(DB_CONNECT_STRING, echo=False)

def create_session():
    DB_Session = sessionmaker(bind=engine)
    session = DB_Session()
    return session

BaseModel = declarative_base()

def init_db():
    BaseModel.metadata.create_all(engine)

def drop_db():
    BaseModel.metadata.drop_all(engine)

class User(BaseModel):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(32), nullable=False)
    email = Column(String(64), nullable=False)
    group = Column(SmallInteger, default=0)  # 0: gamer, 1: admin
    status = Column(SmallInteger, default=0)  # 0: allowed, 1: forbidden
    regtime = Column(DateTime)
    regip = Column(String(15))
    lasttime = Column(DateTime)
    lastip = Column(String(15))
    salt = Column(String(6), nullable=False)

class Level(BaseModel):
    __tablename__ = 'level'

    id = Column(Integer, primary_key=True)
    level = Column(SmallInteger, nullable=False)
    step = Column(SmallInteger, nullable=False)  # 0: fake page
    type = Column(SmallInteger, nullable=False)  # 0: common, 1: puretext, 2: redirect
    dirname = Column(String(64), nullable=False)
    pagename = Column(String(64), nullable=False)
    title = Column(String(256), nullable=False)
    imgname = Column(String(128))
    imgalt = Column(String(256))
    otherimgs = Column(String(256))  # name of other images, ',' seperate
    audioname = Column(String(128))
    otheraudios = Column(String(256))  # name of other audios, ',' seperate
    hint = Column(String(512))
    hiddencode = Column(Text)
    puretexth1 = Column(String(256))
    puretextp = Column(Text)
    redirectto = Column(String(128))
    redirecttime = Column(SmallInteger)

class Progress(BaseModel):
    __tablename__ = 'progress'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'))
    lid = Column(Integer, ForeignKey('level.id'))
    time = Column(DateTime)
    iscurrent = Column(Boolean)

class Page(BaseModel):
    __tablename__ = 'page'
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    content = Column(Text)

class Setting(BaseModel):
    __tablename__ = 'setting'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)
    value = Column(Text())
