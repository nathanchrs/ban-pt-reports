# -*- coding: utf-8 -*-

from odoo import models, fields, api
from .. import utils

class Record_3A_453(models.Model):
    _name = 'banpt_report_generator.record_3a_453'
    _rec_name = 'nama_dosen'
    _title = '3A-4.5.3 Kegiatan Dosen Tetap'

    nama_dosen = fields.Char(string='Nama Dosen Tetap', required=True)
    jenis_kegiatan = fields.Char(string='Jenis Kegiatan')
    tempat = fields.Char(string='Tempat')
    tahun = fields.Char(string='Tahun')
    sebagai_penyaji = fields.Selection([('checklist', 'V')], string='Sebagai Penyaji')
    sebagai_peserta = fields.Selection([('checklist', 'V')], string='Sebagai Peserta')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        report.record_3a_453.unlink()

        lecturers = reports.env['hr.employee'].search([
            ['is_faculty', '=', True],
            ['prodi', '=', report.prodi.id]
        ])

        for lecturer in lecturers:
            publication_authors = reports.env['itb.hr_publication_author'].search([
                ['employee_id', '=', lecturer.id]
            ])

            for publication_author in publication_authors:
                publications = reports.env['itb.hr_publication'].search([
                    ['id', '=', publication_author.publication_id.id]
                ])

                for publication in publications:
                    year = utils.get_year(publication.day)

                    if ((year >= report.year - 3) and (year <= report.year)):
                        pub_type = publication.media_id.name

                        if 'Proceeding' in pub_type:
                            new_record_3a_453 = {
                                'nama_dosen': lecturer.name_related,
                                'jenis_kegiatan': publication.publisher,
                                'tempat': '', # TODO: find where to get seminar place, option parse publisher
                                'tahun': year,
                                'sebagai_penyaji': 'checklist',
                                'sebagai_peserta': '',
                            }

                            report.write({'record_3a_453': [(0, 0, new_record_3a_453)]})
