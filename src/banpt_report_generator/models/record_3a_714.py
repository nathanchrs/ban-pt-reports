# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_714(models.Model):
    _name = 'banpt_report_generator.record_3a_714'
    _rec_name = 'karya_haki'
    _title = '3A-7.1.4 Hak Atas Kekayaan Intelektual'

    karya_haki = fields.Text(string='Karya', required=True)

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        report.record_3a_714.unlink()

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

                if ((project.tahun >= report.year - 2) and ((project.tahun <= report.year)) and ('other' in project.tipe) or ('paten' in project.tipe)):
                    new_record_3a_714 = {
                        'karya_haki': project.name,
                    }

                    report.write({'record_3a_714': [(0, 0, new_record_3a_714)]})
