#! /usr/bin/python
# -*- coding: utf-8 -*-

import os

import tornado.web

from forms import UserEditForm, SettingsForm, LevelTypeChangeForm, \
        CommonLevelForm, PureTextLevelForm, RedirectLevelForm
from models.admin import get_users, get_user_count, \
        user_update_validation, level_update_validation, delete_user, \
        update_user_info, update_level_info, get_page_count, \
        get_levels, get_settings, settings_update_validation, update_settings, \
        level_type_validation, update_level_type
from models.user import get_user_info_by_id
from models.cipher import get_level_info_by_id
from handlers.basehandler import BaseHandler

# TODO: 1.Validation for administrator should be refactoring
#       2.Active State of left sidebar
#       3.from ... import ... should be refactoring

class AdminIndexHandler(BaseHandler):
    '''Index page of Management Center.'''
    @tornado.web.authenticated
    def get(self):
        if self.group != '1':
            self.render("404.html", username=self.username, group=self.group)

        self.render(
                "admin/index.html", 
                username=self.username,
                group=self.group)

class LevelListHandler(BaseHandler):
    '''List all levels.'''
    @tornado.web.authenticated
    def get(self):
        if self.group != '1':
            self.render("404.html", username=self.username, group=self.group)

        levels = get_levels(self.session)
        self.render(
                "admin/level_list.html", 
                username=self.username,
                group=self.group, 
                levels=levels, 
                type_name=self.type_name
        )

class LevelShowHandler(BaseHandler):
    '''Show the detail information of some level.'''
    @tornado.web.authenticated
    def get(self, id):
        if self.group != '1':
            self.render("404.html", username=self.username, group=self.group)

        level_info = get_level_info_by_id(self.session, id)

        if level_info is None:
            self.render("404.html", username=self.username, group=self.group)

        self.render(
                "admin/level_detail.html", 
                username=self.username,
                group=self.group, 
                type_name=self.type_name,
                level_info=level_info
        )

class LevelCreateHandler(BaseHandler):
    '''Create new Level or step.

    Attention: This handler has not be implemented now!'''
    @tornado.web.authenticated
    def get(self):
        if self.group != '1':
            self.render("404.html", username=self.username, group=self.group)

        self.write("level create test")

class LevelEditHandler(BaseHandler):
    '''Edit information of some level/step.

    Attention: This handler has just been partly implemented.

    TODO: 1.Image file upload.
          2.Other Image file.
          3.Audio file upload.
          4.Other Audio file.'''
    @tornado.web.authenticated
    def get(self, id):
        if self.group != '1':
            self.render("404.html", username=self.username, group=self.group)

        cipher_type = self.get_argument("type")
        level_info = get_level_info_by_id(self.session, id)

        if level_info is None:
            self.render("404.html", username=self.username, group=self.group)

        if cipher_type != str(level_info.type):
            self.redirect("/admin/level/type/" + str(level_info.id))

        if cipher_type == "0":
            form = CommonLevelForm()
        elif cipher_type == "1":
            form = PureTextLevelForm()
        elif cipher_type == "2":
            form = RedirectLevelForm()
        else:
            return

        self.render(
                "admin/level_edit.html",
                username = self.username,
                group = self.group,
                level_info = level_info,
                form = form,
                db_error = None,
                cipher_type = cipher_type
        )

    @tornado.web.authenticated
    def post(self, id):
        if self.group != '1':
            self.render("404.html", username=self.username, group=self.group)

        cipher_type = self.get_argument("type")
        level_info = get_level_info_by_id(self.session, id)

        if level_info is None:
            self.render("404.html", username=self.username, group=self.group)

        if cipher_type != str(level_info.type):
            self.redirect("/admin/level/type/" + str(level_info.id))

        if cipher_type == "0":
            form = CommonLevelForm(self.request.arguments)
            arguments = {
                    "level": self.get_argument("level"),
                    "step": self.get_argument("step"),
                    "dir_name": self.get_argument("dirname"),
                    "page_name": self.get_argument("pagename"),
                    "title": self.get_argument("title"),
                    "img_name": self.get_argument("imgname"),
                    "img_alt": self.get_argument("imgalt"),
                    "hint": self.get_argument("hint"),
                    "hidden_code": self.get_argument("hiddencode"),
                    "redirect_to": self.get_argument("redirectto"),
                    "redirect_time": self.get_argument("redirecttime"),
            }
        elif cipher_type == "1":
            form = PureTextLevelForm(self.request.arguments)
            arguments = {
                    "level": self.get_argument("level"),
                    "step": self.get_argument("step"),
                    "dir_name": self.get_argument("dirname"),
                    "page_name": self.get_argument("pagename"),
                    "title": self.get_argument("title"),
                    "hidden_code": self.get_argument("hiddencode"),
                    "pure_text_h1": self.get_argument("puretexth1"),
                    "pure_text_p": self.get_argument("puretextp"),
            }
        elif cipher_type == "2":
            form = RedirectLevelForm(self.request.arguments)
            arguments = {
                    "level": self.get_argument("level"),
                    "step": self.get_argument("step"),
                    "dir_name": self.get_argument("dirname"),
                    "page_name": self.get_argument("pagename"),
                    "title": self.get_argument("title"),
                    "redirect_to": self.get_argument("redirectto"),
                    "redirect_time": self.get_argument("redirecttime"),
            }
        else:
            return

        update_error = level_update_validation(self.session, level_info, 
                arguments, cipher_type)
        
        if form.validate():
            if update_error == "":
                update_level_info(self.session, level_info, 
                        arguments, cipher_type)
                self.redirect("/admin/level/show/" + str(level_info.id))
            else:
                self.render(
                    "admin/level_edit.html",
                    username = self.username,
                    group = self.group,
                    level_info = level_info,
                    form = form,
                    db_error = update_error,
                    cipher_type = cipher_type
                )
        else:
            self.render(
                "admin/level_edit.html",
                username = self.username,
                group = self.group,
                level_info = level_info,
                form = form,
                db_error = None,
                cipher_type = cipher_type
            )

