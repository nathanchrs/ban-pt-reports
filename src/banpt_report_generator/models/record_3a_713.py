# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import models, fields, api

class Record_3A_713(models.Model):
    _name = 'banpt_report_generator.record_3a_713'
    _rec_name = 'judul'
    _title = '3A-7.1.3 Judul Artikel Ilmiah/Karya Ilmiah/Karya Seni/Buku'

    judul = fields.Text(string='Judul', required=True)
    nama_dosen = fields.Text(string='Nama-nama Dosen')
    tempat_publikasi = fields.Text(string='Dihasilkan/Dipublikasikan Pada')
    tahun_publikasi = fields.Text(string='Tahun Penyajian/Publikasi')
    dosen_lokal = fields.Selection([('checklist', 'V')], string='Banyaknya Dosen Lokal')
    dosen_nasional = fields.Selection([('checklist', 'V')], string='Banyaknya Dosen Nasional')
    dosen_internasional = fields.Selection([('checklist', 'V')], string='Banyaknya Dosen Internasional')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear Record_3A_713 table
        report.record_3a_713.unlink()

        # Add judul artikel ilmiah or others table
        instructors = reports.env['hr.employee'].search([
            ['is_faculty', '=', True],
            ['prodi', '=', report.prodi.id]
        ])

        for instructor in instructors:
            publication_authors = reports.env['itb.hr_publication_author'].search([
                ['employee_id', '=', instructor.id]
            ])

            for publication_author in publication_authors:
                publications = reports.env['itb.hr_publication'].search([
                    ['id', '=', publication_author.publication_id.id]
                ])

                for publication in publications:
                    tahun = datetime.strptime(publication.day, "%Y-%m-%d")

                    if ((int(tahun.year) >= report.year - 3) and ((int(tahun.year) <= report.year))):
                        pub_type = publication.media_id.name
                        new_record_3a_713 = {
                            'judul': publication.name,
                            'nama_dosen': publication.authors,
                            'tempat_publikasi': publication.publisher,
                            'tahun_publikasi': tahun.year,
                            'dosen_lokal': 'checklist' if 'Local' in pub_type else '',
                            'dosen_nasional': 'checklist' if 'National' in pub_type else '',
                            'dosen_internasional': 'checklist' if 'International' in pub_type else '',
                        }

                        report.write({'record_3a_713': [(0, 0, new_record_3a_713)]})
