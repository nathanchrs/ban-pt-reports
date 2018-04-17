# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class Example(http.Controller):
    #@http.route(['/abet'], type='http', auth='public', website=True)
    @http.route(['/abet'], auth='public')
    def render_abet(self, **kwargs):
        #return http.request.render('itb_hr.example_page', {})
        #return request.website.render('itb_hr.abet', {})
        return "Hello, World"

    @http.route(['/abet/detail'], type='http', auth="public", website=True)
    def navigate_to_detail_page(self, **kwargs):
        # This will get all company details (in case of multicompany this are multiple records)
        companies = http.request.env['res.company'].sudo().search([])
        return request.website.render('itb_hr.detail_page', {
          # pass company details to the webpage in a variable
          'companies': companies})