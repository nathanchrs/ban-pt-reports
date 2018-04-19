# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_551(models.Model):
    _name = 'banpt_report_generator.record_3a_551'
    _rec_name = 'nama_dosen'
    _title = '3A-5.5.1 Dosen Pembimbing Tugas Akhir dan Jumlah Mahasiswa'

    nama_dosen = fields.Text(string='Nama Dosen Pembimbing Akademik', required=True)
    jumlah_mahasiswa_bimbingan = fields.Integer(string='Jumlah Mahasiswa Bimbingan', required=True)

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear record_3a_551 table
        report.record_3a_551.unlink()

        # add record_3a_551 according to program_id
        instructors = reports.env['hr.employee'].search([['is_faculty', '=', True], ['prodi', '=', report.prodi.id]])
        for instructor in instructors:
            new_record_3a_551 = {
                'nama': instructor.name_related,
                'jumlah_mahasiswa_bimbingan': 0,
            }

            report.write({'record_3a_551': [(0, 0, new_record_3a_551)]})
