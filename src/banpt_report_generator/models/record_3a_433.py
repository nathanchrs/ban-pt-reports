# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_433(models.Model):
    _name = 'banpt_report_generator.record_3a_433'
    _rec_name = 'nama_dosen'
    _title = '3A-4.3.3 Aktivitas Dosen Tetap yang Bidang Keahliannya Sesuai Dengan PS'

    nama_dosen = fields.Char(string='Nama Dosen Tetap', required=True)
    sks_ps_sendiri = fields.Integer(string='SKS Pengajaran Pada PS Sendiri')
    sks_ps_lain_pt_sendiri = fields.Integer(string='SKS Pengajaran Pada PS Lain, PT Sendiri')
    sks_pt_lain = fields.Integer(string='SKS Pengajaran Pada PT Lain')
    sks_penelitian = fields.Integer(string='SKS Penelitian')
    sks_pengmas = fields.Integer(string='SKS Pengabdian Pada Masyarakat')
    sks_mgmt_pt_sendiri = fields.Integer(string='SKS Manajemen PT Sendiri')
    sks_mgmt_pt_lain = fields.Integer(string='SKS Manajemen PT Lain')
    sks_total = fields.Integer(string='Jumlah SKS')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear Record_3A_433 table
        report.record_3a_433.unlink()

        # Add aktivitas dosen tetap
        semester_even = reports.env['itb.academic_semester'].search([['year', '=', report.year], ['type', '=', 'even']])
        semester_odd = reports.env['itb.academic_semester'].search([['year', '=', report.year - 1], ['type', '=', 'odd']])
        instructors = reports.env['hr.employee'].search([['is_faculty', '=', True], ['prodi', '=', report.prodi.id]]) # TODO; add WHERE statement with sesuai prodi
        for instructor in instructors:
            course_evens = reports.env['itb.academic_course'].search([['semester_id', '=', semester_even.id], ['program_id', '=', 11]]) # TODO: change to instructor_id
            course_odds = reports.env['itb.academic_course'].search([['semester_id', '=', semester_odd.id], ['program_id', '=', 11]]) # TODO: change to instructor_id
            sks_ps_sendiri_even = 0
            sks_ps_sendiri_odd = 0
            for course_even in course_evens:
                catalog_even = reports.env['itb.academic_catalog'].search([['id', '=', course_even.catalog_id.id]])
                sks_ps_sendiri_even += catalog_even.credit
            for course_odd in course_odds:
                catalog_odd = reports.env['itb.academic_catalog'].search([['id', '=', course_odd.catalog_id.id]])
                sks_ps_sendiri_odd += catalog_odd.credit

            new_record_3a_433 = {
                'nama_dosen': instructor.name_related,
                'sks_ps_sendiri': sks_ps_sendiri_even,
                'sks_ps_lain_pt_sendiri': sks_ps_sendiri_odd,
                'sks_pt_lain': sks_ps_sendiri_even, # TODO: need more information
                'sks_penelitian': sks_ps_sendiri_odd, # TODO: need more information
                'sks_pengmas': semester_even.id, # TODO: need more information
                'sks_mgmt_pt_sendiri': semester_odd.id,
                'sks_mgmt_pt_lain': 0, # TODO: need more information
                'sks_total': 0,
            }

            report.write({'record_3a_433': [(0, 0, new_record_3a_433)]})
