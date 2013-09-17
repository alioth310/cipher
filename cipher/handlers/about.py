#! /usr/bin/python
# -*- coding: utf-8 -*-

from handlers.basehandler import BaseHandler

class AboutHandler(BaseHandler):
    def get(self):
        self.render(
                "about.html",
                username = self.username,
                group = self.group
        )
