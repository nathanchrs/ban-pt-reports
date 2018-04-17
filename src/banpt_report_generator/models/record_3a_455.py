# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import models, fields, api

class Record_3A_455(models.Model):
    _name = 'banpt_report_generator.record_3a_455'
    _rec_name = 'nama'
    _title = '3A-4.5.5 Keikutsertaan Dosen Tetap Dalam Organisasi Keilmuan/Profesi'

    nama = fields.Char(string='Nama', required=True)
    nama_organisasi = fields.Text(string='Nama Organisasi Keilmuan atau Organisasi Profesi')
    tahun_awal = fields.Char(string='Kurun Waktu Tahun Awal')
    tahun_akhir = fields.Char(string='Kurun Waktu Tahun Akhir')
    tingkat_internasional = fields.Boolean(string='Tingkat Internasional')
    tingkat_nasional = fields.Boolean(string='Tingkat Nasional')
    tingkat_lokal = fields.Boolean(string='Tingkat Lokal')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        report.record_3a_455.unlink()

        instructors = reports.env['hr.employee'].search([['is_faculty', '=', True], ['prodi', '=', report.prodi.id]])
        for instructor in instructors:
            memberships = reports.env['itb.hr_membership'].search([['employee_id', '=', instructor.id]])
            for membership in memberships:
                start_date = datetime.strptime(membership.start, "%Y-%m-%d")
                end_date = datetime.strptime(membership.finish, "%Y-%m-%d")
                new_record_3a_455 = {
                    'nama': instructor.name,
                    'nama_organisasi': membership.name,
                    'tahun_awal': start_date.year,
                    'tahun_akhir': end_date.year,
                    'tingkat_lokal': True if membership.level == 'local' else False,
                    'tingkat_nasional': True if membership.level == 'national' else False,
                    'tingkat_internasional': True if membership.level == 'global' else False,
                }

                report.write({'record_3a_455': [(0, 0, new_record_3a_455)]})
