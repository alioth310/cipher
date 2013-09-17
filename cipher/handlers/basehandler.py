#! /usr/bin/python
# -*- coding: utf-8 -*-

import tornado.web

from models.basemodel import create_session
from models.admin import get_single_value_setting, get_dict_value_setting

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.session = create_session()
        self.username, self.uid, self.group = self.get_login_info()

        self.page_size = int(
                get_single_value_setting(self.session, "pagesize"))
        self.status_name = get_dict_value_setting(self.session, "statusname")
        self.group_name = get_dict_value_setting(self.session, "groupname")
        self.type_name = get_dict_value_setting(self.session, "typename")

    def on_finish(self):
        self.session.close()

    def get_current_user(self):
        return self.get_secure_cookie("username")

    def get_login_info(self):
        username = self.get_secure_cookie("username")
        uid = self.get_secure_cookie("uid")
        group = self.get_secure_cookie("group")
        return username, uid, group

    def get_ip(self):
        return self.request.remote_ip

    def get_pages(self, page, page_count):
        pages = [1] 
        if page <= 4:
            pages += [p for p in range(1, 6) if p <= page_count]
        elif page > page_count - 4:
            pages += [p for p in range(page_count-4, page_count+1)]
        else:
            pages += [p for p in range(page-2, page+3)] 
        pages.append(page_count)
        return pages

    def set_cookies(self, user_info):
        self.set_secure_cookie("username", user_info.username, httponly=True)
        self.set_secure_cookie("uid", str(user_info.id), httponly=True)
        self.set_secure_cookie("group", str(user_info.group), httponly=True)

