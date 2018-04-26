# -*- coding: utf-8 -*-

from odoo.tests import common

def seed(context):
    prodi_if = context.env['itb.academic_program'].create(dict(
        name='Informatika', name_en='Informatics', prefix='135', degree='s1', active=True
    ))

    dosen_if_1 = context.env['hr.employee'].create(dict(
        name='Ridwan Kamal',
        nidn='014-A5A-133-C2D',
        birthday='1970-03-22',
        is_faculty=True,
        prodi=prodi_if.id
    ))

    project_1 = context.env['itb.hr_project'].create(dict(
        name='test_1',
        tipe='penelitian',
        start='2014-03-09',
        state='valid',
        deskripsi_sispran='DES-01',
        reference='REF-01',
        nilai=1000000
    ))

    context.env['itb.hr_project_team'].create(dict(employee_id=dosen_if_1.id, role='leader', project_id=project_1.id))

    report_1 = context.env['banpt_report_generator.report'].create(dict(
        name='Sample Report 1 - IF',
        year=2015,
        refresh_date='2015-06-22 10:00:00',
        prodi=prodi_if.id
    ))

    return report_1

class TestRecord_3A_622(common.TransactionCase):
    def test_refresh(self):
        report_1 = seed(self)

        report_1.refresh()

        project_1_test = report_1.record_3a_622.search([['judul_penelitian', '=', 'test_1']])
        self.assertEqual(project_1_test.judul_penelitian, 'test_1')
        self.assertEqual(project_1_test.tahun, 2014)
        self.assertEqual(project_1_test.sumber_jenis_dana, 'DES-01 - REF-01')
        self.assertEqual(project_1_test.jumlah_dana, 1000000/1000000)
