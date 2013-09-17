#! /usr/bin/python
# -*- coding: utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.locale

from tornado.options import define, options

from app import app
from config import DEFAULT_PORT, I18N_PATH

define("port", default=DEFAULT_PORT, help="run on the given port", type=int)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    
    tornado.locale.load_gettext_translations(I18N_PATH, "cipher")
    tornado.locale.set_default_locale('zh_CN')

    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
