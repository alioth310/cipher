#! /usr/bin/python
# -*- coding: utf-8 -*-

import tornado.locale

from forms import LoginForm
from handlers.basehandler import BaseHandler

class IndexHandler(BaseHandler):
    def get(self):
        self.render("index.html", username=self.username, group=self.group)
        
