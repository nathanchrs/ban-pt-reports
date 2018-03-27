# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Report(models.Model):
    _name = 'banpt_report_generator.report'

    name = fields.Char(string='Judul', required=True)
    state = fields.Selection(string='Status', required=True, selection=[('pending_review', 'Menunggu review'), ('approved', 'Disetujui')], default='pending_review')
    year = fields.Selection(string='Tahun', required=True, selection=[(year, str(year)) for year in range(2010, 2050)])
    prodi = fields.Char(string='Prodi', required=True)
    description = fields.Text(string='Keterangan')

    refresh_date = fields.Datetime(string='Waktu pemutakhiran terakhir', default=fields.datetime.now())

    dosen = fields.One2many(comodel_name='banpt_report_generator.dosen', inverse_name='report')
    identitas = fields.One2many(comodel_name='banpt_report_generator.identitas', inverse_name='report')
    pengisi = fields.One2many(comodel_name='banpt_report_generator.pengisi', inverse_name='report')
    record_3a_311 = fields.One2many(comodel_name='banpt_report_generator.record_3a_311', inverse_name='report')
    record_3a_312 = fields.One2many(comodel_name='banpt_report_generator.record_3a_312', inverse_name='report')
    record_3a_314 = fields.One2many(comodel_name='banpt_report_generator.record_3a_314', inverse_name='report')
    record_3a_331 = fields.One2many(comodel_name='banpt_report_generator.record_3a_331', inverse_name='report')
    record_3a_431 = fields.One2many(comodel_name='banpt_report_generator.record_3a_431', inverse_name='report')
    record_3a_432 = fields.One2many(comodel_name='banpt_report_generator.record_3a_432', inverse_name='report')
    record_3a_433 = fields.One2many(comodel_name='banpt_report_generator.record_3a_433', inverse_name='report')
    record_3a_434 = fields.One2many(comodel_name='banpt_report_generator.record_3a_434', inverse_name='report')
    record_3a_435 = fields.One2many(comodel_name='banpt_report_generator.record_3a_435', inverse_name='report')

    @api.multi
    def write(self, values):
        "Set state to 'pending_review' if object is edited"
        values['state'] = 'pending_review'
        return super(Report, self).write(values)

    @api.multi
    def approve(self):
        "Set state to 'approved'; bypass edit object check"
        super(Report, self).write({'state': 'approved'})

    @api.multi
    def refresh(self):
        "Load or refresh report data from iBOS, then update the refresh_date"

        # TODO: generate reports here based on year and prodi

        self.write({'refresh_date': fields.datetime.now()})
