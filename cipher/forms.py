#! /usr/bin/python
# -*- coding: utf-8 -*-

import re

from tornado.escape import to_unicode
import tornado.locale
_ = tornado.locale.get('zh_CN').translate  # Just a Hack for xgettext

from wtforms import Form as wtForm
from wtforms import validators
from wtforms import TextField, PasswordField, SubmitField, RadioField, \
        FileField, HiddenField, TextAreaField

class Form(wtForm):
    """
    Using this Form instead of wtforms.Form

    Modified from http://github.com/lepture/tornado.ext

    """
    def __init__(self, formdata=None, obj=None, prefix='', **kwargs):
        super(Form, self).__init__(formdata, obj, prefix, **kwargs)

    def process(self, formdata=None, obj=None, **kwargs):
        if formdata is not None and not hasattr(formdata, 'getlist'):
            formdata = TornadoArgumentsWrapper(formdata)
        super(Form, self).process(formdata, obj, **kwargs)

class TornadoArgumentsWrapper(dict):
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError

    def getlist(self, key):
        try:
            values = []
            for v in self[key]:
                v = to_unicode(v)
                if isinstance(v, unicode):
                    v = re.sub(r"[\x00-\x08\x0e-\x1f]", " ", v)
                values.append(v)
            return values
        except KeyError:
            raise AttributeError

class LoginForm(Form):
    username = TextField(_("Username"), [
        validators.Required(message=_("Username should not be blank")),
        validators.Length(min=1, max=64, 
            message=_("Username length should less than 64")),
    ])
    password = PasswordField(_("Password"), [
        validators.Required(message=_("Password shoule not be blank")),
        validators.Length(min=1, max=32, 
            message=_("Password length should less than 32")),
    ])
    login = SubmitField(_("Login"))

class ChangePasswordForm(Form):
    old_password = PasswordField(_("Old Password"), [
        validators.Required(message=_("Old password should not be blank")),
    ])
    new_password = PasswordField(_("New Password"), [
        validators.Required(message=_("New password should not be blank")),
        validators.Length(min=1, max=32,
            message=_("New password length should less than 32")),
    ])
    confirm_password = PasswordField(_("Confirm Password"), [
        validators.EqualTo("new_password", 
            message=_("New password you entered twice is different")),
    ])
    submit = SubmitField(_("Submit"))

class SignupForm(Form):
    username = TextField(_("Username"), [
        validators.Required(message=_("Username should not be blank")),
        validators.Regexp(r"^\S+$", message=_("Username is not valid")),
        validators.Length(min=1, max=64, 
            message=_("Username length should less than 64")),
    ])
    email = TextField(_("Email"), [
        validators.Required(message=_("Email should not be blank")),
        validators.Email(message=_("Email address is not valid")),
        validators.Length(min=4, max=64, 
            message=_("Email length should less than 64")),
    ])
    password = PasswordField(_("Password"), [
        validators.Required(message=_("Password should not be blank")),
        validators.Length(min=1, max=32,
            message=_("Password length should less than 32")),
    ])
    confirm_password = PasswordField(_("Confirm Password"), [
        validators.EqualTo("password", 
            message=_("Password you entered twice is different")),
    ])
    signup = SubmitField(_("Sign up"))

class UserEditForm(Form):
    username = TextField(_("Username"), [
        validators.Required(message=_("Username should not be blank")),
        validators.Regexp(r"^\S+$", message=_("Username is not valid")),
        validators.Length(min=1, max=64, 
            message=_("Username length should less than 64")),
    ])
    email = TextField(_("Email"), [
        validators.Required(message=_("Email should not be blank")),
        validators.Email(message=_("Email address is not valid")),
        validators.Length(min=4, max=64, 
            message=_("Email length should less than 64")),
    ])
    password = PasswordField(_("Password"), [
        validators.Length(min=0, max=32,
            message=_("Password length should less than 32")),
    ])
    status = RadioField('0')
    group = RadioField('0')
    submit = SubmitField(_("Submit"))

class LevelTypeChangeForm(Form):
    type = RadioField('1')
    submit = SubmitField(_("Submit"))

