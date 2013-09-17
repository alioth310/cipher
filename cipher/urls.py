#! /usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web

from handlers.index import IndexHandler
from handlers.about import AboutHandler
from handlers.cipher import CipherHandler
from handlers.user import LoginHandler, LogoutHandler, SignupHandler, \
        LevelChooseHandler, PasswordChangeHandler
from handlers.admin import AdminIndexHandler, LevelListHandler, \
        LevelShowHandler, LevelCreateHandler, LevelEditHandler, \
        UserListHandler, UserShowHandler, \
        UserEditHandler, UserDeleteHandler, SettingsHandler, \
        LevelTypeChangeHandler

from config import MEDIA_PATH

urls = [
    (r'/(?:cipher)*/?', IndexHandler),
    (r'/about/?', AboutHandler),
    (r'/cipher/(.+)/(.+)\.html', CipherHandler),
    (r'/media/(.+)', tornado.web.StaticFileHandler, {'path': MEDIA_PATH}),
    (r'/user/login/?', LoginHandler),
    (r'/user/logout/?', LogoutHandler),
    (r'/user/signup/?', SignupHandler),
    (r'/user/profile/level/?', LevelChooseHandler),
    (r'/user/profile/password/?', PasswordChangeHandler),
    (r'/admin/index/?', AdminIndexHandler),
    (r'/admin/level/list/?', LevelListHandler),
    (r'/admin/level/show/(\d+)/?', LevelShowHandler),
    (r'/admin/level/create/?', LevelCreateHandler),
    (r'/admin/level/edit/(\d+)/?', LevelEditHandler),
    (r'/admin/level/type/(\d+)/?', LevelTypeChangeHandler),
    (r'/admin/user/list/?', UserListHandler),
    (r'/admin/user/show/(\d+)/?', UserShowHandler),
    (r'/admin/user/edit/(\d+)?', UserEditHandler),
    (r'/admin/user/delete/?', UserDeleteHandler),
    (r'/admin/settings/?', SettingsHandler),
]
