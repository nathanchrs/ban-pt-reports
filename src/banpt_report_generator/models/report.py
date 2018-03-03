# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Report(models.Model):
    _name = 'banpt_report_generator.report'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