class LevelTypeChangeHandler(BaseHandler):
    '''Change level type'''

    @tornado.web.authenticated
    def get(self, id):
        if self.group != '1':
            self.render("404.html", username=self.username, group=self.group)

        level_info = get_level_info_by_id(self.session, id)
        if level_info is None:
            self.render(
                    "404.html",
                    username = self.username,
                    group = self.group
            )

        form = LevelTypeChangeForm()
        form.type.choices = [(k, v) for k, v in self.type_name.iteritems()]
        form.type.choices.sort()

        self.render(
                "admin/level_changetype.html",
                username = self.username,
                group = self.group,
                level_info = level_info,
                form = form,
                db_error = None,
                type_name = self.type_name
        )

    @tornado.web.authenticated
    def post(self, id):
        if self.group != '1':
            self.render("404.html", username=self.username, group=self.group)

        type = self.get_argument("type")
        level_info = get_level_info_by_id(self.session, id)
        
        if level_info is None:
            self.render(
                    "404.html",
                    username = self.username,
                    group = self.group
            )

        form = LevelTypeChangeForm(self.request.arguments)
        form.type.choices = [(k, v) for k, v in self.type_name.iteritems()]
        form.type.choices.sort()

        update_error = level_type_validation(self.session, type)

        if form.validate():
            if update_error == "":
                update_level_type(self.session, level_info, type)
                self.redirect("/admin/level/show/" + str(level_info.id))
            else:
                self.render(
                        "admin/level_changetype.html",
                        username = self.username,
                        group = self.group,
                        level_info = level_info,
                        form = form,
                        db_error = update_error,
                        type_name = self.type_name
                )
        else:
            self.render(
                    "admin/level_changetype.html",
                    username = self.username,
                    group = self.group,
                    level_info = level_info,
                    form = form,
                    db_error = None,
                    type_name = self.type_name
            )

class UserListHandler(BaseHandler):
    '''List users according to page.'''
    @tornado.web.authenticated
    def get(self):
        if self.group != '1':
            self.render("404.html", username=self.username, group=self.group)

        user_count = get_user_count(self.session)
        page_count = get_page_count(user_count, self.page_size)

        try:
            page = int(self.get_argument("page", '1'))
            page = 1 if page < 1 else page
        except ValueError:
            page = 1

        pages = self.get_pages(page, page_count)

        users = get_users(self.session, page, self.page_size)

        self.render(
                "admin/user_list.html", 
                username=self.username,
                group=self.group, 
                users=users, 
                page=page, 
                pages=pages, 
                page_size=self.page_size,
                user_count=user_count, 
                status_name=self.status_name,
                group_name=self.group_name
        )
    
