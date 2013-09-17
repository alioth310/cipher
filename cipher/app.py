#! /usr/bin/python
# -*- coding: utf-8 -*-

import os

import tornado.web

from urls import urls
from modules import modules

settings = dict(
    template_path = os.path.join(os.path.dirname(__file__), "templates"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    cookie_secret = "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
    xsrf_cookies = True,
    login_url = "/user/login",
    debug = True,
)

app = tornado.web.Application(
    handlers = urls,
    ui_modules = modules,
    **settings
)
