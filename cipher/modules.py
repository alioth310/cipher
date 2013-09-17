#! /usr/bin/python
# -*- coding: utf-8 -*-

from handlers.formfieldmodule import *
from handlers.paginationmodule import *

modules = {
        'InputField': InputFieldModule,
        'ButtonField': ButtonFieldModule,
        'RadioField': RadioFieldModule,
        'TextAreaField': TextAreaFieldModule,
        'HiddenField': HiddenFieldModule,
        'FileField': FileFieldModule,
        'Pagination': PaginationModule,
}
