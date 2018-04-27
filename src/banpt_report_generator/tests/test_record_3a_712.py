# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    rec_3a_712 = context.env['banpt_report_generator.record_3a_712'].create(dict(
        mhs_ta_penelitian_dosen='ada',
        jml_mhs_ta_penelitian_dosen=75,
        jml_mhs_ta_total=100
    ))

    return rec_3a_712

class TestRecord_3A_712(common.TransactionCase):
    def test_refresh(self):
        rec_3a_712 = seed(self)

        project_1_test = rec_3a_712.search([['mhs_ta_penelitian_dosen', '=', 'ada']])
        self.assertEqual(project_1_test.mhs_ta_penelitian_dosen, 'ada')
        self.assertEqual(project_1_test.jml_mhs_ta_penelitian_dosen, 75)
        self.assertEqual(project_1_test.jml_mhs_ta_total, 100)
