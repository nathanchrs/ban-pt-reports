# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_5121(models.Model):
    _name = 'banpt_report_generator.record_3a_5121'
    _rec_name = 'jenis_mata_kuliah'
    _title = '3A-5.1.2.1 Jumlah SKS Mata Kuliah Wajib dan Pilihan'

    jenis_mata_kuliah = fields.Text(string='Jenis Mata Kuliah', required=True)
    sks = fields.Integer(string='SKS')
    keterangan = fields.Text(string='Keterangan')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear record_3a_5121 table
        report.record_3a_5121.unlink()

        wajib = 0
        curriculums = reports.env['itb.academic_curriculum'].search([['program_id', '=', report.prodi.id], ['year', '<', report.year]], order='year desc', limit=1)
        for curriculum_id in curriculums:
            curriculum_lines = reports.env['itb.academic_curriculum_line'].search([['curriculum_id', '=', curriculum_id.id], ['category', '=', 'wajib']], order='semester')
            for curriculum_line in curriculum_lines:
                catalog = reports.env['itb.academic_catalog'].search([['id', '=', curriculum_line.catalog_id.id]])
                wajib += catalog[0].credit

        pilihan = 0
        curriculums = reports.env['itb.academic_curriculum'].search([['program_id', '=', report.prodi.id], ['year', '<', report.year]], order='year desc', limit=1)
        for curriculum_id in curriculums:
            curriculum_lines = reports.env['itb.academic_curriculum_line'].search([['curriculum_id', '=', curriculum_id.id], ['category', '=', 'opsional']], order='semester')
            for curriculum_line in curriculum_lines:
                catalog = reports.env['itb.academic_catalog'].search([['id', '=', curriculum_line.catalog_id.id]])
                pilihan += catalog[0].credit

        curriculums = reports.env['itb.academic_curriculum'].search([['program_id', '=', report.prodi.id], ['year', '<', report.year]], order='year desc', limit=1)
        for curriculum_id in curriculums:
            curriculum_lines = reports.env['itb.academic_curriculum_line'].search([['curriculum_id', '=', curriculum_id.id], ['category', '=', 'opsional-external']], order='semester')
            for curriculum_line in curriculum_lines:
                catalog = reports.env['itb.academic_catalog'].search([['id', '=', curriculum_line.catalog_id.id]])
                pilihan += catalog[0].credit

        curriculums = reports.env['itb.academic_curriculum'].search([['program_id', '=', report.prodi.id], ['year', '<', report.year]], order='year desc', limit=1)
        for curriculum_id in curriculums:
            curriculum_lines = reports.env['itb.academic_curriculum_line'].search([['curriculum_id', '=', curriculum_id.id], ['category', '=', 'opsional-luar']], order='semester')
            for curriculum_line in curriculum_lines:
                catalog = reports.env['itb.academic_catalog'].search([['id', '=', curriculum_line.catalog_id.id]])
                pilihan += catalog[0].credit

        # Add record_3a_5121 according to program_id
        new_record_3a_5121 = {
            'jenis_mata_kuliah': 'Wajib',
            'sks': wajib,
            'keterangan': '',
        }
        report.write({'record_3a_5121': [(0, 0, new_record_3a_5121)]})

        new_record_3a_5121 = {
            'jenis_mata_kuliah': 'Pilihan',
            'sks': pilihan,
            'keterangan': '',
        }
        report.write({'record_3a_5121': [(0, 0, new_record_3a_5121)]})