class UserShowHandler(BaseHandler):
    '''Show detail information of some user.'''
    @tornado.web.authenticated
    def get(self, id):
        if self.group != '1':
            self.render("404.html", username=self.username, group=self.group)

        user_info = get_user_info_by_id(self.session, id)

        if user_info == None:
            self.render("404.html", username=self.username, group=self.group)

        self.render(
                "admin/user_detail.html", 
                username=self.username,
                group=self.group, 
                status_name=self.status_name,
                group_name=self.group_name,
                user_info=user_info
        )

class UserEditHandler(BaseHandler):
    '''Edit information of some user.'''
    @tornado.web.authenticated
    def get(self, id):
        if self.group != '1':
            self.render("404.html", username=self.username, group=self.group)

        user_info = get_user_info_by_id(self.session, id)

        form = UserEditForm()
        form.status.choices = [(k, v) for k, v in self.status_name.iteritems()]
        form.status.choices.sort()
        form.group.choices = [(k, v) for k, v in self.group_name.iteritems()]
        form.group.choices.sort()

        if user_info is None:
             self.render("404.html", username=self.username, group=self.group)

        self.render(
                "admin/user_edit.html", 
                username=self.username,
                group=self.group, 
                status_name=self.status_name,
                group_name=self.group_name, 
                form=form, 
                db_error=None,
                user_info=user_info
        )

    @tornado.web.authenticated
    def post(self, id):
        if self.group != '1':
            self.render("404.html", username=self.username, group=self.group)

        arguments = {
                'username': self.get_argument("username"),
                'email': self.get_argument("email"),
                'password': self.get_argument("password"),
                'status': self.get_argument("status"),
                'group': self.get_argument("group"),
        }

        form = UserEditForm(self.request.arguments)
        form.status.choices = [(k, v) for k, v in self.status_name.iteritems()]
        form.status.choices.sort()
        form.group.choices = [(k, v) for k, v in self.group_name.iteritems()]
        form.group.choices.sort()
        
        user_info = get_user_info_by_id(self.session, id)
        if user_info is None:
             self.render("404.html", username=self.username, group=self.group)
        update_error = user_update_validation(self.session, 
                user_info, self.uid, arguments)
        
        if form.validate():
            if update_error == "":
                update_user_info(self.session, user_info, arguments)
                self.redirect("/admin/user/show/" + id)
            else:
                self.render(
                        "admin/user_edit.html", 
                        username=self.username,
                        group=self.group, 
                        status_name=self.status_name,
                        group_name=self.group_name, 
                        form=form,
                        db_error=update_error, 
                        user_info=user_info
                )
        else:
            self.render(
                    "admin/user_edit.html", 
                    username=self.username,
                    group=self.group, 
                    status_name=self.status_name,
                    group_name=self.group_name, 
                    form=form, 
                    db_error=None,
                    user_info=user_info
            )

class UserDeleteHandler(BaseHandler):
    '''Delete user.'''
    @tornado.web.authenticated
    def post(self):
        if self.group != '1':
            self.render("404.html", username=self.username, group=self.group)

        id = self.get_argument("id")
        error_info = delete_user(self.session, id)
        self.write(error_info)

class SettingsHandler(BaseHandler):
    '''Change settings.

    page_size: User number to show per page.
    status_name: User status name.
    group_name: User group name.
    type_name: Level type name.'''
    @tornado.web.authenticated
    def get(self):
        if self.group != '1':
            self.render("404.html", username=self.username, group=self.group)

        settings = get_settings(self.session)

        form = SettingsForm()

        self.render(
                "admin/settings.html",
                username = self.username,
                group = self.group,
                settings = settings,
                form = form,
                db_error = None
        )

    @tornado.web.authenticated
    def post(self):
        if self.group != '1':
            self.render("404.html", username=self.username, group=self.group)

        arguments = {
                "page_size": self.get_argument("pagesize"),
                "status_name": self.get_argument("statusname"),
                "group_name": self.get_argument("groupname"),
                "type_name": self.get_argument("typename"),
        }

        settings = get_settings(self.session)

        form = SettingsForm(self.request.arguments)

        update_error = settings_update_validation(self.session)

        if form.validate():
            if update_error == "":
                update_settings(self.session, settings, arguments)
                self.redirect("/admin/settings")
            else:
                self.render(
                        "/admin/settings.html",
                        username = self.username,
                        group = self.group,
                        settings = settings,
                        form = form,
                        db_error = update_error
                )
        else:
            self.render(
                    "/admin/settings.html",
                    username = self.username,
                    group = self.group,
                    settings = settings,
                    form = form,
                    db_error = None
            )
