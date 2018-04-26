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
        semester_even = reports.env['itb.academic_semester'].search([
            ['year', '=', report.year],
            ['type', '=', 'even']
        ])

        semester_odd = reports.env['itb.academic_semester'].search([
            ['year', '=', report.year - 1],
            ['type', '=', 'odd']
        ])

        dosen_employees = reports.env['hr.employee'].search([
            ['is_faculty', '=', True],
            ['prodi', '=', report.prodi.id],
            ['employment_type', '!=', 'contract']
        ]) # TODO; add WHERE statement with dosen_tetap sesuai prodi

        for dosen in dosen_employees:
            instructors_even = reports.env['itb.academic_instructor'].search([
                ['employee_id', '=', dosen.id],
                ['semester', '=', semester_even.name]
            ])

            instructors_odd = reports.env['itb.academic_instructor'].search([
                ['employee_id', '=', dosen.id],
                ['semester', '=', semester_odd.name]
            ])

            projects_team = reports.env['itb.hr_project_team'].search([
                ['employee_id', '=', dosen.id]
            ])

            sks_ps_sendiri = 0
            sks_ps_lain_pt_sendiri = 0
            sks_penelitian = 0
            sks_pengmas = 0
            # sks_mgmt_pt_sendiri = 0

            for project_team in projects_team:
                project = reports.env['itb.hr_project'].search([
                    ['id', '=', project_team.project_id.id]
                ])
                if ((project.tahun >= report.year - 1) and ((project.tahun <= report.year)) and ('penelitian' in project.tipe)):
                    sks_penelitian += 1
                elif ((project.tahun >= report.year - 1) and ((project.tahun <= report.year)) and ('pengabdian' in project.tipe)):
                    sks_pengmas += 1

            for instructor_even in instructors_even:
                if instructor_even.course_id.program_id.id == report.prodi.id:
                    sks_ps_sendiri += instructor_even.credit
                else:
                    sks_ps_lain_pt_sendiri += instructor_even.credit

            for instructor_odd in instructors_odd:
                if instructor_odd.course_id.program_id.id == report.prodi.id:
                    sks_ps_sendiri += instructor_odd.credit
                else:
                    sks_ps_lain_pt_sendiri += instructor_odd.credit

            new_record_3a_433 = {
                'nama_dosen': dosen.name_related,
                'sks_ps_sendiri': sks_ps_sendiri,
                'sks_ps_lain_pt_sendiri': sks_ps_lain_pt_sendiri,
                'sks_pt_lain': 0, # TODO: based on itb.hr_work
                'sks_penelitian': sks_penelitian,
                'sks_pengmas': sks_pengmas,
                'sks_mgmt_pt_sendiri': 0, # TODO: based on itb.hr_assignment -> hr_job
                'sks_mgmt_pt_lain': 0, # TODO: based on itb.hr_work
                'sks_total': sks_ps_sendiri + sks_ps_lain_pt_sendiri + sks_penelitian + sks_pengmas,
            }

            report.write({'record_3a_433': [(0, 0, new_record_3a_433)]})
