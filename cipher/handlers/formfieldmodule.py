#! /usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web

class InputFieldModule(tornado.web.UIModule):
    def render(self, field, **kwargs):
        return self.render_string(
                "modules/inputfield.html",
                field = field,
                kwargs = kwargs
        )

class ButtonFieldModule(tornado.web.UIModule):
    def render(self, field, **kwargs):
        return self.render_string(
                "modules/buttonfield.html",
                field = field,
                kwargs = kwargs
        )

class RadioFieldModule(tornado.web.UIModule):
    def render(self, field, **kwargs):
        return self.render_string(
                "modules/radiofield.html",
                field = field,
                kwargs = kwargs
        )

class TextAreaFieldModule(tornado.web.UIModule):
    def render(self, field, **kwargs):
        return self.render_string(
                "modules/textareafield.html",
                field = field,
                kwargs = kwargs
        )

class HiddenFieldModule(tornado.web.UIModule):
    def render(self, field, **kwargs):
        return self.render_string(
                "modules/hiddenfield.html",
                field = field,
                kwargs = kwargs
        )

class FileFieldModule(tornado.web.UIModule):
    def render(self, field, **kwargs):
        return self.render_string(
                "modules/filefield.html",
                field = field,
                kwargs = kwargs
        )
