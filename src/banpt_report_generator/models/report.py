# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Report(models.Model):
    _name = 'banpt_report_generator.report'

    name = fields.Char(string='Judul', required=True)
    state = fields.Selection(string='Status', required=True, selection=[('pending_review', 'Menunggu review'), ('approved', 'Disetujui')], default='pending_review') 
    year = fields.Selection(string='Tahun', required=True, selection=[(year, str(year)) for year in range(2010, 2050)])
    prodi = fields.Char(string='Prodi', required=True)
    description = fields.Text(string='Keterangan')

    pengisi = fields.One2many(comodel_name='banpt_report_generator.pengisi', inverse_name='report')
    identitas = fields.One2many(comodel_name='banpt_report_generator.identitas', inverse_name='report')
    dosen = fields.One2many(comodel_name='banpt_report_generator.dosen', inverse_name='report')

    @api.model
    def create(self, values):
        record = super(Report, self).create(values)

        # TODO: generate reports here

        return record

    @api.multi
    def write(self, values, ignore_state_change=False):
        # Set state to 'pending_review' if object is edited
        values['state'] = 'pending_review'
        return super(Report, self).write(values)

    @api.one
    def approve(self):
        # Set state to 'approved'; bypass edit object check
        super(Report, self).write({'state': 'approved'})
