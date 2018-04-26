# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))

    rec_3a_331 = context.env['banpt_report_generator.record_3a_331'].create(dict(
        jenis_kemampuan='test_1',
        tanggapan_sangat_baik=90.00,
        tanggapan_baik=10.00,
        tanggapan_cukup=0.00,
        tanggapan_kurang=0.00,
        rencana_tindak_lanjut='test_1'
    ))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1 - IF',
        year=2015,
        refresh_date='2015-06-22 10:00:00',
        prodi=prodi_if.id
    ))

    return report_1, rec_3a_331

class TestRecord_3A_331(common.TransactionCase):
    def test_refresh(self):
        report_1, rec_3a_331 = seed(self)

        report_1.refresh()

        project_1_test = rec_3a_331.search([['jenis_kemampuan', '=', 'test_1']])
        self.assertEqual(project_1_test.jenis_kemampuan, 'test_1')
        self.assertEqual(project_1_test.tanggapan_sangat_baik, 90.00)
        self.assertEqual(project_1_test.tanggapan_baik, 10.00)
        self.assertEqual(project_1_test.tanggapan_cukup, 0.00)
        self.assertEqual(project_1_test.tanggapan_kurang, 0.00)
        self.assertEqual(project_1_test.rencana_tindak_lanjut, 'test_1')

        project_2_test = report_1.record_3a_331.search([['jenis_kemampuan', '=', 'Integritas (etika dan moral)']])
        self.assertEqual(project_2_test.jenis_kemampuan, 'Integritas (etika dan moral)')
        self.assertEqual(project_2_test.tanggapan_sangat_baik, 90.00)
        self.assertEqual(project_2_test.tanggapan_baik, 10.00)
        self.assertEqual(project_2_test.tanggapan_cukup, 0.00)
        self.assertEqual(project_2_test.tanggapan_kurang, 0.00)

        project_3_test = report_1.record_3a_331.search([['jenis_kemampuan', '=', 'Keahlian berdasarkan bidang ilmu (profesionalisme)']])
        self.assertEqual(project_3_test.jenis_kemampuan, 'Keahlian berdasarkan bidang ilmu (profesionalisme)')
        self.assertEqual(project_3_test.tanggapan_sangat_baik, 45.50)
        self.assertEqual(project_3_test.tanggapan_baik, 36.40)
        self.assertEqual(project_3_test.tanggapan_cukup, 18.20)
        self.assertEqual(project_3_test.tanggapan_kurang, 0.00)

        project_4_test = report_1.record_3a_331.search([['jenis_kemampuan', '=', 'Bahasa Inggris']])
        self.assertEqual(project_4_test.jenis_kemampuan, 'Bahasa Inggris')
        self.assertEqual(project_4_test.tanggapan_sangat_baik, 90.00)
        self.assertEqual(project_4_test.tanggapan_baik, 0.00)
        self.assertEqual(project_4_test.tanggapan_cukup, 10.00)
        self.assertEqual(project_4_test.tanggapan_kurang, 0.00)

        project_5_test = report_1.record_3a_331.search([['jenis_kemampuan', '=', 'Penggunaan Teknologi Informasi']])
        self.assertEqual(project_5_test.jenis_kemampuan, 'Penggunaan Teknologi Informasi')
        self.assertEqual(project_5_test.tanggapan_sangat_baik, 90.00)
        self.assertEqual(project_5_test.tanggapan_baik, 10.00)
        self.assertEqual(project_5_test.tanggapan_cukup, 0.00)
        self.assertEqual(project_5_test.tanggapan_kurang, 0.00)

        project_6_test = report_1.record_3a_331.search([['jenis_kemampuan', '=', 'Komunikasi']])
        self.assertEqual(project_6_test.jenis_kemampuan, 'Komunikasi')
        self.assertEqual(project_6_test.tanggapan_sangat_baik, 90.00)
        self.assertEqual(project_6_test.tanggapan_baik, 10.00)
        self.assertEqual(project_6_test.tanggapan_cukup, 0.00)
        self.assertEqual(project_6_test.tanggapan_kurang, 0.00)

        project_7_test = report_1.record_3a_331.search([['jenis_kemampuan', '=', 'Kerjasama Tim']])
        self.assertEqual(project_7_test.jenis_kemampuan, 'Kerjasama Tim')
        self.assertEqual(project_7_test.tanggapan_sangat_baik, 90.00)
        self.assertEqual(project_7_test.tanggapan_baik, 10.00)
        self.assertEqual(project_7_test.tanggapan_cukup, 0.00)
        self.assertEqual(project_7_test.tanggapan_kurang, 0.00)

        project_8_test = report_1.record_3a_331.search([['jenis_kemampuan', '=', 'Pengembangan Diri']])
        self.assertEqual(project_8_test.jenis_kemampuan, 'Pengembangan Diri')
        self.assertEqual(project_8_test.tanggapan_sangat_baik, 41.70)
        self.assertEqual(project_8_test.tanggapan_baik, 41.70)
        self.assertEqual(project_8_test.tanggapan_cukup, 16.70)
        self.assertEqual(project_8_test.tanggapan_kurang, 0.00)
