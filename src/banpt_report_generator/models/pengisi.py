# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_Pengisi(models.Model):
    _name = 'banpt_report_generator.pengisi'

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
