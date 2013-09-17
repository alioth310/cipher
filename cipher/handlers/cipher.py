#! /usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web

from models.user import get_user_info_by_id
from models.cipher import get_level_info_by_uri, update_progress
from handlers.basehandler import BaseHandler

class CipherHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, dirname, pagename):
        level_info = get_level_info_by_uri(self.session, dirname, pagename)

        if level_info is None:
            self.render('404.html', username=self.username, group=self.group)

        user_info = get_user_info_by_id(self.session, self.uid)
        
        update_flag = update_progress(self.session, user_info.id,
                level_info.id, level_info.level, level_info.step)
        if update_flag != 0:
            self.render('404.html', username=self.username, group=self.group)
        
        # Special handler for media files
        audioname = '/media/' + level_info.audioname \
                if level_info.audioname else ''
        imgname = '/media/' + level_info.dirname + '/' + \
                level_info.imgname if level_info.imgname else ''
        imgalt = level_info.imgalt if level_info.imgalt else ''
        

        if level_info.type == 1:
            self.render(
                    'cipher_common.html',
                    username = self.username,
                    group = self.group,
                    title = level_info.title,
                    imgname = imgname,
                    imgalt = imgalt,
                    audioname = audioname,
                    hint = level_info.hint,
                    hiddencode = level_info.hiddencode,
                    redirectto = level_info.redirectto,
                    redirecttime = level_info.redirecttime,
            )
        elif level_info.type == 2:
            self.render(
                    'cipher_puretext.html',
                    username = self.username,
                    group = self.group,
                    title = level_info.title,
                    hiddencode = level_info.hiddencode,
                    puretexth1 = level_info.puretexth1,
                    puretextp = level_info.puretextp,
            )
        elif level_info.type == 3:
            self.render(
                    'cipher_redirect.html',
                    username = self.username,
                    group = self.group,
                    title = level_info.title,
                    redirectto = level_info.redirectto,
                    redirecttime = level_info.redirecttime,
            )
        else:
            self.render('404.html', username=self.username, group=self.group)


