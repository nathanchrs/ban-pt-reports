# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Record_3A_331(models.Model):
    _name = 'banpt_report_generator.record_3a_331'
    _rec_name = 'jenis_kemampuan'
    _title = '3A-3.3.1 Evaluasi Kinerja Lulusan'

    jenis_kemampuan = fields.Text(string='Jenis Kemampuan')
    tanggapan_sangat_baik = fields.Float(string='Tanggapan Sangat Baik')
    tanggapan_baik = fields.Float(string='Tanggapan Baik')
    tanggapan_cukup = fields.Float(string='Tanggapan Cukup')
    tanggapan_kurang = fields.Float(string='Tanggapan Kurang')
    rencana_tindak_lanjut = fields.Text(string='Rencana Tindak Lanjut oleh Prodi')

    # The report this record belongs to
    report = fields.Many2one(comodel_name='banpt_report_generator.report')
    report_refresh_date = fields.Datetime(related='report.refresh_date')

def refresh(reports):
     for report in reports:
        report.record_3a_331.unlink()

        new_3a_331 = {
            'jenis_kemampuan': 'Integritas (etika dan moral)',
            'tanggapan_sangat_baik': 90.00, #TODO
            'tanggapan_baik': 10.00, #TODO
            'tanggapan_cukup': 0.00, #TODO
            'tanggapan_kurang': 0.00, #TODO
            'rencana_tindak_lanjut': 'Peningkatan pembinaan pada program wali akademik dan program kemahasiswaan',
        }

        report.write({'record_3a_3331': [(0, 0, new_3a_331)]})

        new_3a_331 = {
            'jenis_kemampuan': 'Keahlian berdasarkan bidang ilmu (profesionalisme)',
            'tanggapan_sangat_baik': 45.50, #TODO
            'tanggapan_baik': 36.40, #TODO
            'tanggapan_cukup': 18.20, #TODO
            'tanggapan_kurang': 0.00, #TODO
            'rencana_tindak_lanjut': '> Kurikulum dan silabus dikaji setiap tahun untk menjaga kompetensi sesuai tuntutan perkembangan industri. > Mengadakan kunjungan industri ke perusahaan telekomunikasi untk mendapatkan perkembangan terkini',
        }

        report.write({'record_3a_3331': [(0, 0, new_3a_331)]})

        new_3a_331 = {
            'jenis_kemampuan': 'Bahasa Inggris',
            'tanggapan_sangat_baik': 90.00, #TODO
            'tanggapan_baik': 0.00, #TODO
            'tanggapan_cukup': 10.00, #TODO
            'tanggapan_kurang': 0.00, #TODO
            'rencana_tindak_lanjut': 'Mempererat kerjasama dengan UPT Bahasa ITB untuk pelatihan TOEFL.',
        }

        report.write({'record_3a_3331': [(0, 0, new_3a_331)]})

        new_3a_331 = {
            'jenis_kemampuan': 'Penggunaan Teknologi Informasi',
            'tanggapan_sangat_baik': 90.00, #TODO
            'tanggapan_baik': 10.00, #TODO
            'tanggapan_cukup': 0.00, #TODO
            'tanggapan_kurang': 0.00, #TODO
            'rencana_tindak_lanjut': 'Memfasilitasi pelatihan dan bimbingan di bidang teknologi informasi terkini.',
        }

        report.write({'record_3a_3331': [(0, 0, new_3a_331)]})

        new_3a_331 = {
            'jenis_kemampuan': 'Komunikasi',
            'tanggapan_sangat_baik': 90.00, #TODO
            'tanggapan_baik': 10.00, #TODO
            'tanggapan_cukup': 0.00, #TODO
            'tanggapan_kurang': 0.00, #TODO
            'rencana_tindak_lanjut': 'Peningkatan sosialisasi program "soft skill bagi mahasiswa" ke para dosen pengajar melalui rapat Prodi.',
        }

        report.write({'record_3a_3331': [(0, 0, new_3a_331)]})

        new_3a_331 = {
            'jenis_kemampuan': 'Kerjasama Tim',
            'tanggapan_sangat_baik': 90.00, #TODO
            'tanggapan_baik': 10.00, #TODO
            'tanggapan_cukup': 0.00, #TODO
            'tanggapan_kurang': 0.00, #TODO
            'rencana_tindak_lanjut': 'Peningkatan tugas kuliah dan praktikum secara berkelompok serta pembentukan kepanitiaan',
        }

        report.write({'record_3a_3331': [(0, 0, new_3a_331)]})

        new_3a_331 = {
            'jenis_kemampuan': 'Pengembangan Diri',
            'tanggapan_sangat_baik': 41.70, #TODO
            'tanggapan_baik': 41.70, #TODO
            'tanggapan_cukup': 16.70, #TODO
            'tanggapan_kurang': 0.00, #TODO
            'rencana_tindak_lanjut': '> Memperbanyak seminar-seminar dari alumni yang merupakan pakar industri di bidangnya. > Mendorong mahasiswa untuk mengikuti berbagai kompetisi nasional dan internasional dengan memfasilitasi penggalangan bantuan dana dari alumni. > Memfasilitasi pelatihan dan workshop di bidang teknikal dan non-teknikal bagi mahasiswa',
        }

        report.write({'record_3a_3331': [(0, 0, new_3a_331)]})