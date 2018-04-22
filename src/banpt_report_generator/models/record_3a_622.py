# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_622(models.Model):
    _name = 'banpt_report_generator.record_3a_622'
    _rec_name = 'tahun'
    _title = '3A-6.2.2 Dana Untuk Kegiatan Penelitian'

    tahun = fields.Integer(string='Tahun', required=True)
    judul_penelitian = fields.Text(string='Judul Penelitian')
    sumber_jenis_dana = fields.Text(string='Sumber dan Jenis Dana')
    jumlah_dana = fields.Float(string='Jumlah Dana (dalam juta rupiah)')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear Record_3A_622 table
        report.record_3a_622.unlink()

        # Add funding for research table according to lecturer
        lecturers = reports.env['hr.employee'].search([
            ['is_faculty', '=', True],
            ['prodi', '=', report.prodi.id]
        ])

        for lecturer in lecturers:
            projects_team = reports.env['itb.hr_project_team'].search([
                ['employee_id', '=', lecturer.id]
            ])

            for project_team in projects_team:
                project = reports.env['itb.hr_project'].search([
                    ['id', '=', project_team.project_id.id]
                ])

                if ((project.tahun >= report.year - 3) and ((project.tahun <= report.year)) and ('penelitian' in project.tipe)):
                    new_record_3a_622 = {
                        'tahun': project.tahun,
                        'judul_penelitian': project.name,
                        'sumber_jenis_dana': project.mitra, # TODO: ganti dengan SISPRAN NOTE + Reference
                        'jumlah_dana': project.nilai / 1000000,
                    }

                    report.write({'record_3a_622': [(0, 0, new_record_3a_622)]})
