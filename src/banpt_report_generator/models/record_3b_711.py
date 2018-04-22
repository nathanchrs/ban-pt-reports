# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3B_711(models.Model):
    _name = 'banpt_report_generator.record_3b_711'
    _rec_name = 'program_studi'
    _title = '3B-7.1.1 Penelitian'

    program_studi = fields.Text(string='Nama Program Studi', required=True)
    jumlah_judul_penelitian_ts_2 = fields.Integer(string='Jumlah Judul Penelitian TS-2')
    jumlah_judul_penelitian_ts_1 = fields.Integer(string='Jumlah Judul Penelitian TS-1')
    jumlah_judul_penelitian_ts = fields.Integer(string='Jumlah Judul Penelitian TS')
    total_dana_penelitian_ts_2 = fields.Integer(string='Total Dana Penelitian TS-2 (juta rupiah)')
    total_dana_penelitian_ts_1 = fields.Integer(string='Total Dana Penelitian TS-1 (juta rupiah)')
    total_dana_penelitian_ts = fields.Integer(string='Total Dana Penelitian TS (juta rupiah)')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear Record_3B_711 table
        report.record_3b_711.unlink()

        # Add research data
        if_judul_ts_2 = count_project_title(report, 11, report.year - 2)
        if_judul_ts_1 = count_project_title(report, 11, report.year - 1)
        if_judul_ts = count_project_title(report, 11, report.year)

        el_judul_ts_2 = count_project_title(report, 12, report.year - 2)
        el_judul_ts_1 = count_project_title(report, 12, report.year - 1)
        el_judul_ts = count_project_title(report, 12, report.year)

        ep_judul_ts_2 = count_project_title(report, 13, report.year - 2)
        ep_judul_ts_1 = count_project_title(report, 13, report.year - 1)
        ep_judul_ts = count_project_title(report, 13, report.year)

        et_judul_ts_2 = count_project_title(report, 14, report.year - 2)
        et_judul_ts_1 = count_project_title(report, 14, report.year - 1)
        et_judul_ts = count_project_title(report, 14, report.year)

        sti_judul_ts_2 = count_project_title(report, 15, report.year - 2)
        sti_judul_ts_1 = count_project_title(report, 15, report.year - 1)
        sti_judul_ts = count_project_title(report, 15, report.year)

        eb_judul_ts_2 = count_project_title(report, 16, report.year - 2)
        eb_judul_ts_1 = count_project_title(report, 16, report.year - 1)
        eb_judul_ts = count_project_title(report, 16, report.year)

        if_dana_ts_2 = count_project_cost(report, 11, report.year - 2)
        if_dana_ts_1 = count_project_cost(report, 11, report.year - 1)
        if_dana_ts = count_project_cost(report, 11, report.year)

        el_dana_ts_2 = count_project_cost(report, 12, report.year - 2)
        el_dana_ts_1 = count_project_cost(report, 12, report.year - 1)
        el_dana_ts = count_project_cost(report, 12, report.year)

        ep_dana_ts_2 = count_project_cost(report, 13, report.year - 2)
        ep_dana_ts_1 = count_project_cost(report, 13, report.year - 1)
        ep_dana_ts = count_project_cost(report, 13, report.year)

        et_dana_ts_2 = count_project_cost(report, 14, report.year - 2)
        et_dana_ts_1 = count_project_cost(report, 14, report.year - 1)
        et_dana_ts = count_project_cost(report, 14, report.year)

        sti_dana_ts_2 = count_project_cost(report, 15, report.year - 2)
        sti_dana_ts_1 = count_project_cost(report, 15, report.year - 1)
        sti_dana_ts = count_project_cost(report, 15, report.year)

        eb_dana_ts_2 = count_project_cost(report, 16, report.year - 2)
        eb_dana_ts_1 = count_project_cost(report, 16, report.year - 1)
        eb_dana_ts = count_project_cost(report, 16, report.year)

        if_record_3b_711 = {
            'program_studi': 'Teknik Informatika',
            'jumlah_judul_penelitian_ts_2': if_judul_ts_2,
            'jumlah_judul_penelitian_ts_1': if_judul_ts_1,
            'jumlah_judul_penelitian_ts': if_judul_ts,
            'total_dana_penelitian_ts_2': if_dana_ts_2,
            'total_dana_penelitian_ts_1': if_dana_ts_1,
            'total_dana_penelitian_ts': if_dana_ts,
        }

        report.write({'record_3b_711': [(0, 0, if_record_3b_711)]})

        el_record_3b_711 = {
            'program_studi': 'Teknik Elektro',
            'jumlah_judul_penelitian_ts_2': el_judul_ts_2,
            'jumlah_judul_penelitian_ts_1': el_judul_ts_1,
            'jumlah_judul_penelitian_ts': el_judul_ts,
            'total_dana_penelitian_ts_2': el_dana_ts_2,
            'total_dana_penelitian_ts_1': el_dana_ts_1,
            'total_dana_penelitian_ts': el_dana_ts,
        }

        report.write({'record_3b_711': [(0, 0, el_record_3b_711)]})

        ep_record_3b_711 = {
            'program_studi': 'Teknik Tenaga Listrik',
            'jumlah_judul_penelitian_ts_2': ep_judul_ts_2,
            'jumlah_judul_penelitian_ts_1': ep_judul_ts_1,
            'jumlah_judul_penelitian_ts': ep_judul_ts,
            'total_dana_penelitian_ts_2': ep_dana_ts_2,
            'total_dana_penelitian_ts_1': ep_dana_ts_1,
            'total_dana_penelitian_ts': ep_dana_ts,
        }

        report.write({'record_3b_711': [(0, 0, ep_record_3b_711)]})

        et_record_3b_711 = {
            'program_studi': 'Teknik Telekomunikasi',
            'jumlah_judul_penelitian_ts_2': et_judul_ts_2,
            'jumlah_judul_penelitian_ts_1': et_judul_ts_1,
            'jumlah_judul_penelitian_ts': et_judul_ts,
            'total_dana_penelitian_ts_2': et_dana_ts_2,
            'total_dana_penelitian_ts_1': et_dana_ts_1,
            'total_dana_penelitian_ts': et_dana_ts,
        }

        report.write({'record_3b_711': [(0, 0, et_record_3b_711)]})

        sti_record_3b_711 = {
            'program_studi': 'Sistem & Teknologi Informasi',
            'jumlah_judul_penelitian_ts_2': sti_judul_ts_2,
            'jumlah_judul_penelitian_ts_1': sti_judul_ts_1,
            'jumlah_judul_penelitian_ts': sti_judul_ts,
            'total_dana_penelitian_ts_2': sti_dana_ts_2,
            'total_dana_penelitian_ts_1': sti_dana_ts_1,
            'total_dana_penelitian_ts': sti_dana_ts,
        }

        report.write({'record_3b_711': [(0, 0, sti_record_3b_711)]})

        eb_record_3b_711 = {
            'program_studi': 'Teknik Biomedis',
            'jumlah_judul_penelitian_ts_2': eb_judul_ts_2,
            'jumlah_judul_penelitian_ts_1': eb_judul_ts_1,
            'jumlah_judul_penelitian_ts': eb_judul_ts,
            'total_dana_penelitian_ts_2': eb_dana_ts_2,
            'total_dana_penelitian_ts_1': eb_dana_ts_1,
            'total_dana_penelitian_ts': eb_dana_ts,
        }

        report.write({'record_3b_711': [(0, 0, eb_record_3b_711)]})

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

            if((project.tahun == year) and ('penelitian' in project.tipe)):
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

            if((project.tahun == year) and ('penelitian' in project.tipe)):
                project_cost += project.nilai

    return project_cost / 1000000
