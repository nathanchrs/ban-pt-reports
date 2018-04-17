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
from . import record_3a_632
from . import record_3a_633
from . import record_3a_6411
from . import record_3a_6412
from . import record_3a_643
from . import record_3a_652
from . import record_3a_711
from . import record_3a_712
from . import record_3a_713
from . import record_3a_714
from . import record_3a_721
from . import record_3a_731
from . import record_3a_732
from . import record_3b_312
from . import record_3b_321
from . import record_3b_411
from . import record_3b_412
from . import record_3b_42
from . import record_3b_6111
from . import record_3b_6112
from . import record_3b_6113
from . import record_3b_642
from . import record_3b_711
from . import record_3b_721

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
    record_3a_632 = fields.One2many(comodel_name='banpt_report_generator.record_3a_632', inverse_name='report')
    record_3a_633 = fields.One2many(comodel_name='banpt_report_generator.record_3a_633', inverse_name='report')
    record_3a_6411 = fields.One2many(comodel_name='banpt_report_generator.record_3a_6411', inverse_name='report')
    record_3a_6412 = fields.One2many(comodel_name='banpt_report_generator.record_3a_6412', inverse_name='report')
    record_3a_643 = fields.One2many(comodel_name='banpt_report_generator.record_3a_643', inverse_name='report')
    record_3a_652 = fields.One2many(comodel_name='banpt_report_generator.record_3a_652', inverse_name='report')
    record_3a_711 = fields.One2many(comodel_name='banpt_report_generator.record_3a_711', inverse_name='report')
    record_3a_712 = fields.One2many(comodel_name='banpt_report_generator.record_3a_712', inverse_name='report')
    record_3a_713 = fields.One2many(comodel_name='banpt_report_generator.record_3a_713', inverse_name='report')
    record_3a_714 = fields.One2many(comodel_name='banpt_report_generator.record_3a_714', inverse_name='report')
    record_3a_721 = fields.One2many(comodel_name='banpt_report_generator.record_3a_721', inverse_name='report')
    record_3a_731 = fields.One2many(comodel_name='banpt_report_generator.record_3a_731', inverse_name='report')
    record_3a_732 = fields.One2many(comodel_name='banpt_report_generator.record_3a_732', inverse_name='report')
    record_3b_312 = fields.One2many(comodel_name='banpt_report_generator.record_3b_312', inverse_name='report')
    record_3b_321 = fields.One2many(comodel_name='banpt_report_generator.record_3b_321', inverse_name='report')
    record_3b_411 = fields.One2many(comodel_name='banpt_report_generator.record_3b_411', inverse_name='report')
    record_3b_412 = fields.One2many(comodel_name='banpt_report_generator.record_3b_412', inverse_name='report')
    record_3b_42 = fields.One2many(comodel_name='banpt_report_generator.record_3b_42', inverse_name='report')
    record_3b_6111 = fields.One2many(comodel_name='banpt_report_generator.record_3b_6111', inverse_name='report')
    record_3b_6112 = fields.One2many(comodel_name='banpt_report_generator.record_3b_6112', inverse_name='report')
    record_3b_6113 = fields.One2many(comodel_name='banpt_report_generator.record_3b_6113', inverse_name='report')
    record_3b_642 = fields.One2many(comodel_name='banpt_report_generator.record_3b_642', inverse_name='report')
    record_3b_711 = fields.One2many(comodel_name='banpt_report_generator.record_3b_711', inverse_name='report')
    record_3b_721 = fields.One2many(comodel_name='banpt_report_generator.record_3b_721', inverse_name='report')

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
        record_3a_632.refresh(self)
        record_3a_633.refresh(self)
        record_3a_6411.refresh(self)
        record_3a_6412.refresh(self)
        record_3a_643.refresh(self)
        record_3a_652.refresh(self)
        record_3a_711.refresh(self)
        record_3a_712.refresh(self)
        record_3a_713.refresh(self)
        record_3a_714.refresh(self)
        record_3a_721.refresh(self)
        record_3a_731.refresh(self)
        record_3a_732.refresh(self)
        record_3b_312.refresh(self)
        record_3b_321.refresh(self)
        record_3b_411.refresh(self)
        record_3b_412.refresh(self)
        record_3b_42.refresh(self)
        record_3b_6111.refresh(self)
        record_3b_6112.refresh(self)
        record_3b_6113.refresh(self)
        record_3b_642.refresh(self)
        record_3b_711.refresh(self)
        record_3b_721.refresh(self)

        self.write({'refresh_date': fields.datetime.now()})
