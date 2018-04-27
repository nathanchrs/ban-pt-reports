# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3B_721(models.Model):
    _name = 'banpt_report_generator.record_3b_721'
    _rec_name = 'program_studi'
    _title = '3B-7.2.1 Kegiatan Pelayanan/Pengabdian kepada Masyarakat'

    program_studi = fields.Text(string='Nama Program Studi', required=True)
    jumlah_judul_kegiatan_masyarakat_ts_2 = fields.Integer(string='Jumlah Judul Kegiatan Pelayanan / Pengabdian Kepada Masyarakat TS-2', required=True)
    jumlah_judul_kegiatan_masyarakat_ts_1 = fields.Integer(string='Jumlah Judul Kegiatan Pelayanan / Pengabdian Kepada Masyarakat TS-1', required=True)
    jumlah_judul_kegiatan_masyarakat_ts = fields.Integer(string='Jumlah Judul Kegiatan Pelayanan / Pengabdian Kepada Masyarakat TS', required=True)
    total_dana_kegiatan_masyarakat_ts_2 = fields.Integer(string='Total Dana Kegiatan Pelayanan / Pengabdian Kepada Masyarakat TS-2 (juta rupiah)')
    total_dana_kegiatan_masyarakat_ts_1 = fields.Integer(string='Total Dana Kegiatan Pelayanan / Pengabdian Kepada Masyarakat TS-1 (juta rupiah)')
    total_dana_kegiatan_masyarakat_ts = fields.Integer(string='Total Dana Kegiatan Pelayanan / Pengabdian Kepada Masyarakat TS (juta rupiah)')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear Record_3B_721 table
        report.record_3b_721.unlink()

        # Add research data
        programs = reports.env['itb.academic_program'].search([])
        for program in programs:
            judul_ts_2 = count_project_title(report, program.id, report.year - 2)
            judul_ts_1 = count_project_title(report, program.id, report.year - 1)
            judul_ts = count_project_title(report, program.id, report.year)

            dana_ts_2 = count_project_cost(report, program.id, report.year - 2)
            dana_ts_1 = count_project_cost(report, program.id, report.year - 1)
            dana_ts = count_project_cost(report, program.id, report.year)

            new_record_3b_721 = {
                'program_studi': program.name,
                'jumlah_judul_kegiatan_masyarakat_ts_2': judul_ts_2,
                'jumlah_judul_kegiatan_masyarakat_ts_1': judul_ts_1,
                'jumlah_judul_kegiatan_masyarakat_ts': judul_ts,
                'total_dana_kegiatan_masyarakat_ts_2': dana_ts_2,
                'total_dana_kegiatan_masyarakat_ts_1': dana_ts_1,
                'total_dana_kegiatan_masyarakat_ts': dana_ts,
            }
            report.write({'record_3b_721': [(0, 0, new_record_3b_721)]})

def count_project_title(report, prodi_id, year):
    count_project = 0
    lecturers = report.env['hr.employee'].search([
        ['is_faculty', '=', True],
        ['prodi', '=', prodi_id]
    ])

    for lecturer in lecturers:
        projects_team = report.env['itb.hr_project_team'].search([
            ['employee_id', '=', lecturer.id]
        ])

        for project_team in projects_team:
            project = report.env['itb.hr_project'].search([
                ['id', '=', project_team.project_id.id]
            ])

            if((project.tahun == year) and ('pengabdian' in project.tipe)):
                count_project += 1

    return count_project

def count_project_cost(report, prodi_id, year):
    project_cost = 0
    lecturers = report.env['hr.employee'].search([
        ['is_faculty', '=', True],
        ['prodi', '=', prodi_id]
    ])

    for lecturer in lecturers:
        projects_team = report.env['itb.hr_project_team'].search([
            ['employee_id', '=', lecturer.id]
        ])

        for project_team in projects_team:
            project = report.env['itb.hr_project'].search([
                ['id', '=', project_team.project_id.id]
            ])

            if((project.tahun == year) and ('pengabdian' in project.tipe)):
                project_cost += project.nilai

    return project_cost / 1000000
    