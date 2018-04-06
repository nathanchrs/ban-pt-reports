# -*- coding: utf-8 -*-

from odoo import models, fields, api
from . import dosen
from . import identitas
from . import pengisi
from . import record_3a_311
from . import record_3a_312
from . import record_3a_314
from . import record_3a_331
from . import record_3a_431
from . import record_3a_432
from . import record_3a_433
from . import record_3a_434
from . import record_3a_435
from . import record_3a_441
from . import record_3a_442
from . import record_3a_451
from . import record_3a_452
from . import record_3a_453
from . import record_3a_454
from . import record_3a_455
from . import record_3a_461
from . import record_3a_5121
from . import record_3a_5122
from . import record_3a_513
from . import record_3a_541
from . import record_3a_551
from . import record_3a_6211
from . import record_3a_6212
from . import record_3a_622
from . import record_3a_623
from . import record_3a_631

class Report(models.Model):
    _name = 'banpt_report_generator.report'

    name = fields.Char(string='Judul', required=True)
    state = fields.Selection(string='Status', required=True, selection=[('pending_review', 'Menunggu review'), ('approved', 'Disetujui')], default='pending_review')
    year = fields.Selection(string='Tahun', required=True, selection=[(year, str(year)) for year in range(2010, 2050)])
    prodi = fields.Many2one(string='Prodi', required=True, comodel_name='itb.academic_program')
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
    record_3a_441 = fields.One2many(comodel_name='banpt_report_generator.record_3a_441', inverse_name='report')
    record_3a_442 = fields.One2many(comodel_name='banpt_report_generator.record_3a_442', inverse_name='report')
    record_3a_451 = fields.One2many(comodel_name='banpt_report_generator.record_3a_451', inverse_name='report')
    record_3a_452 = fields.One2many(comodel_name='banpt_report_generator.record_3a_452', inverse_name='report')
    record_3a_453 = fields.One2many(comodel_name='banpt_report_generator.record_3a_453', inverse_name='report')
    record_3a_454 = fields.One2many(comodel_name='banpt_report_generator.record_3a_454', inverse_name='report')
    record_3a_455 = fields.One2many(comodel_name='banpt_report_generator.record_3a_455', inverse_name='report')
    record_3a_461 = fields.One2many(comodel_name='banpt_report_generator.record_3a_461', inverse_name='report')
    record_3a_5121 = fields.One2many(comodel_name='banpt_report_generator.record_3a_5121', inverse_name='report')
    record_3a_5122 = fields.One2many(comodel_name='banpt_report_generator.record_3a_5122', inverse_name='report')
    record_3a_513 = fields.One2many(comodel_name='banpt_report_generator.record_3a_513', inverse_name='report')
    record_3a_541 = fields.One2many(comodel_name='banpt_report_generator.record_3a_541', inverse_name='report')
    record_3a_551 = fields.One2many(comodel_name='banpt_report_generator.record_3a_551', inverse_name='report')
    record_3a_6211 = fields.One2many(comodel_name='banpt_report_generator.record_3a_6211', inverse_name='report')
    record_3a_6212 = fields.One2many(comodel_name='banpt_report_generator.record_3a_6212', inverse_name='report')
    record_3a_622 = fields.One2many(comodel_name='banpt_report_generator.record_3a_622', inverse_name='report')
    record_3a_623 = fields.One2many(comodel_name='banpt_report_generator.record_3a_623', inverse_name='report')
    record_3a_631 = fields.One2many(comodel_name='banpt_report_generator.record_3a_631', inverse_name='report')

    @api.multi
    def write(self, values):
        "Set state to 'pending_review' if object is edited."
        values['state'] = 'pending_review'
        return super(Report, self).write(values)

    @api.multi
    def approve(self):
        "Set state to 'approved'; bypass edit object check."
        super(Report, self).write({'state': 'approved'})

    @api.multi
    def refresh(self):
        "Load or refresh report data from iBOS, then update the refresh_date."

        dosen.refresh(self)
        identitas.refresh(self)
        pengisi.refresh(self)
        record_3a_311.refresh(self)
        record_3a_312.refresh(self)
        record_3a_314.refresh(self)
        record_3a_331.refresh(self)
        record_3a_431.refresh(self)
        record_3a_432.refresh(self)
        record_3a_433.refresh(self)
        record_3a_434.refresh(self)
        record_3a_435.refresh(self)
        record_3a_441.refresh(self)
        record_3a_442.refresh(self)
        record_3a_451.refresh(self)
        record_3a_452.refresh(self)
        record_3a_453.refresh(self)
        record_3a_454.refresh(self)
        record_3a_455.refresh(self)
        record_3a_461.refresh(self)
        record_3a_5121.refresh(self)
        record_3a_5122.refresh(self)
        record_3a_513.refresh(self)
        record_3a_541.refresh(self)
        record_3a_551.refresh(self)
        record_3a_6211.refresh(self)
        record_3a_6212.refresh(self)
        record_3a_622.refresh(self)
        record_3a_623.refresh(self)
        record_3a_631.refresh(self)

        self.write({'refresh_date': fields.datetime.now()})
