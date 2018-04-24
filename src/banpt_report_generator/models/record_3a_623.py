# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_623(models.Model):
    _name = 'banpt_report_generator.record_3a_623'
    _rec_name = 'tahun'
    _title = '3A-6.2.3 Dana Pelayanan/Pengabdian Kepada Masyarakat'

    tahun = fields.Char(string='Tahun', required=True)
    judul_kegiatan = fields.Text(string='Judul Kegiatan Pelayanan/Pengabdian kepada Masyarakat')
    sumber_jenis_dana = fields.Text(string='Sumber dan Jenis Dana')
    jumlah_dana = fields.Integer(string='Jumlah Dana (dalan juta rupiah)')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear Record_3A_623 table
        report.record_3a_623.unlink()

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

                if ((project.tahun >= report.year - 2) and ((project.tahun <= report.year)) and ('pengabdian' in project.tipe)):
                    new_record_3a_623 = {
                        'tahun': project.tahun,
                        'judul_kegiatan': project.name,
                        'sumber_jenis_dana': '%s - %s' % (project.deskripsi_sispran, project.reference),
                        'jumlah_dana': project.nilai / 1000000,
                    }

                    report.write({'record_3a_623': [(0, 0, new_record_3a_623)]})
