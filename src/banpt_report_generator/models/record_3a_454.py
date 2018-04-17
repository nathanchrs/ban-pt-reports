# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta

class Record_3A_454(models.Model):
    _name = 'banpt_report_generator.record_3a_454'
    _rec_name = 'nama'
    _title = '3A-4.5.4 Pencapai Prestasi/Reputasi Dosen'

    nama = fields.Char(string='Nama', required=True)
    prestasi_yang_dicapai = fields.Text(string='Prestasi yang Dicapai')
    tahun_pencapaian = fields.Char(string='Tahun Pencapaian')
    tingkat_internasional = fields.Boolean(string='Tingkat Internasional', default=False)
    tingkat_nasional = fields.Boolean(string='Tingkat Nasional', default=False)
    tingkat_lokal = fields.Boolean(string='Tingkat Lokal', default=False)

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        report.record_3a_454.unlink()

        instructors = reports.env['hr.employee'].search([['is_faculty', '=', True], ['prodi', '=', report.prodi.id]])
        for instructor in instructors:
            awards = reports.env['itb.hr_award'].search([['employee_id', '=', instructor.id]])
            for award in awards:
                new_record_3a_454 = {
                    'nama': instructor.name,
                    'prestasi_yang_dicapai': award.name,
                    'tahun_pencapaian': award.start,
                    'tingkat_lokal': True if award.level == 'local' else False,
                    'tingkat_nasional': True if award.level == 'national' else False,
                    'tingkat_internasional': True if award.level == 'global' else False,
                }

                report.write({'record_3a_454': [(0, 0, new_record_3a_454)]})
            
