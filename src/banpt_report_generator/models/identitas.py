# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_Identitas(models.Model):
    _name = 'banpt_report_generator.identitas'
    _rec_name = 'nama_prodi'
    _title = 'Identitas Prodi'

    nama_prodi = fields.Char(string='Nama prodi', required=True)
    departemen = fields.Char(string='Departemen')
    fakultas = fields.Char(string='Fakultas')
    perguruan_tinggi = fields.Char(string='Perguruan tinggi', required=True)

    nomor_sk_pendirian = fields.Char(string='Nomor SK pendirian')
    tanggal_sk_pendirian = fields.Date(string='Tanggal SK pendirian')
    pejabat_sk_pendirian = fields.Char(string='Pejabat SK pendirian')
    tanggal_penyelenggaraan = fields.Date(string='Tanggal penyelenggaraan')
    nomor_sk_izin_operasional = fields.Char(string='Nomor SK izin operasional')
    tanggal_sk_izin_operasional = fields.Date(string='Tanggal SK izin operasional')
    peringkat_akreditasi_ban_pt = fields.Char(string='Peringkat akreditasi BAN-PT')
    nilai_akreditasi_ban_pt = fields.Integer(string='Nilai akreditasi BAN-PT')
    nomor_sk_akreditasi_ban_pt = fields.Char(string='Nomor SK akreditasi BAN-PT')

    alamat = fields.Text(string='Alamat')
    telepon = fields.Char(string='Telepon')
    faks = fields.Char(string='Faks')
    homepage = fields.Char(string='Homepage')
    email = fields.Char(string='Email')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
    for report in reports:
        # Clear identitas table
        report.identitas.unlink()

        # TODO: add table recording akreditasi ban-pt table results for each prodi
        #latest_banpt_accreditation = reports.env['itb_academic_banpt_accreditation'].search([['prodi', '=', report.prodi.id]], order='date desc', limit=1)

        # Add identitas
        new_identitas = {
            'nama_prodi': report.prodi.name,
            'departemen': '',
            'fakultas': 'Sekolah Teknik Elektro dan Informatika',
            'perguruan_tinggi': 'Institut Teknologi Bandung',

            # TODO: add fields to itb_academic_program:

            #'nomor_sk_pendirian': report.prodi.nomor_sk_pendirian,
            #'tanggal_sk_pendirian': report.prodi.tanggal_sk_pendirian,
            #'pejabat_sk_pendirian': report.prodi.pejabat_sk_pendirian,

            #'tanggal_penyelenggaraan': report.prodi.tanggal_penyelenggaraan,
            #'nomor_sk_izin_operasional': report.prodi.nomor_sk_izin_operasional,
            #'tanggal_sk_izin_operasional': report.prodi.tanggal_sk_izin_operasional,

            # TODO: add table recording akreditasi ban-pt table results for each prodi, then use its fields:

            # 'peringkat_akreditasi_ban_pt': latest_banpt_accreditation[0].peringkat if latest_banpt_accreditation else '',
            # 'nilai_akreditasi_ban_pt': latest_banpt_accreditation[0].peringkat if latest_banpt_accreditation else 0,
            # 'nomor_sk_akreditasi_ban_pt': latest_banpt_accreditation[0].peringkat if latest_banpt_accreditation else '',

            # TODO: add fields to itb_academic_program

            #'alamat': '',
            #'telepon': '',
            #'faks': '',
            #'homepage': '',
            #'email': ''
        }
        report.write({'identitas': [(0, 0, new_identitas)]})
