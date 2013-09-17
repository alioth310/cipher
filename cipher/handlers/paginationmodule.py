#! /usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web

class PaginationModule(tornado.web.UIModule):
    def render(self, pages, page):
        return self.render_string(
                "modules/pagination.html",
                pages = pages,
                page = page
        )

