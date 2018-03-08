# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Report(models.Model):
    _name = 'banpt_report_generator.report'

    name = fields.Char(string='Judul', required=True)
    state = fields.Selection(string='Status', required=True, selection=[('pending_review', 'Menunggu review'), ('approved', 'Disetujui')], default='pending_review') 
    start_year = fields.Integer(string='Tahun awal', required=True)
    end_year = fields.Integer(string='Tahun akhir', required=True)
    department = fields.Char(string='Prodi', required=True)
    description = fields.Text()

    @api.model
    def create(self, values):
        record = super(Report, self).create(values)
        print('[Report]: create(vals) override') # DEBUG
        print(values)
        return record

    @api.one
    def approve(self):
        self.write({
            'state': 'approved'
        })
