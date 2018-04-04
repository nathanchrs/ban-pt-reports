# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class Todo(http.Controller):

    @http.route('/helloworld', auth='public')
    def hello_world(self):
        """
        Basic Hello World example
        """
        return '<h1>Hello World!</h1>'

    @http.route('/hello', auth='public')
    def hello(self, **kwargs):
        """
        Hello World using a QWeb template
        Also used for the controller extension example
        """
        return request.render('itb_hr.hello')