# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))

    rec_3a_631 = context.env['banpt_report_generator.record_3a_631'].create(dict(
        ruang_kerja_dosen='test_1',
        jumlah_ruang=0,
        jumlah_luas=0
    ))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1 - IF',
        year=2015,
        refresh_date='2015-06-22 10:00:00',
        prodi=prodi_if.id
    ))

    return report_1, rec_3a_631

class TestRecord_3A_631(common.TransactionCase):
    def test_refresh(self):
        report_1, rec_3a_631 = seed(self)

        report_1.refresh()

        project_1_test = rec_3a_631.search([['ruang_kerja_dosen', '=', 'test_1']])
        self.assertEqual(project_1_test.ruang_kerja_dosen, 'test_1')
        self.assertEqual(project_1_test.jumlah_ruang, 0)
        self.assertEqual(project_1_test.jumlah_luas, 0)

        project_2_test = report_1.record_3a_631.search([['ruang_kerja_dosen', '=', 'Satu ruang untuk lebih dari 4 dosen']])
        self.assertEqual(project_2_test.ruang_kerja_dosen, 'Satu ruang untuk lebih dari 4 dosen')
        self.assertEqual(project_2_test.jumlah_ruang, 0)
        self.assertEqual(project_2_test.jumlah_luas, 0)

        project_3_test = report_1.record_3a_631.search([['ruang_kerja_dosen', '=', 'Satu ruang untuk 3-4 dosen']])
        self.assertEqual(project_3_test.ruang_kerja_dosen, 'Satu ruang untuk 3-4 dosen')
        self.assertEqual(project_3_test.jumlah_ruang, 3)
        self.assertEqual(project_3_test.jumlah_luas, 174)

        project_4_test = report_1.record_3a_631.search([['ruang_kerja_dosen', '=', 'Satu ruang untuk 2 dosen']])
        self.assertEqual(project_4_test.ruang_kerja_dosen, 'Satu ruang untuk 2 dosen')
        self.assertEqual(project_4_test.jumlah_ruang, 1)
        self.assertEqual(project_4_test.jumlah_luas, 60)

        project_5_test = report_1.record_3a_631.search([['ruang_kerja_dosen', '=', 'Satu ruang untuk 1 dosen (bukan pejabat struktural)']])
        self.assertEqual(project_5_test.ruang_kerja_dosen, 'Satu ruang untuk 1 dosen (bukan pejabat struktural)')
        self.assertEqual(project_5_test.jumlah_ruang, 2)
        self.assertEqual(project_5_test.jumlah_luas, 48)