class CommonLevelForm(Form):
    level = TextField(_("Level"), [
        validators.Required(message=_("Level should not be blank")),
        validators.Regexp(r"^\d+$", message=_("Level should be a number")),
    ])
    step = TextField(_("Step"), [
        validators.Required(message=_("Step should not be blank")),
        validators.Regexp(r"^\d+$", message=_("Step should be a number")),
    ])
    type = HiddenField("0")
    dirname = TextField(_("Dir Name"), [
        validators.Required(message=_("Dir name should not be blank")),
        validators.Regexp(r"^[\d\w_]+$", message=_("Dir name is invalid")),
    ])
    pagename = TextField(_("Page Name"), [
        validators.Required(message=_("Page name should not be blank")),
        validators.Regexp(r"^[\d\w_]+$", message=_("Page name is invalid")),
    ])
    title = TextField(_("Title"), [
        validators.Required(message=_("Title should not be blank")),
    ])
    image = FileField(_("Image File"), [
        validators.Optional(),
        #validators.Regexp(r"^[^/\\]\.(jpg|jpeg|gif|png)$", 
        #    message=_("Image File is invalid"))
    ])
    imgname = TextField(_("Image Name"), [
        validators.Required(message=_("Image name should not be blank")),
        validators.Regexp(r"^[\d\w_\.]+$", message=_("Image name is invalid")),
    ])
    imgalt = TextField(_("Image Alt"), [])
    hint = TextField(_("Hint"), [])
    hiddencode = TextAreaField("Hidden code")
    redirectto = TextField(_("Redirect To"), [
        validators.Regexp(r"^[\d\w_/]*$", message=_("Redirect URL is invalid"))
    ])
    redirecttime = TextField(_("Redirect time"), [
        validators.Regexp(r"^[\d]*$", message=_("Redirect time is invalid"))
    ])
    submit = SubmitField(_("Submit"))

class PureTextLevelForm(Form):
    level = TextField(_("Level"), [
        validators.Required(message=_("Level should not be blank")),
        validators.Regexp(r"^\d+$", message=_("Level should be a number")),
    ])
    step = TextField(_("Step"), [
        validators.Required(message=_("Step should not be blank")),
        validators.Regexp(r"^\d+$", message=_("Step should be a number")),
    ])
    type = HiddenField("1")
    dirname = TextField(_("Dir Name"), [
        validators.Required(message=_("Dir name should not be blank")),
        validators.Regexp(r"^[\d\w_]+$", message=_("Dir name is invalid")),
    ])
    pagename = TextField(_("Page Name"), [
        validators.Required(message=_("Page name should not be blank")),
        validators.Regexp(r"^[\d\w_]+$", message=_("Page name is invalid")),
    ])
    title = TextField(_("Title"), [
        validators.Required(message=_("Title should not be blank")),
    ])
    hiddencode = TextAreaField("Hidden code")
    puretexth1 = TextField(_("Pure Text h1"), [])
    puretextp = TextAreaField(_("Pure Text p"), [])
    submit = SubmitField(_("Submit"))

class RedirectLevelForm(Form):
    level = TextField(_("Level"), [
        validators.Required(message=_("Level should not be blank")),
        validators.Regexp(r"^\d+$", message=_("Level should be a number")),
    ])
    step = TextField(_("Step"), [
        validators.Required(message=_("Step should not be blank")),
        validators.Regexp(r"^\d+$", message=_("Step should be a number")),
    ])
    type = HiddenField("2")
    dirname = TextField(_("Dir Name"), [
        validators.Required(message=_("Dir name should not be blank")),
        validators.Regexp(r"^[\d\w_]+$", message=_("Dir name is invalid")),
    ])
    pagename = TextField(_("Page Name"), [
        validators.Required(message=_("Page name should not be blank")),
        validators.Regexp(r"^[\d\w_]+$", message=_("Page name is invalid")),
    ])
    title = TextField(_("Title"), [
        validators.Required(message=_("Title should not be blank")),
    ])
    redirectto = TextField(_("Redirect To"), [
        validators.Regexp(r"^[\d\w_/]*$", message=_("Redirect URL is invalid"))
    ])
    redirecttime = TextField(_("Redirect time"), [
        validators.Regexp(r"^[\d]*$", message=_("Redirect time is invalid"))
    ])
    submit = SubmitField(_("Submit"))

class SettingsForm(Form):
    pagesize = TextField(_("Page Size"), [
        validators.Required(message=_("Page size should not be blank")),
        validators.Regexp(r"^\d+$", message=_("Page size should be a number")),
    ])
    statusname = TextField(_("Status Name"), [
        validators.Required(message=_("Status name should not be blank")),
    ])
    groupname = TextField(_("Group Name"), [
        validators.Required(message=_("Group name should not be blank")),
    ])
    typename = TextField(_("Cipher Type Name"), [
        validators.Required(message=_("Cipher type name should not be blank")),
    ])
    submit = SubmitField(_("Submit"))

