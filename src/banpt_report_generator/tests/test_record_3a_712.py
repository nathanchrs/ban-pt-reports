# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))

    rec_3a_712 = context.env['banpt_report_generator.record_3a_712'].create(dict(
        mhs_ta_penelitian_dosen='ada',
        jml_mhs_ta_penelitian_dosen=75,
        jml_mhs_ta_total=100
    ))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1 - IF',
        year=2015,
        refresh_date='2015-06-22 10:00:00',
        prodi=prodi_if.id
    ))

    return report_1, rec_3a_712

class TestRecord_3A_712(common.TransactionCase):
    def test_refresh(self):
        report_1, rec_3a_712 = seed(self)

        report_1.refresh()

        project_1_test = rec_3a_712.search([['mhs_ta_penelitian_dosen', '=', 'ada']])
        self.assertEqual(project_1_test.mhs_ta_penelitian_dosen, 'ada')
        self.assertEqual(project_1_test.jml_mhs_ta_penelitian_dosen, 75)
        self.assertEqual(project_1_test.jml_mhs_ta_total, 100)

        project_1_test = report_1.record_3a_712.search([['mhs_ta_penelitian_dosen', '=', 'tidak']])
        self.assertEqual(project_1_test.mhs_ta_penelitian_dosen, 'tidak')
        self.assertEqual(project_1_test.jml_mhs_ta_penelitian_dosen, 0)
        self.assertEqual(project_1_test.jml_mhs_ta_total, 0)
