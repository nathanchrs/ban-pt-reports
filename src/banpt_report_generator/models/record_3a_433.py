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
        dosen_employees = reports.env['hr.employee'].search([['is_faculty', '=', True], ['prodi', '=', report.prodi.id]]) # TODO; add WHERE statement with sesuai prodi
        for dosen in dosen_employees:
            instructors_even = reports.env['itb.academic_instructor'].search([['employee_id', '=', dosen.id], ['semester', '=', semester_even.name]])
            instructors_odd = reports.env['itb.academic_instructor'].search([['employee_id', '=', dosen.id], ['semester', '=', semester_odd.name]])
            sks_ps_sendiri = 0
            sks_ps_lain_pt_sendiri = 0
            sks_mgmt_pt_sendiri = 0
            for instructor_even in instructors_even:
                if instructor_even.course_id.program_id.id == report.prodi.id:
                    sks_ps_sendiri += instructor_even.credit
                    if 'Manajemen' in instructor_even.course_id.name:
                        sks_mgmt_pt_sendiri += instructor_even.credit
                else:
                    sks_ps_lain_pt_sendiri += instructor_even.credit
                    if 'Manajemen' in instructor_even.course_id.name:
                        sks_mgmt_pt_sendiri += instructor_even.credit
            for instructor_odd in instructors_odd:
                if instructor_odd.course_id.program_id.id == report.prodi.id:
                    sks_ps_sendiri += instructor_odd.credit
                    if 'Manajemen' in instructor_odd.course_id.name:
                        sks_mgmt_pt_sendiri += instructor_odd.credit
                else:
                    sks_ps_lain_pt_sendiri += instructor_odd.credit
                    if 'Manajemen' in instructor_odd.course_id.name:
                        sks_mgmt_pt_sendiri += instructor_odd.credit

            new_record_3a_433 = {
                'nama_dosen': dosen.name_related,
                'sks_ps_sendiri': sks_ps_sendiri,
                'sks_ps_lain_pt_sendiri': sks_ps_lain_pt_sendiri,
                'sks_pt_lain': 0, # TODO: need more information
                'sks_penelitian': 0, # TODO: need more information
                'sks_pengmas': 0, # TODO: need more information
                'sks_mgmt_pt_sendiri': sks_mgmt_pt_sendiri,
                'sks_mgmt_pt_lain': 0, # TODO: need more information
                'sks_total': sks_ps_sendiri + sks_ps_lain_pt_sendiri,
            }

            report.write({'record_3a_433': [(0, 0, new_record_3a_433)]})
