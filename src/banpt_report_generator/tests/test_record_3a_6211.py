# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))

    rec_3a_6211 = context.env['banpt_report_generator.record_3a_6211'].create(dict(
        sumber_dana='test_1',
        jenis_dana='test_1',
        jumlah_dana_ts_2=0,
        jumlah_dana_ts_1=0,
        jumlah_dana_ts=0
    ))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1 - IF',
        year=2015,
        refresh_date='2015-06-22 10:00:00',
        prodi=prodi_if.id
    ))

    return report_1, rec_3a_6211

class TestRecord_3A_6211(common.TransactionCase):
    def test_refresh(self):
        report_1, rec_3a_6211 = seed(self)

        report_1.refresh()

        project_1_test = rec_3a_6211.search([['sumber_dana', '=', 'test_1'], ['jenis_dana', '=', 'test_1']])
        self.assertEqual(project_1_test.sumber_dana, 'test_1')
        self.assertEqual(project_1_test.jenis_dana, 'test_1')
        self.assertEqual(project_1_test.jumlah_dana_ts_2, 0)
        self.assertEqual(project_1_test.jumlah_dana_ts_1, 0)
        self.assertEqual(project_1_test.jumlah_dana_ts, 0)

        project_2_test = report_1.record_3a_6211.search([['sumber_dana', '=', 'PT Sendiri'], ['jenis_dana', '=', 'DM']])
        self.assertEqual(project_2_test.sumber_dana, 'PT Sendiri')
        self.assertEqual(project_2_test.jenis_dana, 'DM')
        self.assertEqual(project_2_test.jumlah_dana_ts_2, 1437)
        self.assertEqual(project_2_test.jumlah_dana_ts_1, 1084)
        self.assertEqual(project_2_test.jumlah_dana_ts, 1021)

        project_3_test = report_1.record_3a_6211.search([['sumber_dana', '=', 'Pemerintah Pusat'], ['jenis_dana', '=', 'DIPA']])
        self.assertEqual(project_3_test.sumber_dana, 'Pemerintah Pusat')
        self.assertEqual(project_3_test.jenis_dana, 'DIPA')
        self.assertEqual(project_3_test.jumlah_dana_ts_2, 2698)
        self.assertEqual(project_3_test.jumlah_dana_ts_1, 1125)
        self.assertEqual(project_3_test.jumlah_dana_ts, 1056)

        project_4_test = report_1.record_3a_6211.search([['sumber_dana', '=', 'Diknas'], ['jenis_dana', '=', 'DIPA IL']])
        self.assertEqual(project_4_test.sumber_dana, 'Diknas')
        self.assertEqual(project_4_test.jenis_dana, 'DIPA IL')
        self.assertEqual(project_4_test.jumlah_dana_ts_2, 1222)
        self.assertEqual(project_4_test.jumlah_dana_ts_1, 742)
        self.assertEqual(project_4_test.jumlah_dana_ts, 350)

        project_5_test = report_1.record_3a_6211.search([['sumber_dana', '=', 'Sumber Lain'], ['jenis_dana', '=', 'DIPA']])
        self.assertEqual(project_5_test.sumber_dana, 'Sumber Lain')
        self.assertEqual(project_5_test.jenis_dana, 'DIPA')
        self.assertEqual(project_5_test.jumlah_dana_ts_2, 0)
        self.assertEqual(project_5_test.jumlah_dana_ts_1, 0)
        self.assertEqual(project_5_test.jumlah_dana_ts, 0)

        project_6_test = report_1.record_3a_6211.search([['sumber_dana', '=', 'Sumber Lain'], ['jenis_dana', '=', 'DM']])
        self.assertEqual(project_6_test.sumber_dana, 'Sumber Lain')
        self.assertEqual(project_6_test.jenis_dana, 'DM')
        self.assertEqual(project_6_test.jumlah_dana_ts_2, 139)
        self.assertEqual(project_6_test.jumlah_dana_ts_1, 32)
        self.assertEqual(project_6_test.jumlah_dana_ts, 1146)
