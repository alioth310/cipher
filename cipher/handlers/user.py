#! /usr/bin/python
# -*- coding: utf-8 -*-

from hashlib import md5

import tornado.web

from forms import LoginForm, SignupForm, ChangePasswordForm
from models.user import update_last_visit, signup, \
        get_user_info_by_name, login_validation, \
        password_validation, change_password, signup_validation
from models.cipher import get_current_level, get_levels
from handlers.basehandler import BaseHandler

class LoginHandler(BaseHandler):
    def get(self):
        form = LoginForm()
        self.render("login.html", username=None, group=None,
                form=form, db_error=None)

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")

        login_error = login_validation(self.session, username, password)

        form = LoginForm(self.request.arguments)

        if form.validate():
            if login_error == "":
                user_info = get_user_info_by_name(self.session, username)
                update_last_visit(self.session, username, self.get_ip())
                self.set_cookies(user_info)
                self.redirect("/")
            else:
                self.render("login.html", username=None, group=None,
                        form=form, db_error=login_error)
        else:
            self.render("login.html", username=None, group=None,
                    form=form, db_error=None)

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_all_cookies()
        self.redirect("/")

class SignupHandler(BaseHandler):
    def get(self):
        form = SignupForm()
        self.render("signup.html", username=None, group=None,
                form=form, db_error=None)

    def post(self):
        username = self.get_argument("username")
        email = self.get_argument("email")
        password = self.get_argument("password")
        confirm_password = self.get_argument("confirm_password")
        
        form = SignupForm(self.request.arguments)

        signup_error = signup_validation(self.session, username)

        if form.validate():
            if signup_error == "":
                signup(self.session, username, email, password, self.get_ip())
                user_info = get_user_info_by_name(self.session, username)
                self.set_cookies(user_info)
                self.redirect("/")
            else:
                self.render("signup.html", username=None, group=None,
                        form=form, db_error=signup_error)
        else:
            self.render("signup.html", username=None, group=None, 
                    form=form, db_error=None)
        

class LevelChooseHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        current_level = get_current_level(self.session, self.uid)
        levels = get_levels(self.session, current_level)
        self.render("chooselevel.html", username=self.username, 
                group=self.group, levels=levels)

class PasswordChangeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        form = ChangePasswordForm()
        self.render("changepassword.html", username=self.username,
                group=self.group, form=form, db_error=None)

    @tornado.web.authenticated
    def post(self):
        old_password = self.get_argument("old_password")
        new_password = self.get_argument("new_password")
        confirm_password = self.get_argument("confirm_password")

        form = ChangePasswordForm(self.request.arguments)

        password_error = password_validation(self.session, self.uid,
                old_password)

        if form.validate():
            if password_error == "":
                change_password(self.session, self.uid, new_password)
                self.redirect("/")
            else:
                self.render("changepassword.html", username=self.username,
                        group=self.group, form=form, db_error=password_error)
        else:
            self.render("changepassword.html", username=self.username,
                    group=self.group, form=form, db_error=None)

