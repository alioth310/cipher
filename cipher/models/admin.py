#! /usr/bin/python
# -*- coding: utf-8 -*-

from hashlib import md5
from math import ceil

import tornado.locale
_ = tornado.locale.get('zh_CN').translate

from models.basemodel import User, Level, Setting
from models.user import get_user_info_by_name, get_user_info_by_id, \
        generate_salt

def user_update_validation(session, user_info, current_uid, arguments):
    if (get_user_info_by_name(session, arguments['username']) is not None) \
            and (user_info.username != arguments['username']):
        return _("Username already exist!")

    if str(user_info.id) == current_uid:
        return _("Can not edit your own information")
    return ""

def update_user_info(session, user_info, arguments):
    user_info.username = arguments['username']
    user_info.email = arguments['email']
    if arguments['password'] != "":
        user_info.salt = generate_salt()
        user_info.password = md5(arguments['password'] + 
                user_info.salt).hexdigest()
    user_info.status = arguments['status']
    user_info.group = arguments['group']
    session.commit()

def delete_user(session, uid):
    user_info = get_user_info_by_id(session, uid)
    if user_info is None:
        return '1'

    if user_info.group == 1:
        return '2'

    try:
        session.delete(user_info)
        session.commit()
        return '0'
    except:
        return '1'

def level_type_validation(session, type):
    if type not in ['0', '1', '2']:
        return _("Level type error")
    return ""

def update_level_type(session, level_info, type):
    level_info.type = type
    session.commit()

def level_update_validation(session, level_info, arguments, type):
    return ""

def update_level_info(session, level_info, arguments, type):
    level_info.level = arguments['level']
    level_info.step = arguments['step']
    level_info.dirname = arguments['dir_name']
    level_info.pagename = arguments['page_name']
    level_info.title = arguments['title']
    if type == "0":
        level_info.imgname = arguments['img_name']
        level_info.imgalt = arguments['img_alt']
        level_info.hint = arguments['hint']
        level_info.hiddencode = arguments['hidden_code']
        level_info.redirectto = arguments['redirect_to']
        level_info.redirecttime = arguments['redirect_time']
    elif type == "1":
        level_info.hiddencode = arguments['hidden_code']
        level_info.puretexth1 = arguments['pure_text_h1']
        level_info.puretextp = arguments['pure_text_p']
    elif type == "2":
        level_info.redirectto = arguments['redirect_to']
        level_info.redirecttime = arguments['redirect_time']
    session.commit()

def settings_update_validation(session):
    return ""

def update_settings(session, settings, arguments):
    page_size = session.query(Setting).filter(
            Setting.name=="pagesize").first()
    page_size.value = arguments["page_size"]
    status_name = session.query(Setting).filter(
            Setting.name=="statusname").first()
    status_name.value = arguments["status_name"]
    group_name = session.query(Setting).filter(
            Setting.name=="groupname").first()
    group_name.value = arguments["group_name"]
    type_name = session.query(Setting).filter(
            Setting.name=="typename").first()
    type_name.value = arguments["type_name"]

    session.commit()

def get_users(session, page, page_size):
    users = session.query(User).offset(
            (page-1)*page_size).limit(page_size).all()
    return users

def get_user_count(session):
    user_count = session.query(User).count()
    return user_count

def get_levels(session):
    levels = session.query(Level).all()
    return levels

def get_page_count(all_count, count_per_page):
    return int(ceil(float(all_count)/count_per_page))

def get_settings(session):
    s = {}
    settings = session.query(Setting).all()

    for setting in settings:
        s[setting.name] = setting.value

    return s

def get_single_value_setting(session, setting_name):
    return get_setting_value(session, setting_name)

def get_multi_value_setting(session, setting_name):
    return get_setting_value(session, setting_name).split(',')

def get_dict_value_setting(session, setting_name):
    value = get_setting_value(session, setting_name).split(',')
    value_dict = {}
    for each in value:
        k, v = each.split(':')
        value_dict[k] = v
    return value_dict

def get_setting_value(session, setting_name):
    return session.query(Setting).filter(
            Setting.name==setting_name).first().value

