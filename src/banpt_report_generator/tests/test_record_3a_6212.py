# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))

    rec_3a_6212 = context.env['banpt_report_generator.record_3a_6212'].create(dict(
        jenis_penggunaan='test_1',
        penggunaan_ts_2=0,
        penggunaan_ts_1=0,
        penggunaan_ts=0
    ))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1 - IF',
        year=2015,
        refresh_date='2015-06-22 10:00:00',
        prodi=prodi_if.id
    ))

    return report_1, rec_3a_6212

class TestRecord_3A_6212(common.TransactionCase):
    def test_refresh(self):
        report_1, rec_3a_6212 = seed(self)

        report_1.refresh()

        project_1_test = rec_3a_6212.search([['jenis_penggunaan', '=', 'test_1']])
        self.assertEqual(project_1_test.penggunaan_ts_2, 0)
        self.assertEqual(project_1_test.penggunaan_ts_1, 0)
        self.assertEqual(project_1_test.penggunaan_ts, 0)

        project_2_test = report_1.record_3a_6212.search([['jenis_penggunaan', '=', 'Pendidikan']])
        self.assertEqual(project_2_test.penggunaan_ts_2, 451)
        self.assertEqual(project_2_test.penggunaan_ts_1, 573)
        self.assertEqual(project_2_test.penggunaan_ts, 424)

        project_3_test = report_1.record_3a_6212.search([['jenis_penggunaan', '=', 'Penelitian']])
        self.assertEqual(project_3_test.penggunaan_ts_2, 50)
        self.assertEqual(project_3_test.penggunaan_ts_1, 66)
        self.assertEqual(project_3_test.penggunaan_ts, 90)

        project_4_test = report_1.record_3a_6212.search([['jenis_penggunaan', '=', 'Pengabdian Kepada Masyarakat']])
        self.assertEqual(project_4_test.penggunaan_ts_2, 0)
        self.assertEqual(project_4_test.penggunaan_ts_1, 0)
        self.assertEqual(project_4_test.penggunaan_ts, 0)

        project_5_test = report_1.record_3a_6212.search([['jenis_penggunaan', '=', 'Investasi Prasarana']])
        self.assertEqual(project_5_test.penggunaan_ts_2, 186)
        self.assertEqual(project_5_test.penggunaan_ts_1, 80)
        self.assertEqual(project_5_test.penggunaan_ts, 64)

        project_6_test = report_1.record_3a_6212.search([['jenis_penggunaan', '=', 'Investasi Sarana']])
        self.assertEqual(project_6_test.penggunaan_ts_2, 0)
        self.assertEqual(project_6_test.penggunaan_ts_1, 0)
        self.assertEqual(project_6_test.penggunaan_ts, 0)

        project_7_test = report_1.record_3a_6212.search([['jenis_penggunaan', '=', 'Investasi SDM']])
        self.assertEqual(project_7_test.penggunaan_ts_2, 0)
        self.assertEqual(project_7_test.penggunaan_ts_1, 0)
        self.assertEqual(project_7_test.penggunaan_ts, 0)

        project_8_test = report_1.record_3a_6212.search([['jenis_penggunaan', '=', 'Lain-lain']])
        self.assertEqual(project_8_test.penggunaan_ts_2, 20)
        self.assertEqual(project_8_test.penggunaan_ts_1, 27)
        self.assertEqual(project_8_test.penggunaan_ts, 75)
