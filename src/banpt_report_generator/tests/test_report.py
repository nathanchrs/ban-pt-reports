# -*- coding: utf-8 -*-

from odoo.tests import common
from . import testutils

sample_report_1 = dict(
    name='Sample Report 1',
    year=2015,
    prodi='Teknik Informatika',
    refresh_date='2015-03-22 10:00:00'
)

class TestReport(common.TransactionCase):
    def test_write(self):
        pass

    def test_approve(self):
        pass

    def test_refresh(self):
        record = self.env['banpt_report_generator.report'].create(sample_report_1)
        record.refresh()
        self.assertGreater(
            testutils.parse_datetime(record.refresh_date),
            testutils.parse_datetime(sample_report_1['refresh_date'])
        )
