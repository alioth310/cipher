#! /usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime

from models.basemodel import Level, Progress

def get_level_info_by_uri(session, dirname, pagename):
    level_info = session.query(Level).filter(
            Level.dirname==dirname, Level.pagename==pagename).first()
    return level_info

def get_level_info_by_id(session, id):
    level_info = session.query(Level).filter(Level.id==id).first()
    return level_info

def get_current_level(session, uid):
    try:
        current_progress = get_current_progress(session, uid)
        current_level = session.query(Level).filter(
                Level.id==current_progress.lid).first().level
        return current_level
    except:
        return 0

def get_levels(session, current_level):
    levels = session.query(Level).filter(Level.level<=current_level,
            Level.step==1).order_by(Level.level).all()
    return levels
    
def get_current_progress(session, uid):
    current_progress = session.query(Progress).filter(
            Progress.uid==uid, Progress.iscurrent==True).first()
    return current_progress

def update_progress(session, uid, lid, level, step):
    old_progress = get_current_progress(session, uid)
    if old_progress is not None:
        old_level_info = session.query(Level).filter(
                Level.id==old_progress.lid).first()
        old_level = old_level_info.level
        old_step = old_level_info.step

        if lid == old_progress.lid:
            return 0

        level_diff = level - old_level
        if level_diff > 1:
            return 1
        elif (level_diff < 0) or (level_diff == 0 and step <= old_step):
            return 0
        else:
            old_progress.iscurrent = False
            session.flush()
    else:
        if level > 1:
            return 1

    new_progress = Progress(
            uid=uid,
            lid=lid,
            time=datetime.now(),
            iscurrent=True
    )
    session.add(new_progress)

    session.commit()
    return 0
