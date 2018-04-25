# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))

    rec_3a_711 = context.env['banpt_report_generator.record_3a_711'].create(dict(
        sumber_biaya='test_1',
        ts_2=1267,
        ts_1=1,
        ts=0
    ))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1 - IF',
        year=2015,
        refresh_date='2015-06-22 10:00:00',
        prodi=prodi_if.id
    ))

    return report_1, rec_3a_711

class TestRecord_3A_711(common.TransactionCase):
    def test_refresh(self):
        report_1, rec_3a_711 = seed(self)

        report_1.refresh()

        project_1_test = rec_3a_711.search([['sumber_biaya', '=', 'test_1']])
        self.assertEqual(project_1_test.sumber_biaya, 'test_1')
        self.assertEqual(project_1_test.ts_2, 1267)
        self.assertEqual(project_1_test.ts_1, 1)
        self.assertEqual(project_1_test.ts, 0)

        project_2_test = report_1.record_3a_711.search([['sumber_biaya', '=', 'Pembiayaan sendiri oleh peneliti']])
        self.assertEqual(project_2_test.sumber_biaya, 'Pembiayaan sendiri oleh peneliti')
        self.assertEqual(project_2_test.ts_2, 0)
        self.assertEqual(project_2_test.ts_1, 0)
        self.assertEqual(project_2_test.ts, 0)

        project_3_test = report_1.record_3a_711.search([['sumber_biaya', '=', 'PT yang bersangkutan']])
        self.assertEqual(project_3_test.sumber_biaya, 'PT yang bersangkutan')
        self.assertEqual(project_3_test.ts_2, 0)
        self.assertEqual(project_3_test.ts_1, 0)
        self.assertEqual(project_3_test.ts, 0)

        project_4_test = report_1.record_3a_711.search([['sumber_biaya', '=', 'Depdiknas']])
        self.assertEqual(project_4_test.sumber_biaya, 'Depdiknas')
        self.assertEqual(project_4_test.ts_2, 0)
        self.assertEqual(project_4_test.ts_1, 0)
        self.assertEqual(project_4_test.ts, 0)

        project_5_test = report_1.record_3a_711.search([['sumber_biaya', '=', 'Institusi dalam negeri di luar Depdiknas']])
        self.assertEqual(project_5_test.sumber_biaya, 'Institusi dalam negeri di luar Depdiknas')
        self.assertEqual(project_5_test.ts_2, 0)
        self.assertEqual(project_5_test.ts_1, 0)
        self.assertEqual(project_5_test.ts, 0)

        project_6_test = report_1.record_3a_711.search([['sumber_biaya', '=', 'Institusi luar negeri']])
        self.assertEqual(project_6_test.sumber_biaya, 'Institusi luar negeri')
        self.assertEqual(project_6_test.ts_2, 0)
        self.assertEqual(project_6_test.ts_1, 0)
        self.assertEqual(project_6_test.ts, 0)
